import datetime
from mongodb import MongoDBHelper
from flask import Flask, render_template, request, session
import hashlib

web_app = Flask("fateh app")
web_app.secret_key = 'fateh-key-1'  # Set your secret key here

@web_app.route("/")
def index():
    return render_template('index.html')

@web_app.route("/register")
def register():
    return render_template('register.html')

@web_app.route("/kada")
def kada():
    return render_template('kada.html')

@web_app.route("/kirpan")
def kirpan():
    return render_template('kirpan.html')

@web_app.route("/rumala")
def rumala_sahib():
    return render_template('rumala.html')

@web_app.route("/hanging")
def car_hanging():
    return render_template('hanging.html')

@web_app.route("/kanga")
def kanga():
    return render_template('kanga.html')

@web_app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@web_app.route("/register-customer", methods=['POST'])
def register_customer():
    customer_data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'phone': request.form['phone'],
        'password': hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest(),
        'createdOn': datetime.datetime.today()
    }

    print(customer_data)
    db = MongoDBHelper(collection="registered")
    result = db.insert(customer_data)
    customer_id = result.inserted_id
    session['phone'] = customer_data['phone']
    return render_template('index.html')

@web_app.route("/login-customer", methods=['POST'])
def login_customer():
    customer_login_data = {
        'email': request.form['email'],
        'password': request.form['password']
                     }

    print(customer_login_data)
    db = MongoDBHelper(collection="registered")
    documents = list(db.fetch(customer_login_data))
    print(documents, type(documents))
    if len(documents) == 1:
        session['customer_email']=documents[0]['email']
        # session['customer_id'] = str(documents[0]['_id'])
        # session['customer_name'] = documents[0]['name']
        session['password'] = documents[0]['password']
        # print(vars(session))
        session['customer_email'] = customer_login_data['email']
        return render_template('rumala.html')
    else:
        return render_template('alert.html')

@web_app.route("/order-rumala", methods=['POST'])
def order():
    rumala_sahib = {
        'customer_email': session.get('customer_email'),
        'item_quantity': request.form['quantity'],
        'item_price':request.form['price'],
        'product_code': request.form['code'],
        'order_time': datetime.datetime.today()

    }

    print(rumala_sahib)
    db = MongoDBHelper(collection="orders")
    result = db.insert(rumala_sahib)
    return render_template('rumala.html')

def main():
    web_app.run(port=5000)

if __name__ == "__main__":
    main()
