import math
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta, MO

from .base import BaseService
from .categories import CategoriesService

"""
Обработка работы с отчетом по операциям (/report)
get_report - получение информации об операциях авторизованного пользователя
"""


class ReportService(BaseService):
    def get_report(self, user_id, query_string):
        """
        Возвращает информацию об операциях пользователя user_id в виде словаря с учетом фильтров query_string
        """
        page = int(query_string.get('page', 1))
        page_size = int(query_string.get('page_size', 20))
        query_string = self._prepare_filters(user_id, query_string)
        query, params = self._build_report_query(query_string, page, page_size)
        cur = self.connection.execute(query, params)
        rows = cur.fetchall()

        categories_service = CategoriesService(self.connection)
        categories = {
            category['id']: dict(
                id =  category['id'],
                name = category['name'],
                parent_id = category['parent_id']
            )
            for category in categories_service.get_categories(user_id)
        }
        return self._build_report(rows, categories, page_size)

    def _prepare_filters(self, user_id, query_string):
        """
        Парсит query_string и возвращает список фильтров
        """
        filters = {'user_id': user_id}
        if 'start_date' in query_string:
            filters['start_date'] = datetime.fromisoformat(query_string['start_date'])
        if 'end_date' in query_string:
            filters['end_date'] = datetime.fromisoformat(query_string['end_date'])
        if 'category_id' in query_string:
            filters['category_id'] = query_string['category_id']
        if 'period' in query_string:
            period = query_string['period']
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if period == 'week':
                filters['start_date'] = today + relativedelta(weekday=MO(-1))
                filters['end_date'] = today + relativedelta(weekday=MO(0))
            elif period == 'prev_week':
                filters['start_date'] = today + relativedelta(weekday=MO(-2))
                filters['end_date'] = today + relativedelta(weekday=MO(-1))
            elif period == 'month':
                filters['start_date'] = today.replace(day=1)
                filters['end_date'] = today.replace(day=1) + relativedelta(months=1)
            elif period == 'prev_month':
                end = today.replace(day=1)
                filters['start_date'] = end - relativedelta(months=1)
                filters['end_date'] = end
            elif period == 'year':
                filters['start_date'] = today.replace(month=1, day=1)
                filters['end_date'] = today.replace(month=1, day=1) + relativedelta(years=1)
            elif period == 'prev_year':
                end = today.replace(month=1, day=1)
                filters['start_date'] = end - relativedelta(years=1)
                filters['end_date'] = end
            elif period == 'quarter':
                quarter = ((today.month - 1) // 3) + 1
                filters['start_date'] = datetime(today.year, quarter * 3 - 2, 1)
                filters['end_date'] = datetime(today.year, (quarter+1) * 3 - 2, 1)
            elif period == 'prev_quarter':
                quarter = ((today.month - 1) // 3) + 1
                end = datetime(today.year, quarter * 3 - 2, 1)
                filters['start_date'] = end - relativedelta(months=3)
                filters['end_date'] = end
        return filters

    def _build_report_query(self, filters, page, page_size):
        """
        Возвращает sql запрос и параметры с учетом списка фильтров и пагинации
        """

        query_template = """
            WITH RECURSIVE cat (id, user_id, name, parent_id, path) AS (
                SELECT id,
                       user_id,
                       name,
                       parent_id,
                       printf('[%d]', id) AS path
                FROM categories
                WHERE parent_id IS NULL

                UNION ALL

                SELECT c.id,
                       c.user_id,
                       c.name,
                       c.parent_id,
                       printf('%s.[%d]', cat.path, c.id) AS path
                FROM categories AS c
                INNER JOIN cat
                    ON c.user_id = cat.user_id AND c.parent_id = cat.id
                WHERE c.parent_id IS NOT NULL
            ), selected AS (
                SELECT
                    o.id,
                    types.name AS type_name,
                    CASE WHEN types.name = 'income' THEN o.amount
                         WHEN types.name = 'expenditure' THEN -o.amount
                    END AS amount,
                    cat.path AS category_path,
                    o.description,
                    o.operation_date,
                    o.created_date
                FROM operations AS o
                INNER JOIN types ON o.type_id = types.id
                LEFT JOIN cat ON o.category_id = cat.id
                WHERE {where_clauses}
            )
            SELECT
                *,
                COUNT(*) OVER () AS total_items,
                SUM(amount) OVER () AS total_amount
            FROM selected
            ORDER BY operation_date, id
            LIMIT ? OFFSET ?
        """
        params = []
        where_clauses = []

        if 'user_id' in filters:
            user_id = filters['user_id']
            where_clauses.append('o.user_id = ?')
            params.append(user_id)

        if 'start_date' in filters:
            start_date = filters['start_date']
            where_clauses.append('strftime(\'%s\', o.operation_date) >= strftime(\'%s\', ?)')
            params.append(start_date)

        if 'end_date' in filters:
            end_date = filters['end_date']
            where_clauses.append('strftime(\'%s\', o.operation_date) < strftime(\'%s\', ?)')
            params.append(end_date)

        if 'category_id' in filters:
            category_id = filters['category_id']
            where_clauses.append('category_path LIKE ?')
            params.append(f'%[{category_id}]%')

        params.append(page_size)
        params.append((page - 1) * page_size)

        where_string = ' AND '.join(
            f'({clause})'
            for clause in where_clauses
        )
        query = query_template.format(where_clauses=where_string)
        return query, params

    def _build_report(self, rows, categories, page_size):
        """
        Собирает отчет из результата sql запроса rows, списка категорий categories ис учетом размера страницы page_size
        Возращает словарь сложной структуры
        """

        operations = []
        for row in rows:
            if not row['category_path']:
                categories_ids = []
            else:
                categories_ids = [
                    int(part[1:-1])
                    for part in row['category_path'].split('.')
                ]
            operation = {
                'id': row['id'],
                'operation_date': row['operation_date'],
                'created_date': row['created_date'],
                'type_name': row['type_name'],
                'amount': row['amount'],
                'description': row['description'],
                'categories': [
                    categories[category_id]
                    for category_id in categories_ids
                ]
            }
            operations.append(operation)
        if not operations:
            total_amount = 0
            total_items = 0
            total_pages = 0
        else:
            total_amount = rows[0]['total_amount']
            total_items = rows[0]['total_items']
            total_pages = math.ceil(total_items / page_size)
        return {
            'operations': operations,
            'total_amount': total_amount,
            'total_items': total_items,
            'total_pages': total_pages,
        }
