__author__ = 'Bren'

from flask import Flask, render_template, Response, request, redirect, url_for, session
from db_controller import FaradayDB
import datetime
from encrypt import Encrypt

app = Flask('__main__')
db = FaradayDB('localhost', 3310, 'root', 'cybr200', 'faraday') # TODO: Find out a way to hide database connection information
Encrypt = Encrypt()
timestamp = datetime.datetime.now()

@app.route('/')
def index():
    print('Opening index/login')
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    print('SERVER/LOG: Opening registration page')
    if request.method == 'POST':
        user = request.form['username']
        email = request.form['email']
        pwd = request.form['password']
        create_date = str(timestamp)
        print('SERVER/LOG: Account created by ', user, ' at ', create_date)
        # TODO: Server side logic to salt and encrypt password

        salt = Encrypt.generate_salt()
        session_key = Encrypt.generate_session_key()
        sym_key_box = Encrypt.generate_key(pwd.encode(), salt)

        values = (user, email, create_date, str(salt), str(session_key), str(sym_key_box))
        db.insert_user(values)
    return render_template('register.html')

@app.route('/cards', methods=['POST', 'GET'])
def cards():
    print('SERVER/LOG: Opening cards page')
    # TODO: User authentication for accessing user cards
    # if authenticate():
    # db.test_select_credit()
    return render_template('cards.html')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    print('SERVER/LOG: Opening profile page')
    # TODO: User authentication for accessing user profile
    # if authenticate():
    return render_template('profile.html')

@app.route('/add', methods=['POST', 'GET'])
def add():
    print('SERVER/LOG: Opening add cards page')
    if request.method == 'POST':
        print('SERVER/LOG: Credit card added by user')
        ccnum = request.form['card']
        notes = request.form['notes']
        print(ccnum)
        print(notes)
        # TODO: Server side logic to encrypt credit card and notes using user key
        db.test_insert_credit(values=(ccnum, notes))
        return redirect(url_for('profile'))
    return render_template('add.html')

if __name__ == '__main__':
    app.run()

