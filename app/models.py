from app import db

#Customer table
class Customer(db.Model):
    __tablename__ = 'Customer'

    customer_id = db.Column(db.Integer, primary_key=True)
    customer_first_name = db.Column(db.String(50))
    customer_last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    country = db.Column(db.String(50))

def __repr__(self):
    return '<Customer {}>'.format(self.customer_id)


#Order table
class Order(db.Model):
    __tablename__ = 'Order'

    order_id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.customer_id'), nullable=False)
    price = db.Column(db.Float)
    chair = db.Column(db.Integer)
    stool = db.Column(db.Integer)
    table = db.Column(db.Integer)
    cabinet = db.Column(db.Integer)
    dresser = db.Column(db.Integer)
    couch = db.Column(db.Integer)
    bed = db.Column(db.Integer)
    shelf = db.Column(db.Integer)

def __repr__(self):
    return '<Order {}>'.format(self.order_id)
