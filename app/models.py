#Importing the 'db' instance from the 'app' module
from app import db

#Customer table definition
class Customer(db.Model):
    #Defining the table name in the database
    __tablename__ = 'Customer'

    # Columns in the 'Customer' table
    customer_id = db.Column(db.Integer, primary_key=True) #Primary key column
    customer_first_name = db.Column(db.String(50)) #String column for customer's first name
    customer_last_name = db.Column(db.String(50)) #String column for customer's last name
    age = db.Column(db.Integer) #Integer column for customer's age
    country = db.Column(db.String(50)) #String column for customer's country
    #Relationship with 'Order' table, defining a one-to-many relationship
    orders = db.relationship('Order',lazy=True, cascade='all, delete-orphan')

    #Representation method for easy debugging and logging
    def __repr__(self):
        return '<Customer {}>'.format(self.customer_id)


#Order table definition
class Order(db.Model):
    #Defining the table name in the database
    __tablename__ = 'Order'

    #Columns in the 'Order' table
    order_id = db.Column(db.Integer, primary_key=True) #Primary key column
    date = db.Column(db.Date) #Date column for the order date
    #customer_id column
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.customer_id', ondelete='CASCADE'), nullable=False)
    price = db.Column(db.Float) #Float column for the order price
    #Integer columns for various furniture items in the order
    chair = db.Column(db.Integer)
    stool = db.Column(db.Integer)
    table = db.Column(db.Integer)
    cabinet = db.Column(db.Integer)
    dresser = db.Column(db.Integer)
    couch = db.Column(db.Integer)
    bed = db.Column(db.Integer)
    shelf = db.Column(db.Integer)

    #Representation method for easy debugging and logging
    def __repr__(self):
        return '<Order {}>'.format(self.order_id)