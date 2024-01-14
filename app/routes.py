# Task 2: edit, add, delete data
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.models import Customer, Order
from app import app, db



# routes.....
@app.route('/')
def index():
    customers = Customer.query.all()
    return render_template('index.html', customers=customers, title='Order/Costumer System')

@app.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['last_name']
        age = request.form['age']
        country = request.form['country']

        new_customer = Customer(customer_first_name=name, customer_last_name=last_name, age=age, country=country)
        db.session.add(new_customer)
        db.session.commit()


        return redirect(url_for('index'))

    return render_template('add_customer.html')

@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    if request.method == 'POST':
        customer.customer_first_name = request.form['name']
        customer.customer_last_name = request.form['last_name']
        customer.age = request.form['age']
        customer.country = request.form['country']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_customer.html', customer=customer)

@app.route('/delete_customer/<int:customer_id>', methods=['GET', 'POST'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    if request.method == 'POST':
        db.session.delete(customer)
        db.session.commit()
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/add_order/<int:customer_id>', methods=['GET', 'POST'])
def add_order(customer_id):
    if request.method == 'POST':
        price = request.form['price']
        chair = request.form['chair']
        stool = request.form['stool']
        table = request.form['table']
        cabinet = request.form['cabinet']
        dresser = request.form['dresser']
        couch = request.form['couch']
        bed = request.form['bed']
        shelf = request.form['shelf']

        new_order = Order(customer_id=customer_id, price=price, chair=chair, stool=stool, table=table, cabinet=cabinet,dresser=dresser,couch=couch,bed=bed,shelf=shelf)
        db.session.add(new_order)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_order.html', customer_id=customer_id)

@app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)

    if request.method == 'POST':
        order.price = request.form['price']
        order.chair = request.form['chair']
        order.stool = request.form['stool']
        order.table = request.form['table']
        order.cabinet = request.form['cabinet']
        order.dresser = request.form['dresser']
        order.couch = request.form['couch']
        order.bed = request.form['bed']
        order.shelf = request.form['shelf']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_order.html', order=order)

@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()

    return redirect(url_for('index'))



# Task 3a: visualize data
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import base64


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

    matplotlib.use('agg')
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
    chair_items = [order.chair for order in orders]
    table_items = [order.table for order in orders]

    matplotlib.use('agg')
    plt.scatter(chair_items, table_items)
    plt.xlabel('Table')
    plt.ylabel('Chair')
    plt.title('Table/Chair Relationship')
    plt.xticks(rotation=45, ha='right')

    # Save the plot to a BytesIO object
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    plt.close()

    # Convert the BytesIO object to base64 for embedding in HTML
    img_base64 = base64.b64encode(img_data.read()).decode('utf-8')

    return render_template('visualization.html', img_base64=img_base64, title='Relationship Chair Table')




#############################################################################
# task 3b: visualize patterns
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64


# ... routes ...
@app.route('/customer_order_relationship')
def customer_order_relationship():
    customers = Customer.query.all()

    # Extracting data for the scatter plot
    ages = [customer.age for customer in customers]
    order_prices = [order.price for customer in customers for order in customer.orders]

    # Scatter plot
    matplotlib.use('agg')
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



##############################################################
# task4: most orders and money spent
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64


# ...  routes ...
@app.route('/top_orders')
def top_orders():
    customers = Customer.query.all()

    # Find customers with the most orders
    customers_most_orders = sorted(customers, key=lambda x: len(x.orders), reverse=True)[:10]

    return render_template('top_order.html', customers=customers_most_orders)

@app.route('/top_spenders')
def top_spenders():
    customers = Customer.query.all()

    # Find customers who spent the most money
    customers_highest_spending = sorted(customers, key=lambda x: sum(order.price for order in x.orders), reverse=True)[:10]

    return render_template('top_spenders.html', customers=customers_highest_spending)



############################################################################
## task5: special_offer for the client
@app.route('/special_offer/<int:customer_id>')
def special_offer(customer_id):
    # Retrieve the customer and their order history
    customer = Customer.query.get_or_404(customer_id)
    total_items_purchased = sum([order.chair + order.stool + order.table + order.cabinet +
                                 order.dresser + order.couch + order.bed + order.shelf for order in customer.orders])

    # Define the threshold for the special offer
    threshold_items = 10  # Adjust this threshold as needed

    # Check if the customer qualifies for the special offer
    if total_items_purchased >= threshold_items:
        offer_message = f"Congratulations, {customer.customer_first_name}! You qualify for a special offer."

        # You can customize the offer message or perform additional actions here
    else:
        offer_message = f"Keep shopping, {customer.customer_first_name}! You are just {threshold_items - total_items_purchased} items away from a special offer."

    # For demonstration purposes, print the offer message to the console
    print(offer_message)

    # Render a simple HTML response (you can customize this based on your needs)
    return render_template('special_offer.html', offer_message=offer_message)


###########################################
    
#task6: recommendation engine (first install pip scikit-learn)
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


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