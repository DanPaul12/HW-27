from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+mysqlconnector://root:thegoblet2@localhost/fitness_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Customer(db.Model):
    __tablename__ = 'Members'
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
    customer_id = db.Column(db.String(255), db.ForeignKey('Customers.id'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

    