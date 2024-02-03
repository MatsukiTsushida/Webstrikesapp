#!flask/bin/python
from flask import Flask, jsonify, make_response, abort, request
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import *

app = Flask(__name__)

db = psycopg2.connect(database = "postgres", user = "postgres", password = "1111", host = "localhost", port = "5432")
cursor = db.cursor(cursor_factory = RealDictCursor)



@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'not found'}), 404)

@app.errorhandler(400)
def invalid_in(error):
    return make_response(jsonify({'error': 'invalid input'}), 400)

@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'User': 'Unauthorized'}), 401)

@app.errorhandler(403)
def forbidden(error):
    return make_response(jsonify({'Content': 'forbidden'}), 403)

@app.errorhandler(410)
def Gone(error):
    return make_response(jsonify({'Record gone': 'deleted'}), 410)

@app.errorhandler(429)
def toomanyrequests(error):
    return make_response(jsonify({'Requests': 'too many'}), 429)

@app.errorhandler(500)
def internalserver(error):
    return make_response(jsonify({'Server': 'error'}), 500)

@app.errorhandler(502)
def BadGateway(error):
    return make_response(jsonify({'two': 'bad servers'}), 502)





@app.route('/orders', methods=['GET'])
def get_orders():
    cursor.execute("select * from orders")
    return jsonify({'orders': cursor.fetchall()})

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    cursor.execute(f"select * from orders where id = {order_id}")
    order = cursor.fetchall()
    if not order:
      abort(404)
    return jsonify({'order': order[0]})

@app.route('/orders', methods=['POST'])
def add_orders():
    if not request.json or not 'user_id' in request.json:
      abort(400)
    print(f'''INSERT INTO orders (order_date, user_id) 
               VALUES ({datetime.strptime(request.json['order_date'], '%Y-%d-%m').date() if 'order_date' in request.json else datetime.now()},
                      {request.json['user_id']})''')
    cursor.execute(f'''INSERT INTO orders (order_date, user_id) 
                       VALUES (\'{datetime.strptime(request.json['order_date'], '%Y-%d-%m').date() if 'order_date' in request.json else datetime.now()}\',
                              {request.json['user_id']}) ''')
    return jsonify({'result': 'insert success'})

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_orders(order_id):
    cursor.execute(f"select * from orders where id = {order_id}")
    order = cursor.fetchall()
    if not order:
      abort(404)
    if not request.json or not 'user_id' in request.json:
      abort(400)
    cursor.execute(f'''UPDATE orders 
        SET order_date = \'{datetime.strptime(request.json['order_date'], '%Y-%d-%m').date() if 'order_date' in request.json else datetime.now()}\',
        user_id = {request.json['user_id']} WHERE id = {order_id}''')
    cursor.execute(f"select * from orders where id = {order_id}")
    order = cursor.fetchall()
    return jsonify({'order': order[0]})

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_orders(order_id):
    cursor.execute(f"select * from orders where id = {order_id}")
    order = cursor.fetchall()
    if not order:
        abort(404)
    cursor.execute(f"delete from orders where id = {order_id}")
    return jsonify({'result': True})


@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute("select * from users")
    users = cursor.fetchall()
    return jsonify({'users': users})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    cursor.execute(f"select * from users where id={user_id}")
    user = cursor.fetchall()
    if not user:
      abort(404)
    return jsonify({'user': user[0]})

@app.route('/users', methods=['POST'])
def add_users():
    if not request.json:
      abort(404)
    cursor.execute(f'''INSERT INTO users (user_name, email) 
                        VALUES (\'{request.json['user_name'] if 'user_name' in request.json else 'cringe'}\',
                                \'{request.json['email']}\')''')
    return jsonify({'user': "success"})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_users(user_id):
    cursor.execute(f"select * from users where id={user_id}")
    user = cursor.fetchall()
    if not user:
      abort(404)
    if not request.json:
      abort(400)
    cursor.execute(f'''UPDATE users 
                       SET user_name = \'{request.json['user_name'] if 'user_name' in request.json else user[0]['user_name']}\',
                        email = \'{request.json['email'] if 'email' in request.json else user[0]['email']}\' where id = {user_id}''')
    cursor.execute(f"select * from users where id = {user_id}")
    cursor.fetchall()
    return jsonify({'user': user[0]})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_users(user_id):
    cursor.execute(f"select * from users where id = {user_id}")
    user = cursor.fetchall()
    if not user:
        abort(404)
    cursor.execute(f"delete from users where id = {user_id}")
    return jsonify({'result': True})


app.run(debug=True)

