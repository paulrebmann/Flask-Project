from app import db

#Customer table
class Customer(db.Model):
    __tablename__ = 'Customer_DB'

    customerId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    last_Name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    country = db.Column(db.String(50))

#Order table
class Order(db.Model):
    __tablename__ = 'Order_DB'

    orderId = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    customerId = db.Column(db.Integer, db.ForeignKey('Customer_DB.CustomerId'))
    price = db.Column(db.Float)
    furniture = db.Column(db.String(50)) 

    customer = db.relationship('Customer', foreign_keys=[customerId])

def __repr__(self):
    return '<Customer {}>'.format(self.name)