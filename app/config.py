import os

basedir = os.path.abspath(os.path.dirname(__file__))


class ConfigMixin(object):
    LANGUAGES = ['en', 'es']
    CSRF_ENABLED = True
    DEBUG = os.environ.get("DEBUG") or False
    TESTING = os.environ.get("TESTING") or False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get("REDIS_URL")


class DevelopementConfig(ConfigMixin):
    DEBUG = True
    SECRET_KEY = "adivina-adivinanza"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "../app.db")
    REDIS_URL = "redis://localhost:6379/0"


class TestingConfig(ConfigMixin):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "adivina-adivinanza"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    REDIS_URL = "redis://localhost:6379/0"


class StagingConfig(ConfigMixin):
    DEBUG = True


class ProductionConfig(ConfigMixin):
    pass


app_config = {
    "development": DevelopementConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
}
