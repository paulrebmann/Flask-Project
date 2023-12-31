from app import db

#Customer table
class Customer(db.Model):
    __tablename__ = 'Customer'

    Customer_ID = db.Column(db.Integer, primary_key=True)
    Customer_First_Name = db.Column(db.String(50))
    Customer_Last_Name = db.Column(db.String(50))
    Age = db.Column(db.Integer)
    Country = db.Column(db.String(50))

#Order table
class Order(db.Model):
    __tablename__ = 'Order'

    Order_Id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date)
    Customer_ID = db.Column(db.Integer, db.ForeignKey('Customer.Customer_ID'), nullable=False)
    Price = db.Column(db.Float)
    Chair = db.Column(db.Integer)
    Stool = db.Column(db.Integer)
    Table = db.Column(db.Integer)
    Cabinet = db.Column(db.Integer)
    Dresser = db.Column(db.Integer)
    Couch = db.Column(db.Integer)
    Bed = db.Column(db.Integer)
    Shelf = db.Column(db.Integer)
