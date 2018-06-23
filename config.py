import os


class Config:
    DEBUG = False
    JWT_SECRET_KEY = os.getenv('SECRET')
    # SECRET_KEY = os.getenv('SECRET_KEY')
    # @staticmethod
    # def init_app(app):
    #     pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
