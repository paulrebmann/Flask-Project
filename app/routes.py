# Task 2
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from app.models import Customer, Order
from app import app, db
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import base64


# Here are the routes
@app.route('/')
def index():
    customers = Customer.query.all()
    return render_template('index.html', customers=customers, title='Order/Costumer System')

# Show Orders
@app.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

# Add Coustomer
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

#Edit Customer
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

#Delete Customer
@app.route('/delete_customer/<int:customer_id>', methods=['GET', 'POST'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('index'))
    
    return redirect(url_for('index'))

#Add Order
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

#Edit Order
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


#Delete Order
@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)

    db.session.delete(order)
    db.session.commit()

    return redirect(url_for('index'))



# Task 3

# Where are the Customers from
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

    # Save the plot 
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    plt.close()

    img_base64 = base64.b64encode(img_data.read()).decode('utf-8')

    return render_template('visualization1.html', img_base64=img_base64, title='Customer Locations')


# most popular forniture
@app.route('/popular_furniture')
def popular_furniture():
    # choose Forniture
    selected_furniture = request.args.getlist('furniture_type')

    # data from db
    orders = Order.query.all()
    data = {furniture_type: [getattr(order, furniture_type) for order in orders] for furniture_type in selected_furniture}

    # create plot
    matplotlib.use('agg')
    plt.figure(figsize=(10, 6))
    for furniture_type, values in data.items():
        plt.scatter([furniture_type] * len(values), values, label=furniture_type)

    plt.xlabel('types of furniture')
    plt.ylabel('count')
    plt.title('Popular types of furniture')
    plt.legend()
    plt.xticks(rotation=45, ha='right')

    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    plt.close()

    img_base64 = base64.b64encode(img_data.read()).decode('utf-8')

    return render_template('visualization2.html', img_base64=img_base64, title='Furniture')




# task4
#Top Orders
@app.route('/top_orders')
def top_orders():
    customers = Customer.query.all()
    customers_most_orders = sorted(customers, key=lambda x: len(x.orders), reverse=True)[:10]
    return render_template('top_order.html', customers=customers_most_orders)

#Top Spends
@app.route('/top_spenders')
def top_spenders():
    customers = Customer.query.all()
    customers_highest_spending = sorted(customers, key=lambda x: sum(order.price for order in x.orders), reverse=True)[:10]

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
    #load Data from db
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

    # Train Alogrithmus
    reader = Reader(rating_scale=(0, 10))
    data = Dataset.load_from_df(pd.DataFrame(data, columns=['customer_id', 'furniture_type', 'quantity']), reader)
    trainset, testset = train_test_split(data, test_size=0.2)
    algo = KNNBasic()
    algo.fit(trainset)

    # get the Prediction
    current_customer_data = [(customer_id, 'chair', None),
                             (customer_id, 'stool', None),
                             (customer_id, 'table', None),
                             (customer_id, 'cabinet', None),
                             (customer_id, 'dresser', None),
                             (customer_id, 'couch', None),
                             (customer_id, 'bed', None),
                             (customer_id, 'shelf', None)]

    predictions = []
    for data_point in current_customer_data:
        prediction = algo.predict(data_point[0], data_point[1])
        predictions.append({'furniture_type': data_point[1], 'predicted_quantity': prediction.est})

    # Sortieren Sie die Vorhersagen nach der vorhergesagten Menge
    predictions.sort(key=lambda x: x['predicted_quantity'], reverse=True)

    return render_template('recommendations.html', predictions=predictions)
