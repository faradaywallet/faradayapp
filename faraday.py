__author__ = 'Bren'

from flask import Flask, render_template, Response, request, redirect, url_for
import db_controller as DB

app = Flask('__main__')

@app.route('/')
def index():
    print('Opening index')
    # if request.method == 'POST':
    #     if request.form['submit'] == 'RegistrationRedirect':
    #         # return redirect(url_for('register'))
    #         return render_template('register.html')

    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    print('Opening registration page')
    if request.method == 'POST':
        print('Test')
        name = request.form['username']
        print(name)
    return render_template('register.html')


if __name__ == '__main__':
    app.run()

