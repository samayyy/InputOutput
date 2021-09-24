from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from mysql.connector import connection
from flask import Flask
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
#from forms import ContactForm

import warnings
warnings.filterwarnings("ignore")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
app = Flask(__name__)
bcrypt = Bcrypt(app)
import mysql.connector



app.secret_key = 'miniproject'


app.config['MYSQL_HOST'] = 'sql6.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql6439270'
app.config['MYSQL_PASSWORD'] = 'v6nSCFAC8T'
app.config['MYSQL_DB'] = 'sql6439270'
app.config['MYSQL_CURSORCLASS']='DictCursor'
#mysql = mysql.connector.connect(
#  host="sql6.freesqldatabase.com",
#  user="sql6439270",
#  password="v6nSCFAC8T",
#  database="sql6439270"
#)

mysql = MySQL(app)
#mycursor = mysql.cursor()
#mycursor.execute("CREATE TABLE customers (username VARCHAR(255), password VARCHAR(255), email VARCHAR(255))")

# Execute the query

#mycursor.execute()
#for x in mycursor:
#    print(x)


@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:

        email= request.form['email']
        password1 = request.form['password']
        print(password1)
        print(type(password1))
        #bcrypt.check_password_hash(password1, )
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result= cursor.execute('SELECT * FROM customers WHERE email = %s ', [email])
        if result>0:

            account = cursor.fetchone()
            print(account)
            password=account['password']
            print(password)
            print(type(password))
            print(check_password_hash(account['password'],request.form['password']))
            if check_password_hash(account['password'],request.form['password']):
                session['loggedin'] = True
                #session['id'] = account['id']
                session['username'] = account['username']
                return redirect(url_for('index'))
            else:
                msg = 'Incorrect Email/password!'
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=''

    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form and 'mobile' in request.form:

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        print(password)
        print(type(password))
        password_hash = generate_password_hash(request.form['password'])
        print(password_hash)
        print(type(password))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customers WHERE email = %s', (email,))
        account1 = cursor.fetchone()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customers WHERE username = %s', (username,))
        account2 = cursor.fetchone()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customers WHERE mobile = %s', (mobile,))
        account3 = cursor.fetchone()
        if account1:
            msg = 'Account on this email already exists!'
        elif account2:
            msg = 'Username is taken by any other user! Please choose a different one'
        elif account3:
            msg = 'Account on this mobile number already exist'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif  (len(username)<5) or (len(username)>10):
            msg = " Username length must be between 5 to 10 characters!"
        elif  (len(password)<6) or (len(password)>18):
            msg = " Password length must be between 6 to 18 characters!"
        elif not (len(mobile)==10):
            msg=" Not a valid Mobile Number (Enter 10 digit Mobile Number)"
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:

            cursor.execute('INSERT INTO customers VALUES (%s, %s, %s, %s)', (username, email, password_hash, mobile,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':

        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)

@app.route('/index')
def index():

    if 'loggedin' in session:

        return render_template('index.html', username=session['username'])

    return redirect(url_for('login'))

@app.route('/rennaissancetechnology/logout')
def logout():

   session.pop('loggedin', None)
   #session.pop('id', None)
   session.pop('username', None)

   return redirect(url_for('login'))
if __name__ == '__main__':
   app.run(debug=True)
