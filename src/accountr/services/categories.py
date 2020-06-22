from .base import BaseService


class CategoriesService(BaseService):
    """
    Обработка работы с категориями (/categories)
    get_categories - получение информации о всех категориях пользователя
    get_category - получение информации о заданной в category_id категории пользователя
    create_category - создает категорию пользователя
    update_category - изменяет информацию в заданной category_id категории пользователя
    delete_category - удаляет заданную категорию и все вложенные категории, убирает привязку категории к операциям
    """

    def get_categories(self, user_id):
        """
        Возвращает информацию о всех категориях пользователя, заданного user_id, в виде списка словарей
        """
        with self.connection as con:
            cur = con.execute("""
                SELECT id, name, parent_id, user_id 
                FROM categories
                WHERE user_id = ?
            """, (user_id,)
                              )
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    def get_category(self, category_id):
        """
        Возвращает информацию о заданной в category_id категории в виде словаря
        """
        result = {}
        with self.connection as con:
            cur = con.execute("""
                SELECT id, name, parent_id, user_id 
                FROM categories
                WHERE id = ?
            """, (category_id,)
                              )
        row = cur.fetchone()
        if row:
            result = dict(row)
        return result

    def create_category(self, user_id, category):
        """
        Создает категорию c параметрами category для заданного user_id
        Возвращает созданную категорию в виде словаря
        """
        result = {}
        name = category.get('name')
        parent_id = category.get('parent_id')
        if category:
            cursor = self.connection.cursor()
            cursor.execute(
                'INSERT INTO categories (name, parent_id, user_id) '
                'VALUES (?, ?, ?) ',
                (name, parent_id, user_id),
            )
            self.connection.commit()
            category_id = cursor.lastrowid
            result = self.get_category(category_id)

        return result

    def update_category(self, category_id, category):
        """
        Изменят категорию c параметрами category для заданного user_id
        Возвращает измененную категорию в виде словаря
        """
        result = {}
        if category_id and category:
            update = {key: value for key, value in category.items()}
            params = ','.join(f'{key} = ?' for key in update)
            query = f'UPDATE categories SET {params} WHERE id = ? '
            self.connection.execute(query, (*update.values(), category_id))
            self.connection.commit()
            result = self.get_category(category_id)

        return result

    def delete_category(self, user_id, category_id):
        """
        Удаляет категорию category_id и все вложенные категории для user_id
        Обнуляет привязку операций ко всем удаляемым категориям
        """
        if category_id:
            cursor = self.connection.cursor()
            cursor.execute("""
                    UPDATE operations SET category_id=NULL where category_id in (
                    WITH RECURSIVE child (id, user_id) AS 
                    (SELECT ? id, ? user_id
                      UNION ALL 
                     SELECT categories.id, categories.user_id FROM categories, child 
                            WHERE categories.parent_id = child.id and categories.user_id = child.user_id
                    )
                    SELECT id FROM child
                    );            
                """, (category_id, user_id)
            )
            cursor.execute("""
                DELETE FROM categories WHERE id IN (
                    WITH RECURSIVE child (id, user_id, parent_id) AS 
                    (SELECT ? id, ? user_id, null parent_id
                      UNION ALL 
                     SELECT categories.id, categories.user_id, categories.parent_id FROM categories, child 
                            WHERE categories.parent_id = child.id and categories.user_id = child.user_id
                    )
                    SELECT id FROM child ORDER BY parent_id DESC, id DESC
                );                
            """, (category_id, user_id)
            )
            self.connection.commit()