CREATE TABLE IF NOT EXISTS types ( 
  id integer not null PRIMARY KEY AUTOINCREMENT,
  name text not null
);

CREATE TABLE IF NOT EXISTS users ( 
  id integer not null PRIMARY KEY AUTOINCREMENT,
  first_name text not null,
  last_name text not null,
  email text not null UNIQUE,
  password text not null
);

CREATE TABLE IF NOT EXISTS categories ( 
  id integer not null PRIMARY KEY AUTOINCREMENT,
  name text not null,
  parent_id integer not null,
  user_id integer not null REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS operations ( 
  id integer not null PRIMARY KEY AUTOINCREMENT,
  type_id integer not null REFERENCES types(id),
  amount integer not null,
  operation_date datetime not null,
  user_id integer not null REFERENCES users(id),
  description text not null,
  created_date datetime not null,
  category_id integer not null REFERENCES categories(id)
);