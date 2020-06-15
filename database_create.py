import sqlite3
from database import db

with db.connection as con:
	cursor = con.cursor()
	cursor.executescript("""
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
		  name TEXT NOT NULL,
		  parent_id INTEGER NOT NULL,
		  user_id INTEGER NOT NULL REFERENCES users(id)
		);
		CREATE TABLE IF NOT EXISTS operations ( 
		  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		  type_id INTEGER NOT NULL REFERENCES types(id),
		  amount INTEGER NOT NULL,
		  operation_date DATETIME NOT NULL,
		  user_id INTEGER NOT NULL REFERENCES users(id),
		  description TEXT NOT NULL,
		  created_date DATETIME NOT NULL,
		  category_id INTEGER NOT NULL REFERENCES categories(id)
		);	
		""")
