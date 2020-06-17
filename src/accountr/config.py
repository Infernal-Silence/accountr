import os


class Config:
    DB_CONNECTION = os.getenv('DB_CONNECTION')
    SECRET_KEY = os.getenv('SECRET_KEY')
