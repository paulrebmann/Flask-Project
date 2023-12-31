from flask import render_template
from app import app
from .models import Customer, db


#homepage (Indexpage)
@app.route('/')
@app.route('/index')
def index():
    customers = Customer.query.all()
    return render_template('index.html',customers=customers)

