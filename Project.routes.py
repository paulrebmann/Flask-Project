# Task 1: integrate
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    orders = db.relationship('Order', backref='customer', lazy=True, cascade='all, delete-orphan')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    furniture = db.Column(db.String(50), nullable=False)

# Create the tables
with app.app_context():
    db.create_all()


#####################################################################
    
# Task 2: edit, add, delete data
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# routes.....
@app.route('/')
def index():
    customers = Customer.query.all()
    return render_template('index.html', customers=customers)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['last_name']
        age = request.form['age']
        country = request.form['country']

        new_customer = Customer(name=name, last_name=last_name, age=age, country=country)
        db.session.add(new_customer)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_customer.html')

@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    if request.method == 'POST':
        customer.name = request.form['name']
        customer.last_name = request.form['last_name']
        customer.age = request.form['age']
        customer.country = request.form['country']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_customer.html', customer=customer)

@app.route('/delete_customer/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/add_order/<int:customer_id>', methods=['GET', 'POST'])
def add_order(customer_id):
    if request.method == 'POST':
        price = request.form['price']
        furniture = request.form['furniture']

        new_order = Order(customer_id=customer_id, price=price, furniture=furniture)
        db.session.add(new_order)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_order.html', customer_id=customer_id)

@app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)

    if request.method == 'POST':
        order.price = request.form['price']
        order.furniture = request.form['furniture']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_order.html', order=order)

@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


#########################################################################
    
# Task 3a: visualize data
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# where are the customers from?
@app.route('/customer_locations')
def customer_locations():
    customers = Customer.query.all()
    countries = [customer.country for customer in customers]

    country_counts = {}
    for country in countries:
        if country in country_counts:
            country_counts[country] += 1
        else:
            country_counts[country] = 1

    labels = list(country_counts.keys())
    values = list(country_counts.values())

    plt.bar(labels, values)
    plt.xlabel('Countries')
    plt.ylabel('Number of Customers')
    plt.title('Customer Locations')
    plt.xticks(rotation=45, ha='right')

    # Save the plot to a BytesIO object
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    plt.close()

    # Convert the BytesIO object to base64 for embedding in HTML
    img_base64 = base64.b64encode(img_data.read()).decode('utf-8')

    return render_template('visualization.html', img_base64=img_base64, title='Customer Locations')

# most popular forniture?

@app.route('/popular_furniture')
def popular_furniture():
    orders = Order.query.all()
    furniture_items = [order.furniture for order in orders]

    furniture_counts = {}
    for furniture in furniture_items:
        if furniture in furniture_counts:
            furniture_counts[furniture] += 1
        else:
            furniture_counts[furniture] = 1

    labels = list(furniture_counts.keys())
    values = list(furniture_counts.values())

    plt.bar(labels, values)
    plt.xlabel('Furniture')
    plt.ylabel('Number of Orders')
    plt.title('Popular Furniture')
    plt.xticks(rotation=45, ha='right')

    # Save the plot to a BytesIO object
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    plt.close()

    # Convert the BytesIO object to base64 for embedding in HTML
    img_base64 = base64.b64encode(img_data.read()).decode('utf-8')

    return render_template('visualization.html', img_base64=img_base64, title='Popular Furniture')

if __name__ == '__main__':
    app.run(debug=True)


#############################################################################
# task 3b: visualize patterns
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# ... routes ...
@app.route('/customer_order_relationship')
def customer_order_relationship():
    customers = Customer.query.all()

    # Extracting data for the scatter plot
    ages = [customer.age for customer in customers]
    order_prices = [order.price for customer in customers for order in customer.orders]

    # Scatter plot
    plt.scatter(ages, order_prices, alpha=0.5)
    plt.xlabel('Customer Age')
    plt.ylabel('Order Price')
    plt.title('Relationship Between Customer Age and Order Price')

    # Save the plot to a BytesIO object
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    plt.close()

    # Convert the BytesIO object to base64 for embedding in HTML
    img_base64 = base64.b64encode(img_data.read()).decode('utf-8')

    return render_template('visualization.html', img_base64=img_base64, title='Customer-Order Relationship')

if __name__ == '__main__':
    app.run(debug=True)

##############################################################
# task4: most orders and money spent
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# ...  routes ...
@app.route('/top_orders')
def top_orders():
    customers = Customer.query.all()

    # Find customers with the most orders
    customers_most_orders = sorted(customers, key=lambda x: len(x.orders), reverse=True)[:10]

    return render_template('top_orders.html', customers=customers_most_orders)

@app.route('/top_spenders')
def top_spenders():
    customers = Customer.query.all()

    # Find customers who spent the most money
    customers_highest_spending = sorted(customers, key=lambda x: sum(order.price for order in x.orders), reverse=True)[:10]

    return render_template('top_spenders.html', customers=customers_highest_spending)

if __name__ == '__main__':
    app.run(debug=True)

############################################################################
    
#task5: send a message to clients
# ... routes ...
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

@app.route('/send_birthday_message')
def send_birthday_message():
    today = datetime.now().date()
    customers_with_birthday = Customer.query.filter(
        (Customer.birthdate.day == today.day) & (Customer.birthdate.month == today.month)
    ).all()

    for customer in customers_with_birthday:
        send_birthday_greeting(customer)

    return "Birthday messages sent successfully!"

def send_birthday_greeting(customer):
    # Replace this with your actual code to send a birthday message
    # For example, you could use an email library or an API to send a message
    # Here, we'll just print a message to the console
    print(f"Happy Birthday, {customer.name} {customer.last_name}!")

if __name__ == '__main__':
    app.run(debug=True)

########################################################################
    
#task6: recommendation engine (first install pip scikit-learn)
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# ... routes ...
@app.route('/recommendations/<int:customer_id>')
def get_recommendations(customer_id):
    # Get the target customer and their purchased furniture
    target_customer = Customer.query.get_or_404(customer_id)
    target_furniture = [order.furniture for order in target_customer.orders]

    # Create a matrix of customer IDs and their purchased furniture
    data = []
    for customer in Customer.query.all():
        row = [1 if furniture in [order.furniture for order in customer.orders] else 0 for furniture in target_furniture]
        data.append(row)

    # Calculate cosine similarity between customers
    similarity_matrix = cosine_similarity(data, data)

    # Find the most similar customers
    similar_customers = np.argsort(similarity_matrix[customer_id - 1])[::-1][1:6]

    # Get the recommended furniture based on similar customers' purchases
    recommended_furniture = set()
    for similar_customer_id in similar_customers:
        similar_customer = Customer.query.get(similar_customer_id + 1)  # Adding 1 because customer IDs start from 1
        for order in similar_customer.orders:
            if order.furniture not in target_furniture:
                recommended_furniture.add(order.furniture)

    return jsonify(list(recommended_furniture))

if __name__ == '__main__':
    app.run(debug=True)
