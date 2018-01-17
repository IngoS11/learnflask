#!env/bin/python
import os
import unittest
import coverage
import uuid

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

COV = coverage.coverage(
    branch=True,
    omit=[
      'tests/*',
      'manage.py',
      'env/*',
      'venv/*'
    ]
)
COV.start()


from app import app, db, Task, User
from werkzeug.security import generate_password_hash

migrate = Migrate(app, db)
manager= Manager(app)

# migrations
manager.add_command('db', MigrateCommand)

@manager.command
def test():
  """Runs the unit tests without test coverage."""
  tests = unittest.TestLoader().discover('tests', pattern='test*.py')
  result = unittest.TextTestRunner(verbosity=2).run(tests)
  if result.wasSuccessful():
      return 0
  return 1

@manager.command
def cov():
  """Runs the unit tests with coverage."""
  tests = unittest.TestLoader().discover('tests')
  result = unittest.TextTestRunner(verbosity=2).run(tests)
  if result.wasSuccessful():
      COV.stop()
      COV.save()
      print('Coverage Summary:')
      COV.report()
      basedir = os.path.abspath(os.path.dirname(__file__))
      covdir = os.path.join(basedir, 'tmp/coverage')
      COV.html_report(directory=covdir)
      print('HTML version: file://%s/index.html' % covdir)
      COV.erase()
      return 0
  return 1

@manager.command
def create_db():
  """Creates the db tables."""
  db.create_all()

@manager.command
def drop_db():
  """Drops the db tables."""
  db.drop_all()

@manager.command
def seed():
  """Seeds the database with some initial data"""
  pwd = generate_password_hash('test1234', method='sha256')
  user = User(public_id=str(uuid.uuid4()), name='Ingo', password=pwd, admin=False)
  task = Task(title='simple task', description='this is a very simple task with description', done=False, user_id=user.id)
  db.session.add(user)
  db.session.add(task)
  db.session.commit()

if __name__ == '__main__':
    manager.run()

