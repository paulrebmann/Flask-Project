# Task 2
# Importing necessary modules and classes
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from app.models import Customer, Order  # Importing models from the 'app' package
from app import app, db  # Importing the Flask app instance, 'app', and the SQLAlchemy database instance, 'db'
import matplotlib.pyplot as plt  # Importing Matplotlib for data visualization
import matplotlib
from io import BytesIO
import base64


# Routes for the Flask application

# Index
@app.route('/')
def index():
    # Fetch all customers from the database
    customers = Customer.query.all()
    # Render the 'index.html' template with customer data
    return render_template('index.html', customers=customers, title='Order/Costumer System')


# Show Orders
@app.route('/orders')
def orders():
    # Fetch all orders from the database
    orders = Order.query.all()
    # Render the 'orders.html' template with order data
    return render_template('orders.html', orders=orders)


# Add Customer
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    # Check if the request method is POST, indicating a form submission
    if request.method == 'POST':
        # Retrieve form data submitted via POST request
        name = request.form['name']
        last_name = request.form['last_name']
        age = request.form['age']
        country = request.form['country']

        # Create a new Customer object with the submitted data
        new_customer = Customer(customer_first_name=name, customer_last_name=last_name, age=age, country=country)
        # Add the new customer to the database session
        db.session.add(new_customer)
        # Commit the changes to the database
        db.session.commit()

        # Redirect to the 'index' route after successfully adding the customer
        return redirect(url_for('index'))
    # If the request method is GET, render the 'add_customer.html' template
    return render_template('add_customer.html')


# Edit Customer
@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    # Fetch the customer with the specified ID from the database
    customer = Customer.query.get_or_404(customer_id)

    # Check if the request method is POST, indicating a form submission
    if request.method == 'POST':
        # Update customer information based on the submitted form data
        customer.customer_first_name = request.form['name']
        customer.customer_last_name = request.form['last_name']
        customer.age = request.form['age']
        customer.country = request.form['country']

        # Commit the changes to the database
        db.session.commit()
        # Redirect to the 'index' route after successfully editing the customer
        return redirect(url_for('index'))

    # If the request method is GET, render the 'edit_customer.html' template with customer data
    return render_template('edit_customer.html', customer=customer)


# Delete Customer
@app.route('/delete_customer/<int:customer_id>', methods=['GET', 'POST'])
def delete_customer(customer_id):
    # Fetch the customer with the specified ID from the database
    customer = Customer.query.get_or_404(customer_id)
    # Delete the customer from the database session
    db.session.delete(customer)
    # Commit the changes to the database
    db.session.commit()
    # Redirect to the 'index' route after successfully deleting the customer
    return redirect(url_for('index'))


# Add Order
@app.route('/add_order/<int:customer_id>', methods=['GET', 'POST'])
def add_order(customer_id):
    # Check if the request method is POST, indicating a form submission
    if request.method == 'POST':
        # Retrieve form data submitted via POST request
        price = request.form['price']
        chair = request.form['chair']
        stool = request.form['stool']
        table = request.form['table']
        cabinet = request.form['cabinet']
        dresser = request.form['dresser']
        couch = request.form['couch']
        bed = request.form['bed']
        shelf = request.form['shelf']

        # Create a new Order object with the submitted data
        new_order = Order(customer_id=customer_id, price=price, chair=chair, stool=stool, table=table, cabinet=cabinet,
                          dresser=dresser, couch=couch, bed=bed, shelf=shelf)
        # Add the new order to the database session
        db.session.add(new_order)
        # Commit the changes to the database
        db.session.commit()

        # Redirect to the 'index' route after successfully adding the order
        return redirect(url_for('index'))

    # If the request method is GET, render the 'add_order.html' template with customer ID
    return render_template('add_order.html', customer_id=customer_id)


# Edit Order
@app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    # Retrieve the Order object with the given order_id from the database
    order = Order.query.get_or_404(order_id)

    # Check if the request method is POST, indicating a form submission for editing
    if request.method == 'POST':
        # Update the order attributes with the form data submitted via POST request
        order.price = request.form['price']
        order.chair = request.form['chair']
        order.stool = request.form['stool']
        order.table = request.form['table']
        order.cabinet = request.form['cabinet']
        order.dresser = request.form['dresser']
        order.couch = request.form['couch']
        order.bed = request.form['bed']
        order.shelf = request.form['shelf']

        # Commit the changes to the database
        db.session.commit()
        # Redirect to the 'index' route after successfully editing the order
        return redirect(url_for('index'))

    # If the request method is GET, render the 'edit_order.html' template with the order data
    return render_template('edit_order.html', order=order)


# Delete Order
@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    # Retrieve the Order object with the given order_id from the database
    order = Order.query.get_or_404(order_id)

    # Delete the retrieved order from the database session
    db.session.delete(order)
    # Commit the changes to the database
    db.session.commit()

    # Redirect to the 'index' route after successfully deleting the order
    return redirect(url_for('index'))


# Task 3

# Where are the Customers from
@app.route('/customer_locations')
def customer_locations():
    # Retrieve all customers from the database
    customers = Customer.query.all()
    # Extract the countries from each customer
    countries = [customer.country for customer in customers]

    # Count the occurrences of each country
    country_counts = {}
    for country in countries:
        if country in country_counts:
            country_counts[country] += 1
        else:
            country_counts[country] = 1

    # Extract labels and values for plotting
    labels = list(country_counts.keys())
    values = list(country_counts.values())

    # Set up Matplotlib for plotting
    matplotlib.use('agg')
    plt.bar(labels, values)
    plt.xlabel('Countries')
    plt.ylabel('Number of Customers')
    plt.title('Customer Locations')
    plt.xticks(rotation=45, ha='right')

    # Save the plot as an image
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    plt.close()

    # Convert the image data to base64 for rendering in HTML
    img_base64 = base64.b64encode(img_data.read()).decode('utf-8')

    # Render the visualization1.html template with the base64-encoded image
    return render_template('visualization1.html', img_base64=img_base64, title='Customer Locations')


# most popular forniture
@app.route('/popular_furniture')
def popular_furniture():
    # Get the selected furniture types from the query parameters
    selected_furniture = request.args.getlist('furniture_type')

    # Retrieve orders and relevant columns (furniture types and customer's country) from the database
    orders = Order.query.join(Customer).add_columns(
        Order.chair, Order.stool, Order.table, Order.cabinet,
        Order.dresser, Order.couch, Order.bed, Order.shelf,
        Customer.country
    ).all()

    # Initialize a dictionary to store furniture count for each country
    order_data = {}
    furniture_types = ['chair', 'stool', 'table', 'cabinet', 'dresser', 'couch', 'bed', 'shelf']

    # Iterate through orders to calculate furniture counts and store in order_data
    for order in orders:
        furniture_count = sum(getattr(order, furniture_type) for furniture_type in furniture_types)
        country = order.country

        order_data[(furniture_count, country)] = order_data.get((furniture_count, country), 0) + 1

    # Extract x and y values for plotting
    x_values, y_values = zip(*order_data.keys())

    # Set up Matplotlib for scatter plot
    matplotlib.use('agg')
    plt.figure(figsize=(10, 6))
    plt.scatter(x_values, y_values, s=[order_data[(x, y)] * 10 for x, y in zip(x_values, y_values)], alpha=0.7)

    # Set labels and title for the scatter plot
    plt.xlabel('Number of Furniture')
    plt.ylabel('Country')
    plt.title('Relationship between Furniture and Customer Country')
    plt.xticks(rotation=45, ha='right')

    # Save the scatter plot as an image
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    plt.close()

    # Convert the image data to base64 for rendering in HTML
    img_base64 = base64.b64encode(img_data.read()).decode('utf-8')

    # Render the visualization2.html template with the base64-encoded image
    return render_template('visualization2.html', img_base64=img_base64, title='Customer Order Relationship')


# task4
# Top Orders
@app.route('/top_orders')
def top_orders():
    # Retrieve all customers from the database
    customers = Customer.query.all()
    # Sort customers based on the number of orders in descending order and select the top 10
    customers_most_orders = sorted(customers, key=lambda x: len(x.orders), reverse=True)[:10]
    # Render the 'top_order.html' template with the top customers
    return render_template('top_order.html', customers=customers_most_orders)


# Top Spends
@app.route('/top_spenders')
def top_spenders():
    # Retrieve all customers from the database
    customers = Customer.query.all()
    # Sort customers based on the total spending (sum of order prices) in descending order and select the top 10
    customers_highest_spending = sorted(customers, key=lambda x: sum(order.price for order in x.orders), reverse=True)[
                                 :10]

    # Render the 'top_spenders.html' template with the top spending customers
    return render_template('top_spenders.html', customers=customers_highest_spending)


# task5
# Special Offer
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


# Task6:
# Recommendation
from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import train_test_split
import pandas as pd


# The model utilizes the k-NN algorithm for Collaborative Filtering,
# predicting quantities of furniture items for a customer based on the ordering patterns of similar customers,
# thereby providing personalized recommendations.
@app.route('/recommendations/<int:customer_id>')
def get_recommendations(customer_id):
    # load Data from db
    orders = Order.query.all()

    # create a DataFrame for each forniture_type
    data = [(order.customer_id, 'chair', order.chair) for order in orders] + \
           [(order.customer_id, 'stool', order.stool) for order in orders] + \
           [(order.customer_id, 'table', order.table) for order in orders] + \
           [(order.customer_id, 'cabinet', order.cabinet) for order in orders] + \
           [(order.customer_id, 'dresser', order.dresser) for order in orders] + \
           [(order.customer_id, 'couch', order.couch) for order in orders] + \
           [(order.customer_id, 'bed', order.bed) for order in orders] + \
           [(order.customer_id, 'shelf', order.shelf) for order in orders]

    # Train the collaborative filtering algorithm using the k-NN (k-Nearest Neighbors) approach
    reader = Reader(rating_scale=(0, 10))
    data = Dataset.load_from_df(pd.DataFrame(data, columns=['customer_id', 'furniture_type', 'quantity']), reader)
    trainset, testset = train_test_split(data, test_size=0.2)
    algo = KNNBasic()
    algo.fit(trainset)

    # Get predictions for the current customer's future purchases (predicted quantities)
    current_customer_data = [(customer_id, 'chair', None),
                             (customer_id, 'stool', None),
                             (customer_id, 'table', None),
                             (customer_id, 'cabinet', None),
                             (customer_id, 'dresser', None),
                             (customer_id, 'couch', None),
                             (customer_id, 'bed', None),
                             (customer_id, 'shelf', None)]

    # Generate predictions for each furniture_type based on the current customer's historical data
    predictions = []
    for data_point in current_customer_data:
        prediction = algo.predict(data_point[0], data_point[1])
        predictions.append({'furniture_type': data_point[1], 'predicted_quantity': prediction.est})

    # Sort the predictions based on the predicted_quantity in descending order
    predictions.sort(key=lambda x: x['predicted_quantity'], reverse=True)

    # Render a template ('recommendations.html') to display the sorted predictions
    return render_template('recommendations.html', predictions=predictions)