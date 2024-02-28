# Flask-Project University of Saarland

## Teammember
- Paul Rebmann
- Niklas Franzen
- Kenny Marcel Estrada Auz

## How do I open the app?
```
source venv/bin/activate
export FLASK_APP=flaskProject.py
flask run
```

## Task 2 (Edit the Data)
It is possible to create a customer in the app and to edit or delete it afterwards.
Orders can be placed via the customer, these can be viewed in a separate view and can be edited or deleted.

## Task 3 (Visualization)
There are 2 visualizations.
One shows the number of customers and where they come from in a box plot.
The second visualization shows a relation between the ordered quantity per customer in relation to where the customers come from.

## Task 4 (Rankings)
Two rankings are shown, one shows the top 10 people with the most orders and the other shows the top 10 people with the most spending.

## Task 5 (Marketing)
The marketing campaign works in such a way that every user receives a special offer from a certain order quantity. 
When the user has reached the quantity of 10 units, this can be called up in the 'Special Offer' field and there is a print output in the console.

## Task 6 (Recommendation)
There is also a recommendation that can be called up in the user field. It shows which products most closely match the purchase history of the respective customer.
A rating of 0 means that the piece of furniture does not match the customer's wishes or requirements at all, while a rating of 10 means that the piece of furniture matches the customer's wishes or requirements perfectly. Scores in between would then represent a gradually increasing match, with higher scores indicating a better match.
