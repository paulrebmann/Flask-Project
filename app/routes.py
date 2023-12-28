from flask import render_template
from app import app

#homepage (Indexpage)
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')