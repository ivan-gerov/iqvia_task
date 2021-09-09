
import os
from dotenv import dotenv_values

class Config:
    """ Base config object """
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.getenv("SECRET_KEY", "this-is-the-default-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "")

class DevelopmentConfig(Config):
    """ Development config object """
    WORKSPACE_ROOT = os.path.sep.join(os.getenv("VIRTUAL_ENV").split("/")[:-1])
    ENV_CONFIG_FILE = dotenv_values(f"{WORKSPACE_ROOT}/.development_env")
    SQLALCHEMY_DATABASE_URI = ENV_CONFIG_FILE["DATABASE_URL"]
    ENV = ENV_CONFIG_FILE["ENV"]


class TestingConfig(Config):
    TESTING = True

