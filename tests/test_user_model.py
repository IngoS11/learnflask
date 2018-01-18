import unittest
import uuid

from app import app, db, User
from tests.base import BaseTestCase
from werkzeug.security import generate_password_hash

class TestUserModel(BaseTestCase):

  def test_encode_auth_token(self):
    pwd = generate_password_hash('test1234', method='sha256')
    user = User(public_id=str(uuid.uuid4()), name='ingo', password=pwd, admin=False)
    db.session.add(user)
    db.session.commit()
    auth_token = user.encode_auth_token(user.id)
    self.assertTrue(isinstance(auth_token, bytes))

  def test_auth_token(self):
    pwd = generate_password_hash('test1234', method='sha256')
    user = User(public_id=str(uuid.uuid4()), name='ingo', password=pwd, admin=False)
    db.session.add(user)
    db.session.commit()
    auth_token = user.encode_auth_token(user.id)
    self.assertTrue(isinstance(auth_token, bytes))

    self.assertTrue(User.decode_auth_token(
        auth_token.decode("utf-8")) == 1)


if __name__ == '__main__':
    unittest.main()
