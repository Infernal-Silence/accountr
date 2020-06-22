from .base import BaseService


class TypesService(BaseService):
    """
    Обработка работы с типами операций (/types)
    get_types - получение информации о типах операций
    get_type - получение информации о заданной в type_id типе операции
    """

    def get_types(self):
        """
        Возвращает информацию о типах операицй в виде списка словарей
        """
        with self.connection as con:
            cur = con.execute("""
                SELECT id, name
                FROM types
            """
            )
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    def get_type(self, type_id):
        """
        Возвращает информацию о заданном в type_id типе операции в виде словаря
        """
        result = {}
        with self.connection as con:
            cur = con.execute("""
                SELECT id, name 
                FROM types
                WHERE id = ?
            """, (type_id,)
                              )
        row = cur.fetchone()
        if row:
            result = dict(row)
        return result
