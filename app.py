from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+mysqlconnector://root:thegoblet2@localhost/fitness_center_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class CustomerSchema(ma.Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    age = fields.String(required=True)

class SessionSchema(ma.Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    age = fields.String(required=True)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

class Customer(db.Model):
    __tablename__ = 'Customers'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255))
    age = db.Column(db.String(255))

class Session(db.Model):
    __tablename__ = 'Sessions'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(255), nullable = False)
    time = db.Column(db.String(255))
    activity = db.Column(db.String(255))
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'))

with app.app_context():
    db.create_all()

@app.route('/customer<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return customer_schema.jsonify(customer)

@app.route('/customers', methods=['POST'])
def add_customer():
    customer_data = customer_schema.load(request.json)
    if customer_data is None:
        return jsonify({'message':"no member"}), 404
    try:
        new_customer = Customer(name = customer_data['name'], email = customer_data['email'], age = customer_data['age'])
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message':'customer added'}), 201
    except:
        pass
    finally:
        pass

@app.route('/customer<int:id>', methods=['PUT'])
def update_customer(id):
    customer_data = Customer.query.get_or_404(id)
    try:
        customer = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    customer.name = customer_data['name']
    customer.email = customer_data['email']
    customer.age = customer_data['age']
    db.session.commit()
    return jsonify({"message":'details updated successfully'}), 200



@app.route('/customer<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        customer = Customer.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'customer deleted'})
    except:
        pass
    finally:
        pass

if __name__ == '__main__':
    app.run(debug=True)

    