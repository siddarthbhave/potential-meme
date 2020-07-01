from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/testdb'

mongo = PyMongo(app)


@app.route('/')
def home():
    return 'Hello!'


@app.route('/add', methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _pwd = _json['pwd']

    if request.method == 'POST':
        _hashpass = generate_password_hash(_pwd)
        id = mongo.db.user.insert({
            'name': _name,
            'email': _email,
            'password': _hashpass
        })

    resp = jsonify('User added successfully!')
    return resp


@app.route('/users', methods=['GET'])
def display():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp


@app.route('/users/<id>', methods=['GET'])
def display_one(id):
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp


@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    mongo.db.user.delete_one({'_id': ObjectId(id)})
    resp = jsonify("User deleted successfully")
    resp.status_code = 200
    return resp


@app.route('/update/<id>', methods=['PUT'])
def edit(id):
    _json = request.json
    _id = id
    _name = _json['name']
    _email = _json['email']
    _pwd = _json['pwd']
    if request.method == 'PUT':
        password = generate_password_hash(_pwd)
        mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(
            _id)}, {'$set': {'name': _name, 'email': _email, 'pwd': password}})
    resp = jsonify("Updated user successfully")
    resp.status_code = 200
    return resp


if __name__ == "__main__":
    app.run(debug=True)
