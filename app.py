#!env/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisthesecretkey'

tasks = [
  {
    'id': 1,
    'title': u'Buy groceries',
    'description': u'Milk, Cheese, Pizza, Fruite, Tylenol',
    'done': False
  },
  {
    'id': 2,
    'title': u'Learn Python',
    'description': u'We need to find a good Python tutorial on the web',
    'done': False
  }
]

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = request.args.get('token') # http://localhost:5000/route?token=akvjaskdjdlavakdsal
    if not token:
      return jsonify({'message':'Token is missing'}), 403

    try:
      data = jwt.decode(token, app.config['SECRET_KEY'])
    except:
      return jsonify({'message':'Token is invalid'}), 403
    return f(*args,**kwargs)
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
  if auth and auth.password == 'pypass':
    token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=30)},app.config['SECRET_KEY'])
    return jsonify({'token' : token.decode('UTF-8')})
  return make_response('Cloud not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login required"'})

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@token_required
def index():
  return jsonify({'tasks': [make_public_task(task) for task in tasks]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@token_required
def get_task(task_id):
  task = [task for task in tasks if task['id'] == task_id]
  if len(task) == 0:
    abort(404) 
  return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@token_required
def create_task():
  if not request.json or not 'title' in request.json:
    abort(400)
  task = {
    'id': tasks[-1]['id'] + 1,
    'title': request.json['title'],
    'description': request.json.get('description', ""),
    'done': False
  }
  tasks.append(task)
  return jsonify({'task': task}), 201

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@token_required
def update_taks(task_id):
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
  task[0]['description'] = request.json.get('description', task[0]['description'])
  task[0]['done'] = request.json.get('done', task[0]['done'])
  return jsonify({'task': task[0]})

@app.route('/todos/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(task_id):
  task = [task for task in tasks if task['id'] == task_id]
  if len(task) == 0:
    abort(404)
  tasks.remove(task[0])
  return jsonify({'result': True})

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
