import os


class Config:
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_URL')


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_TESTING_URL')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
