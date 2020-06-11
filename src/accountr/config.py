import os


class Config:
    DB_CONNECTION = os.getenv('DB_CONNECTION')
