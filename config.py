import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
  """Base configuration."""
  SECRET_KEY = os.getenv('SECRET_KEY', 'thisisjustatest')
  DEBUG = False
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tasks.db'

class DevelopmentConfig(BaseConfig):
  """Development configuration."""
  DEBUG = True

class TestingConfig(BaseConfig):
  DEBUG = True
  TESTING = True
  PRESERVE_CONTEXT_ON_EXCEPTION = False

class ProductionConfig(BaseConfig):
  SECRET_KEY = os.getenv('SECRET_KEY', 'thisshouldneverbeused')
