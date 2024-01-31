#!flask/bin/python
from flask import Flask, jsonify, make_response, abort, request
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import *

app = Flask(__name__)

db = psycopg2.connect(database = "postgres", user = "postgres", password = "1111", host = "localhost", port = "5432")
cursor = db.cursor(cursor_factory = RealDictCursor)
# cursor.execute("select * from product_types")
# print(cursor.fetchall())


data = [
  {
    'id': 1234,
    'amount': 34.60,
    'user_id': 'stas',
    'order_date': '12-12-2024'
  }
]

@app.route('/orders', methods=['GET'])
def get_orders():
    cursor.execute("select * from orders")
    return jsonify({'orders': cursor.fetchall()})


@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'not found'}), 404)

@app.errorhandler(400)
def invalid_in(error):
    return make_response(jsonify({'error': 'invalid input'}), 400)

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    cursor.execute(f"select * from orders where id = {order_id}")
    # order = list(filter(lambda x: x['id'] == order_id, data))
    order = cursor.fetchall()
    if not order:
      abort(404)
    return jsonify({'order': order[0]})

@app.route('/orders', methods=['POST'])
def add_orders():
    if not request.json or not 'user_id' in request.json:
      abort(400)
    print(f"INSERT INTO orders (order_date, user_id) VALUES ({datetime.strptime(request.json['order_date'], '%Y-%d-%m').date() if 'order_date' in request.json else datetime.now()},{request.json['user_id']})")
    cursor.execute(f"INSERT INTO orders (order_date, user_id) VALUES (\'{datetime.strptime(request.json['order_date'], '%Y-%d-%m').date() if 'order_date' in request.json else datetime.now()}\',{request.json['user_id']}) ")
    return jsonify({'result': 'insert success'})

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_orders(order_id):
    cursor.execute(f"select * from orders where id = {order_id}")
    order = cursor.fetchall()
    if not order:
      abort(404)
    if not request.json or not 'user_id' in request.json:
      abort(400)
    cursor.execute(f"UPDATE orders SET order_date = \'{datetime.strptime(request.json['order_date'], '%Y-%d-%m').date() if 'order_date' in request.json else datetime.now()}\', user_id = {request.json['user_id']} WHERE id = {order_id}")
    cursor.execute(f"select * from orders where id = {order_id}")
    order = cursor.fetchall()
    return jsonify({'order': order[0]})

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_orders(order_id):
    # order = list(filter(lambda x: x['id'] == order_id, data))
    # if len(order) == 0:
    #   abort(404)
    # data.remove(order[0])
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
    # user = list(filter(lambda x: x['user_id'] == user_id, info))
    if not user:
      abort(404)
    return jsonify({'user': user[0]})

@app.route('/users', methods=['POST'])
def add_users():
    if not request.json:
      abort(404)
    cursor.execute(f"insert into users (user_name, email) VALUES (\'{request.json['user_name'] if 'user_name' in request.json else 'cringe'}\', \'{request.json['email']}\')")
    # user = {
    #     'user_id': info[-1]['user_id'] + 1,
    #     'name': request.json['name'] if 'name' in request.json else '',
    #     'orders': request.json['orders'],
    #     'region': request.json['region'] if 'region' in request.json else ''
    #   }
    # info.append(user)
    # print(user, info)
    return jsonify({'user': "success"})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_users(user_id):
    cursor.execute(f"select * from users where id={user_id}")
    user = cursor.fetchall()
    # user = list(filter(lambda x: x['user_id'] == user_id, info))
    if not user:
      abort(404)
    if not request.json:
      abort(400)
    cursor.execute(f"UPDATE users SET user_name = \'{request.json['user_name'] if 'user_name' in request.json else user[0]['user_name']}\', email = \'{request.json['email'] if 'email' in request.json else user[0]['email']}\' where id = {user_id}")
    # user[0] = {
    #   'user_id': user[0]['user_id'],
    #   'amount': request.json['name'] if 'name' in request.json else user[0]['name'],
    #   'orders': request.json['orders'] if 'orders' in request.json else user[0]['orders'],
    #   'region': request.json['region'] if 'region' in request.json else user[0]['region']
    # }
    cursor.execute(f"select * from users where id = {user_id}")
    cursor.fetchall()
    return jsonify({'user': user[0]})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_users(user_id):
    cursor.execute(f"select * from users where id = {user_id}")
    user = cursor.fetchall()
    if not user:
        abort(404)
    # user = list(filter(lambda x: x['user_id'] == user_id, info))
    # if len(user) == 0:
    #   abort(404)
    # data.remove(user[0])
    cursor.execute(f"delete from users where id = {user_id}")
    return jsonify({'result': True})


# if __name__ == 'main':
app.run(debug=True)

#
# INSERT INTO Products (product_name, type_id, price)
# VALUES
#   ('Wireless Headphones', 1, 79.99),
#   ('Running Shoes', 2, 49.99),
#   ('Bookshelf', 3, 89.99),
#   ('Digital Camera', 1, 299.99),
#   ('Stainless Steel Water Bottle', 2, 14.99),
#   ('Laptop', 1, 999.99),
#   ('Smartphone', 1, 499.99),
#   ('T-shirt', 2, 19.99),
#   ('Jeans', 2, 39.99),
#   ('Coffee Table', 3, 149.99);