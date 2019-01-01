import os
import secrets

basedir = os.path.abspath((os.path.dirname(__name__)))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql://postgres:password@db:5432/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REGISTERS_API_KEY = os.environ.get('REGISTERS_KEY')
    REDIS_URL = os.environ.get('REDIS_URL') or "redis://redis:6379"
    STATIC_FOLDER = "/static"


class Test(Config):
    TESTDB = 'test_project.db'
    TEST_DATABASE_URI = 'sqlite///' + TESTDB
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = TEST_DATABASE_URI
