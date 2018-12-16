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
    DATABASE_URL = "postgres://vmumuasubnpcpq:0710f7d02383e1835620eedc4e939fc644d712d5a48923e20dbf2ee17d440214@ec2-54-243-150-10.compute-1.amazonaws.com:5432/d359hbd00asc7a"


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
