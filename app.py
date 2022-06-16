from crypt import methods
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



# Init App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__)) # So flask know where the db is. Base directory

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db = SQLAlchemy(app)

# Init MA
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity')

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create Product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']

    new_product = Product(name, description, price, quantity)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# Get all products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)

    return jsonify(result)

# Get all products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# 

# TESTING GET REQUEST
# @app.route('/', methods=['GET'])
# def get():
#     return jsonify({'msg': 'Hello World'})



if __name__ == '__main__':
    app.run(debug=True)
