import os


class Config:
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_URL')


class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = os.getenv('DATABASE_TESTING_URL')


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
