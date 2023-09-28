import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'the_bland_mirror.sqlite3')


    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MSEARCH_INDEX_NAME = 'msearch'
    MSEARCH_PRIMARY_KEY = 'id'
    MSEARCH_ENABLE = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True