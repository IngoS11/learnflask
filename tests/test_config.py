import unittest

from flask import current_app
from flask_testing import TestCase

from app import app

class TestDevelopmentConfig(TestCase):
  def create_app(self):
    app.config.from_object('config.DevelopmentConfig')
    return app

  def test_app_is_development(self):
    self.assertTrue(app.config['SECRET_KEY'] is 'thisisjustatest')
    self.assertTrue(app.config['DEBUG'] is True)
    self.assertFalse(current_app is None)
    self.assertTrue(
      app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///data/tasks.db'
    )

class TestTestingConfig(TestCase):
  def create_app(self):
    app.config.from_object('config.TestingConfig')
    return app

  def test_app_is_testing(self):
    self.assertTrue(app.config['SECRET_KEY'] is 'thisisjustatest')
    self.assertTrue(app.config['DEBUG'])
    self.assertTrue(
      app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///data/tasks.db'
    )

class TestProductionConfig(TestCase):
  def create_app(self):
    app.config.from_object('config.ProductionConfig')
    return app

  def test_app_is_production(self):
    self.assertFalse(app.config['DEBUG'])

if __name__ == '__main__':
    unittest.main()

