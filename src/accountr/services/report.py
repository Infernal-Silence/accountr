import math
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from .base import BaseService
from .categories import CategoriesService


class ReportService(BaseService):
    def get_report(self, user_id, qs):
        page = qs.get('page', 1)
        page_size = qs.get('page_size', 20)
        filters = self._prepare_filters(user_id, qs)
        query, params = self._build_report_query(filters, page, page_size)
        cur = self.connection.execute(query, params)
        rows = cur.fetchall()
        categories_service = CategoriesService(self.connection)
        categories = {
            category['id']: category
            for category in categories_service.get_categories(user_id)
        }
        return self._build_report(rows, categories, page_size)

    def _prepare_filters(self, user_id, qs):
        filters = {'user_id': user_id}
        if 'start_date' in qs:
            filters['start_date'] = datetime.fromisoformat(qs['start_date'])
        if 'end_date' in qs:
            filters['end_date'] = datetime.fromisoformat(qs['end_date'])
        if 'category_id' in qs:
            filters['category_id'] = qs['category_id']
        if 'period' in qs:
            period = qs['period']
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if period == 'today':
                filters['start_date'] = today
            elif period == 'yesterday':
                filters['start_date'] = today - timedelta(days=1)
                filters['end_date'] = today
            elif period == 'month':
                filters['start_date'] = today.replace(day=1)
            elif period == 'prev_month':
                end = today.replace(day=1)
                filters['start_date'] = end - relativedelta(months=1)
                filters['end_date'] = end
            elif period == 'year':
                filters['start_date'] = today.replace(month=1, day=1)
            elif period == 'prev_year':
                end = today.replace(month=1, day=1)
                filters['start_date'] = end - relativedelta(years=1)
                filters['end_date'] = end
            elif period == 'quarter':
                quarter = ((today.month - 1) // 3) + 1
                filters['start_date'] = datetime(today.year, quarter * 3 - 2, 1)
            elif period == 'prev_quarter':
                quarter = ((today.month - 1) // 3) + 1
                end = datetime(today.year, quarter * 3 - 2, 1)
                filters['start_date'] = end - relativedelta(months=3)
                filters['end_date'] = end
        return filters

    def _build_report_query(self, filters, page, page_size):
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
            ), selected AS (
                SELECT
                    o.id,
                    types.name AS type_name,
                    CASE WHEN types.name = 'income' THEN o.amount
                         WHEN types.name = 'outcome' THEN -o.amount
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
            start_date = filters['start_date'].timestamp()
            where_clauses.append('o.operation_date >= ?')
            params.append(start_date)

        if 'end_date' in filters:
            end_date = filters['end_date'].timestamp()
            where_clauses.append('o.operation_date < ?')
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
        total_amount = rows[0]['total_amount'] / 100
        total_items = rows[0]['total_items']
        total_pages = math.ceil(total_items / page_size)
        operations = []
        for row in rows:
            categories_ids = [
                int(part[1:-1])
                for part in row['category_path'].split('.')
            ]
            operation = {
                'id': row['id'],
                'operation_date': datetime.fromtimestamp(row['operation_date']).isoformat(),
                'created_date': datetime.fromtimestamp(row['created_date']).isoformat(),
                'type_name': row['type_name'],
                'amount': row['amount'] / 100,
                'description': row['description'],
                'categories': [
                    categories[category_id]
                    for category_id in categories_ids
                ]
            }
            operations.append(operation)
        return {
            'operations': operations,
            'total_amount': total_amount,
            'total_items': total_items,
            'total_pages': total_pages,
        }
