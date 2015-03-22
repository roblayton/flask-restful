#!venv/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# need to add setup.py and unit tests

# datastore
tasks = [
  {
    'id': 1,
    'title': u'Buy groceries',
    'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
    'done': False
  },
  {
    'id': 2,
    'title': u'Learn Python',
    'description': u'Need to find a good Python tutorial on the web',
    'done': False
  }
]

@app.route('/')
def index():
  return "Flask API!" # should print out the endpoints to the user

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
  return jsonify({'tasks': [make_public_task(task) for task in tasks]})

@app.route('/todo/api/v1.0/task/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
  task = [task for task in tasks if task['id'] == task_id]
  if len(task) == 0:
    abort(404)
  return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
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
  return jsonify({'task': make_public_task(task)}), 201

@app.route('/todo/api/v1.0/task/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
  if not request.json or not task_id:
    abort(400)
  for task in (t for t in tasks if t['id'] == task_id):
    task['title'] = request.json.get('title', task['title'])
    task['description'] = request.json.get('description', task['description'])
    return jsonify({'task': make_public_task(task)})
  abort(404)

def make_public_task(task):
  new_task = {}
  for field in task:
    if field == 'id':
      new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)
    else:
      new_task[field] = task[field]
  return new_task

# authentication
@auth.get_password
def get_password(username):
  if username == 'test':
    return 'password'
  return None

# error handling
@auth.error_handler
def unauthorized():
  return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
  app.run(debug=True)
  
