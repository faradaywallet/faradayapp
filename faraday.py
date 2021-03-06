__author__ = 'Bren'

from flask import Flask, render_template, Response, request, redirect, url_for, session
from db_controller import FaradayDB
from encrypt import Encrypt
from logger import Logger
from flask_sslify import SSLify
from werkzeug.serving import make_ssl_devcert
import base64, os, datetime, json

make_ssl_devcert('key')

app = Flask('__main__')
sslify = SSLify(app)
db = FaradayDB('localhost', 3310, 'root', 'cybr200', 'faraday') # TODO: Find out a way to hide database connection information
Logger = Logger()
Encrypt = Encrypt()
timestamp = datetime.datetime.now()
app.secret_key = os.urandom(24)

@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

@app.route('/', methods=['POST', 'GET'])
def index():
    print('Opening index/login')

    # Wipe session on opening
    session.pop('username', None)

    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        # TODO: Session validation, password shouldn't be stored anywhere
        try:
            symmetric_box = base64.b64decode(db.get_symmetric_box(user))
            salt = base64.b64decode(db.get_salt(user))
        except:
            print('SERVER/LOG: Username not found')
            return redirect("/")

        if Encrypt.decrypt_key(symmetric_box, pwd.encode(), salt) == -1:
            print('SERVER/LOG: Incorrect password')
            return redirect("/")

        print('SERVER/LOG: Login OK')
        session['symkey'] = Encrypt.decrypt_key(symmetric_box, pwd.encode(), salt)
        session['username'] = request.form['username']
        Logger.log("Login from " + session['username'])

        return redirect('/cards')

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

        values = (user, email, create_date, base64.b64encode(salt), base64.b64encode(session_key), base64.b64encode(sym_key_box))
        db.insert_user(values)
    return render_template('register.html')

@app.route('/cards', methods=['POST', 'GET'])
def cards():
    print('SERVER/LOG: Opening cards page')
    user_cards = []
    # TODO: Decryption logic for cards

    if request.method == 'POST':
        print("SERVER/LOG: Headers:\n", request.headers)
        print("SERVER/LOG: Data:\n", request.data)
        try:
            print("SERVER/LOG: Form:\n", request.form['cardId'])
            db.delete_card(request.form['cardId'])
            return redirect("/cards")
        except:
            print("SERVER/FAIL: Unable to edit/delete card:\n")

    try:
        if 'username' in session:
            print('SERVER/LOG: Logged in as', session['username'])
            try:
                # payloads = db.get_payloads(session['username'])
                id_payloads = db.get_id_payload(session['username'])
                print(id_payloads)
                for payload in id_payloads:
                    user_cards.append((json.loads(Encrypt.decrypt_payload(session['symkey'], base64.b64decode(payload["payload"]))), payload["id"]))
            except:
                print('SERVER/FAIL: No cards found for', session['username'])
        else:
            return redirect("/")
    except:
        return redirect("/")
    return render_template('cards.html', user_cards=user_cards)

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    print('SERVER/LOG: Opening profile page')

    # TODO: User authentication for accessing user profile
    try:
        if 'username' in session:
            email = db.get_email(session['username'])
        else:
            return redirect("/")
    except:
        return redirect("/")

    return render_template('profile.html', username=session['username'], email=email)

@app.route('/add', methods=['POST', 'GET'])
def add():
    print('SERVER/LOG: Opening add cards page')
    if request.method == 'POST':
        # print('SERVER/LOG: Credit card added by user at', str(timestamp))
        Logger.log("Credit card card added by " + session['username'])
        payload = {'cardname': request.form['cardname'],
                    'ccnum': request.form['card'],
                   'expdate': request.form['expdate'],
                   'cvc': request.form['cvc'],
                   'notes': request.form['notes']}
        # TODO: Server side logic to encrypt credit card and notes using user key
        json_payload_string = json.dumps(payload)
        encrypted_payload = Encrypt.encrypt_payload(session['symkey'], json_payload_string.encode())
        db.insert_credit(values=(session['username'], base64.b64encode(encrypted_payload)))
        return redirect(url_for('cards'))
    return render_template('add.html')

if __name__ == '__main__':
    app.run(port=80, debug=False, ssl_context=('key.crt', 'key.key'))
