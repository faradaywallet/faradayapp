__author__ = 'Bren'

from flask import Flask, render_template, Response, request, redirect, url_for, session
from db_controller import FaradayDB

app = Flask('__main__')
db = FaradayDB('localhost', 3310, 'root', 'cybr200', 'faraday')

@app.route('/')
def index():
    print('Opening index')
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    print('SERVER/LOG: Opening registration page')
    if request.method == 'POST':
        print('SERVER/LOG: Account created by user')
        name = request.form['username']
        email = request.form['email']
        pwd = request.form['password']
        print(name)
        print(email)
        print(pwd)
        # TODO: Server side logic to salt and encrypt password
        db.test_insert_user(values=(name, email))
    return render_template('register.html')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    print('SERVER/LOG: Opening profile page')
    # TODO: User authentication for accessing user profile
    # if authenticate():
    db.test_select_credit()
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

