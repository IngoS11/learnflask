#!env/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_sqlalchemy import SQLAlchemy
import jwt
import uuid
import datetime
import os
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app_settings = os.getenv('APP_SETTINGS', 'config.DevelopmentConfig')
app.config.from_object(app_settings)

db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  public_id = db.Column(db.String(50), unique=True)
  name = db.Column(db.String(50))
  password = db.Column(db.String(80))
  admin = db.Column(db.Boolean)

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50))
  description = db.Column(db.String(255))
  done = db.Column(db.Boolean)
  user_id = db.Column(db.Integer)

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = None
    if 'x-access-token' in request.headers:
       token = request.headers['x-access-token']
    if not token:
      return jsonify({'message':'Token is missing'}), 403

    try:
      data = jwt.decode(token, app.config['SECRET_KEY'])
      current_user = User.query.filter_by(public_id=data['public_id']).first()
    except:
      return jsonify({'message':'Token is invalid'}), 403
    return f(current_user, *args,**kwargs)
  return decorated

def make_public_task(task):
  new_task = {}
  for field in task:
    if field == 'id':
      new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
    else:
      new_task[field] = task[field]
    return new_task

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/login')
def login():
  auth = request.authorization
  if not auth or not auth.username or not auth.password:
    return make_response('Cloud not verify!', 401,
        {'WWW-Authenticate' : 'Basic realm="Login required"'})
  user = User.query.filter_by(name=auth.username).first()
  if not user: 
    return make_response('Cloud not verify!', 401,
        {'WWW-Authenticate' : 'Basic realm="Login required"'})
  if check_password_hash(user.password, auth.password):
    token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime
       .utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
    return jsonify({'token' : token.decode('UTF-8')})
  return make_response('Cloud not verify!', 401,
      {'WWW-Authenticate' : 'Basic realm="Login required"'})

@app.route('/api/v1.0/user', methods=['GET'])
@token_required
def get_all_users(current_user):
  if not current_user.admin:
    return jsonify({'message':'Admin authentication required!'}), 400
  users = User.query.all()
  output = []
  for user in users:
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    output.append(user_data)
  return jsonify({'users': output})

@app.route('/api/v1.0/user/<public_id>', methods=['GET'])
@token_required
def get_single_user(current_user, public_id):
  if not current_user.admin:
    return jsonify({'message':'Admin authentication required!'}), 400
  user = User.query.filter_by(public_id=public_id).first()
  if not user:
    return jsonify({'message':'No user found!'}), 404
  user_data = {}
  user_data['public_id'] = user.public_id
  user_data['name'] = user.name
  user_data['password'] = user.password
  user_data['admin'] = user.admin
  return jsonify({'user': user_data})

@app.route('/api/v1.0/user', methods=['POST'])
@token_required
def create_user(current_user):
  if not current_user.admin:
    return jsonify({'message':'Admin authentication required!'}), 400
  data = request.get_json()
  hashed_password = generate_password_hash(data['password'], method='sha256')
  new_user = User(public_id=str(uuid.uuid4()), name=data['name'],
    password=hashed_password, admin=False)
  db.session.add(new_user)
  db.session.commit()
  return jsonify({'message':'New user created!'}), 201

@app.route('/api/v1.0/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
  if not current_user.admin:
    return jsonify({'message':'Admin authentication required!'}), 400
  user = User.query.filter_by(public_id=public_id).first()
  if not user:
    return jsonify({'message':'No user found!'}), 404
  user.admin = True
  db.session.commit()
  return jsonify({'message':'User has been promoted'}), 201

@app.route('/api/v1.0/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
  if not current_user.admin:
    return jsonify({'message':'Admin authentication required!'}), 400
  user = User.query.filter_by(public_id=public_id).first()
  if not user:
    return jsonify({'message':'No user found!'}), 404
  db.session.delete(user)
  db.session.commit()
  return jsonify({'message':'The user has been deleted'}), 200

@app.route('/api/v1.0/tasks', methods=['GET'])
@token_required
def index(current_user):
  tasks = Task.query.filter_by(user_id=current_user.id).all()
  output = []
  for task in tasks:
    task_data = {}
    task_data['id'] = task.id
    task_data['title'] = task.title
    task_data['description'] = task.description
    task_data['done'] = task.done
    output.append(task_data)
  return jsonify({'tasks': output })

@app.route('/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@token_required
def get_task(current_user, task_id):
  task = Task.query.filter_by(id=task_id).first()
  if not task:
    abort(404) 
  return jsonify({'task': task})

@app.route('/api/v1.0/tasks', methods=['POST'])
@token_required
def create_task(current_user):
  if not request.json or not 'title' in request.json:
    abort(400)
  data = request.get_json()
  new_task = Task(title=data['title'], description=data['description'],
    done=False, user_id=current_user.id)
  db.session.add(new_task)
  db.session.commit()
  return jsonify({'message':'task was create'}), 201

@app.route('/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_taks(current_user, task_id):
  task = [task for task in tasks if task['id'] == task_id]
  if len(task) == 0:
    abort(404)
  if not request.json:
    abort(400)
  if 'title' in request.json:
    abort(400)
  if 'description' in request.json:
    abort(400)
  if 'done' in request.json and type(request.json['done']) is not bool:
    abort(400)
  task[0]['title'] = request.json.get('title', task[0]['title'])
  task[0]['description'] = request.json.get('description',
      task[0]['description'])

  task[0]['done'] = request.json.get('done', task[0]['done'])
  return jsonify({'task': task[0]})

@app.route('/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
  task = [task for task in tasks if task['id'] == task_id]
  if len(task) == 0:
    abort(404)
  tasks.remove(task[0])
  return jsonify({'result': True})

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
