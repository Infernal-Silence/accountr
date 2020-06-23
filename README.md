# accountr
Приложение для фиксирования доходов и расходов пользователей, чтобы пользователи могли видеть отчеты по своим личным финансам.

### [Техническое задание](https://docs.google.com/document/d/12RieA2g_HA7tVc9n1DKBoY3a4xHsPNBrY3W7v6yQfGQ/edit)

### Команда
**Red studio:**
+ Infernal-Silence - Lina Markes
+ konons - Konstantin Novoselov
+ AlexandrGrents - Alexandr Grents

### Инструкция по запуску
1. `$ poetry env use <путь к python>`
2. `$ poetry install`
3. Создать файл `.env` по образцу `.env.example`:
    ```
    FLASK_APP=accountr.app:create_app
    FLASK_ENV=development
    DB_CONNECTION=<путь к файлу базы данных>
    SECRET_KEY=<секретный ключ>
    ```
4. `$ poetry shell`
5. На windows (cmd): `$ set PYTHONPATH=./src`

   На windows (powershell): `$ $env:PYTHONPATH="./src"`

   На unix: `$ export PYTHONPATH=./src`
6. Если не создана база данных: `$ python database_create.py`
7. `$ flask run`
