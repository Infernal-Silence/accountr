from .base import BaseService


class OperationsService(BaseService):
    """
    Обработка работы с операциями (/operations)
    get_operation - получение информации о заданной в operation_id операции пользователя
    create_operation - создает операцию пользователя
    update_operation - изменяет информацию в заданной operation_id операции пользователя
    delete_operation - удаляет заданную в operation_id операцию
    """

    def get_operation(self, operation_id):
        """
        Возвращает информацию о заданной в operation_id операции в виде словаря
        """
        result = {}
        with self.connection as con:
            cur = con.execute("""
                SELECT id, user_id, type_id, category_id, amount, operation_date, created_date, description 
                FROM operations
                WHERE id = ?
            """, (operation_id,)
                              )
        row = cur.fetchone()
        if row:
            result = dict(row)
        return result

    def create_operation(self, user_id, operation):
        """
        Создает операцию c параметрами operation для заданного user_id
        Возвращает созданную операцию в виде словаря
        """
        result = {}
        type_id = operation.get('type_id')
        category_id = operation.get('category_id')
        amount = operation.get('amount')
        if not amount:
            amount = 0

        operation_date = operation.get('operation_date')
        description = operation.get('description')

        if operation:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO operations (type_id, category_id, amount, operation_date, user_id, description, created_date) 
                VALUES (?, ?, ?, ?, ?, ?, DATETIME('now'))
            """,
                (type_id, category_id, amount, operation_date, user_id, description),
            )
            self.connection.commit()
            operation_id = cursor.lastrowid
            result = self.get_operation(operation_id)

        return result

    def update_operation(self, operation_id, operation):
        """
        Изменят операцию c параметрами operation для заданного operation_id
        Возвращает измененную операцию в виде словаря
        """
        result = {}
        if operation_id and operation:
            update = {key: value for key, value in operation.items()}
            params = ','.join(f'{key} = ?' for key in update)
            query = f'UPDATE operations SET {params} WHERE id = ? '
            amount = operation.get('amount')
            self.connection.execute(query, (*update.values(), operation_id))
            self.connection.commit()
            result = self.get_operation(operation_id)

        return result

    def delete_operation(self, operation_id):
        """
        Удаляет операцию operation_id
        """
        if operation_id:
            cursor = self.connection.cursor()
            cursor.execute("""
                DELETE FROM operations WHERE id = ?; 
            """, (operation_id,)
                           )
            self.connection.commit()
