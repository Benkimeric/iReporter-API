import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    SECRET = os.getenv('SECRET')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    DATABASE_URL = "dbname='ireporter' host='localhost' port='5432' user='postgres'\
     password='kali12'"


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = False
    DATABASE_URL = "dbname='test_ireporter' host='localhost' port='5432' user='postgres'\
     password='kali12'"


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
