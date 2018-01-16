#!env/bin/python
from app import db, Task, User
from werkzeug.security import generate_password_hash
import uuid
# create the database
db.create_all()

# seed the database with some data
pwd = generate_password_hash('test1234', method='sha256')
user = User(public_id=str(uuid.uuid4()), name='ingo', password=pwd, admin=False)
task = Task(title='simple task', description='this is a simple test task', done=False, user_id=user.id)
db.session.add(user)
db.session.add(task)
db.session.commit()
