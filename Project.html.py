# html for task 1: index
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Orders</title>
</head>
<body>
    <h1>Customers</h1>
    <ul>
        {% for customer in customers %}
            <li>{{ customer.name }} {{ customer.last_name }} - <a href="{{ url_for('add_order', customer_id=customer.id) }}">Add Order</a></li>
        {% endfor %}
    </ul>
    <a href="{{ url_for('add_customer') }}">Add New Customer</a>
</body>
</html>


# html for task 1: add customer

<!-- templates/add_customer.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Customer</title>
</head>
<body>
    <h1>Add Customer</h1>
    <form method="POST" action="">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
        <br>
        <label for="last_name">Last Name:</label>
        <input type="text" id="last_name" name="last_name" required>
        <br>
        <label for="age">Age:</label>
        <input type="number" id="age" name="age" required>
        <br>
        <label for="country">Country:</label>
        <input type="text" id="country" name="country" required>
        <br>
        <button type="submit">Submit</button>
    </form>
    <br>
    <a href="{{ url_for('index') }}">Back to Customers</a>
</body>
</html>


# html for task1: add order

<!-- templates/add_order.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Order</title>
</head>
<body>
    <h1>Add Order for Customer {{ customer_id }}</h1>
    <form method="POST" action="">
        <label for="price">Price:</label>
        <input type="text" id="price" name="price" required>
        <br>
        <label for="furniture">Furniture:</label>
        <input type="text" id="furniture" name="furniture" required>
        <br>
        <button type="submit">Submit</button>
    </form>
    <br>
    <a href="{{ url_for('index') }}">Back to Customers</a>
</body>
</html>


# html for task2: edit customer
<!-- templates/edit_customer.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit Customer</title>
</head>
<body>
    <h1>Edit Customer</h1>
    <form method="POST" action="">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" value="{{ customer.name }}" required>
        <br>
        <label for="last_name">Last Name:</label>
        <input type="text" id="last_name" name="last_name" value="{{ customer.last_name }}" required>
        <br>
        <label for="age">Age:</label>
        <input type="number" id="age" name="age" value="{{ customer.age }}" required>
        <br>
        <label for="country">Country:</label>
        <input type="text" id="country" name="country" value="{{ customer.country }}" required>
        <br>
        <button type="submit">Save Changes</button>
    </form>
    <br>
    <a href="{{ url_for('index') }}">Back to Customers</a>
</body>
</html>


# html for task2: edit order
<!-- templates/edit_order.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit Order</title>
</head>
<body>
    <h1>Edit Order</h1>
    <form method="POST" action="">
        <label for="price">Price:</label>
        <input type="text" id="price" name="price" value="{{ order.price }}" required>
        <br>
        <label for="furniture">Furniture:</label>
        <input type="text" id="furniture" name="furniture" value="{{ order.furniture }}" required>
        <br>
        <button type="submit">Save Changes</button>
    </form>
    <br>
    <a href="{{ url_for('index') }}">Back to Customers</a>
</body>
</html>


# html for task 3: visualization
<!-- templates/visualization.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <img src="data:image/png;base64,{{ img_base64 }}" alt="{{ title }} Chart">
    <br>
    <a href="{{ url_for('index') }}">Back to Customers</a>
</body>
</html>


# html for task4: customers with most orders
<!-- templates/top_orders.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Top Customers by Orders</title>
</head>
<body>
    <h1>Top Customers by Orders</h1>
    <ul>
        {% for customer in customers %}
            <li>{{ customer.name }} {{ customer.last_name }} - Orders: {{ len(customer.orders) }}</li>
        {% endfor %}
    </ul>
    <br>
    <a href="{{ url_for('index') }}">Back to Customers</a>
</body>
</html>


# html for task4: top spenders
<!-- templates/top_spenders.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Top Spenders</title>
</head>
<body>
    <h1>Top Spenders</h1>
    <ul>
        {% for customer in customers %}
            <li>{{ customer.name }} {{ customer.last_name }} - Total Spending: ${{ "{:.2f}".format(sum(order.price for order in customer.orders)) }}</li>
        {% endfor %}
    </ul>
    <br>
    <a href="{{ url_for('index') }}">Back to Customers</a>
</body>
</html>
