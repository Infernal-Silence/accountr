# Спецификация API

---
## Работа с пользователем
### Регистрация
Метод: **POST**

Запрос:
```
{
    first_name: str,
    last_name: str,
    email: str,
    password: str
}
```
Код успешного ответа: **200**

Ответ:
```
{
    id: int,
    first_name: str,
    last_name: str,
    email: str,
    password: str
}
```
Примечания:
- Если пользователь уже был создан ранее, возвращает код ошибки ...
- Если нет части параметров, возвращает код ошибки 403 

---
### Авторизация
Метод: **POST**

Запрос:
```
{
    email: str,
    password: str
}
```
Код успешного ответа: **200**

Ответ:
```
{
    id: int,
    email: str,
    password: str
}
```
Примечания:
- Если логин или пароль неверные, возвращает код ошибки 401

---
### Выход из аккаунта
Метод: **POST**

Запрос: **пустой**

Код успешного ответа: **200**

Ответ: **пустой**

Примечания:


----
## Работа с операциями
### Создание операции
Требования: 
 - пользователь авторизован

Метод: **POST**

Запрос:
```
{
    user_id: int,
    type_id: int,
    category_id: int,
    amount: float,
    operation_date: date,
    description: str    
}
```
Код успешного ответа: **201**

Ответ:
```
{
    id: int,
    user_id: int,
    type_id: int,
    category_id: int,
    amount: float,
    operation_date: date,
    description: str
}
```
Примечания:


----
### Изменение созданной операции
Требования: 
 - пользователь авторизован
 - пользователь обновляет только свою операцию

Метод: **PATCH**

Запрос:
```
{
    id: int,
    user_id: int,
    type_id: int?,
    category_id: int?,
    amount: float?,
    operation_date: date?,
    description: str?  
}
```
Код успешного ответа: **200**

Ответ:
```
{
    id: int,
    user_id: int,
    type_id: int,
    category_id: int,
    amount: float,
    operation_date: date,
    description: str
}
```
Примечания:


----
### Удаление созданной операции
Требования: 
 - пользователь авторизован
 - пользователь обновляет только свою операцию

Метод: **DELETE**

Запрос:
```
{
    id: int,
    user_id: int
}
```
Код успешного ответа: **200**

Ответ:
```
{
    id: int,
    user_id: int,
    type_id: int,
    category_id: int,
    amount: float,
    operation_date: date,
    description: str
}
```
Примечания:


----
## Работа с категориями
### Добавление категории 
Метод: **POST**

Запрос:
```
{
    name: str,
    parent_category: int?
}
```
Код успешного ответа: **200**

Ответ:
```
{
    id: int,
    name: str,
    user_id: int,
    parent_id: int?
}
```
Примечания:


----
### Изменение категории
Метод: **PATCH**

Запрос:
```
{
    id: int,
    name: str?,
    parent_id: int?
}
```
Код успешного ответа: **200**

Ответ:
```
{
    id: int,
    name: str,
    user_id: int,
    parent_id: int?
}
```
Примечания:


----
### Удаление категории
Метод: **DELETE**

Запрос: пустой
```
{

}
```
Код успешного ответа: **200**

Ответ:
```
{

}
```
Примечания:


----
## Работа с отчётами
### Получение отчёта