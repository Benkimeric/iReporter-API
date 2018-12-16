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


class ProductionConfig(Config):
    """"Configurations for production"""

    DEBUG = False
    TESTING = False
    DATABASE_URL = "postgres://szjgiekrolovoc:a68f2b6ca11a48ac9eb8347eb2d9fad9b378aad66611b09cc728dc56f3ec3b72@ec2-54-247-102-1.eu-west-1.compute.amazonaws.com:5432/dd8qlehec47quf"


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = False
    DATABASE_URL = "dbname='test_ireporter' host='localhost' port='5432' user='postgres'\
     password='kali12'"


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
