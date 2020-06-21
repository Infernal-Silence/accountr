import os
import sqlite3
from dotenv import load_dotenv


load_dotenv()
db_connection = os.getenv('DB_CONNECTION')


with sqlite3.connect(db_connection) as connection:
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS types ( 
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS users ( 
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS categories ( 
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            name TEXT NOT NULL,
            parent_id INTEGER NOT NULL,
            UNIQUE (user_id, name)
        );
        CREATE TABLE IF NOT EXISTS operations ( 
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            type_id INTEGER NOT NULL REFERENCES types(id),
            category_id INTEGER NOT NULL REFERENCES categories(id),
            amount INTEGER NOT NULL,
            description TEXT NOT NULL,
            operation_date DATETIME NOT NULL,
            created_date DATETIME NOT NULL
        );
        INSERT INTO types (name) VALUES('доход');
        INSERT INTO types (name) VALUES('расход');
    """)
    connection.commit()
