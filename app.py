#!venv/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask.ext.httpauth import HTTPBasicAuth
import time
import datetime


app = Flask(__name__)
auth = HTTPBasicAuth()
ts = time.time()

# need to add setup.py and unit tests

# datastore
orders = [
  {
    'id': 44029472,
    'date': u'',
    'customer_id': 220300,
    'customer_name': u'David',
    'customer_address': u'Anchorage, Alaska'
  },
  {
    'id': 440929472,
    'date': u'',
    'customer_id': 220300,
    'customer_name': u'Jack',
    'customer_address': u'New York, New York'
  },
]

@app.route('/')
def index():
  return "Flask API!" # should print out the endpoints to the user

@app.route('/orders/api/v1.0/orders', methods=['GET'])
@auth.login_required
def get_orders():
  return jsonify({'orders': [make_public_order(order) for order in orders]})

@app.route('/orders/api/v1.0/order/<int:order_id>', methods=['GET'])
@auth.login_required
def get_order(order_id):
  order = [order for order in orders if order['id'] == order_id]
  if len(order) == 0:
    abort(404)
  return jsonify({'order': order[0]})

@app.route('/orders/api/v1.0/orders', methods=['POST'])
@auth.login_required
def create_order():
  if not request.json or not 'title' in request.json:
    abort(400)
  order = {
    'id': orders[-1]['id'] + 1,
    'date': datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'),
    'customer_id': order[-1]['customer_id'] + 1,
    'customer_name': request.json.get('customer_name', ""),
    'customer_address': request.json.get('customer_name', "")
  }
  orders.append(order)
  return jsonify({'order': make_public_order(order)}), 201

@app.route('/orders/api/v1.0/order/<int:order_id>', methods=['PUT'])
@auth.login_required
def update_order(order_id):
  if not request.json or not order_id:
    abort(400)
  for order in (t for t in orders if t['id'] == order_id):
    order['customer_id'] = request.json.get('customer_id', order['customer_id'])
    order['customer_name'] = request.json.get('customer_name', order['customer_name'])
    order['customer_address'] = request.json.get('description', order['customer_address'])
    return jsonify({'order': make_public_order(order)})
  abort(404)

def make_public_order(order):
  new_order = {}
  for field in order:
    if field == 'id':
      new_order['uri'] = url_for('get_order', order_id = order['id'], _external = True)
    else:
      new_order[field] = order[field]
  return new_order

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
  
