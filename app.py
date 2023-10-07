# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from werkzeug.utils import secure_filename 
import os
import io
from flask import Flask, render_template, request, redirect, session 
from flask_mysqldb import MySQL
import mysql.connector
from sqlalchemy import create_engine
import MySQLdb.cursors
import re
import mysql.connector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import sqlite3

app = Flask(__name__)


app.secret_key = 'a'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Pallavi37!'
app.config['MYSQL_DB'] = 'budget'

mysql= MySQL(app)


#HOME--PAGE
@app.route("/home")
def home():
    return render_template("base.html")

@app.route("/")
def add():
    return render_template("home.html")



#SIGN--UP--OR--REGISTER


@app.route("/signup")
def signup():
    return render_template("signup.html")



@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM register WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO register (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return render_template('login.html', msg=msg)
        

        
        
 
        
 #LOGIN--PAGE
    
@app.route("/signin")
def signin():
    return render_template("login.html")
        
@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    global expid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM register WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        print (account)
        
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[0]
           
            return redirect('/home')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)



       





#ADDING----DATA


@app.route("/add")
def adding():
    return render_template('add.html')

@app.route('/addexpense',methods=['GET', 'POST'])
def addexpense():
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    paymode = request.form['paymode']
    category = request.form['category']
    
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO expenses ( userid,date, expensename, amount, paymode, category) VALUES (%s,%s, %s, %s, %s, %s)', ( userid,date, expensename, amount, paymode, category))
    mysql.connection.commit()
    print(date + " " + expensename + " " + amount + " " + paymode + " " + category)
    return redirect("/display")

@app.route("/upload")
def uploading():
    return render_template('upload.html')

#upload csv

@app.route('/uploadexpense', methods=['POST','GET'])
def upload():
    userid=session['id']
    if 'csv_file' not in request.files:
        return redirect(request.url)
   
    file = request.files['csv_file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        try:
            cursor = mysql.connection.cursor()
            # Parse the CSV file
            csv_data = csv.reader(io.TextIOWrapper(file.stream, encoding='utf-8'))
            
            # Insert data into the MySQL table
            for row in csv_data:
                cursor.execute("INSERT INTO expenses (userid,date,expensename,amount,paymode,category) VALUES (%s,%s,%s, %s,%s,%s)", (userid,row[0], row[1], row[2],row[3],row[4]))

            mysql.connection.commit()
            cursor.close()

            return 'Data from the CSV file has been inserted into the MySQL table successfully.'
        except Exception as e:
            mysql.connection.rollback()
            return f'Error: {str(e)}'


#DISPLAY---graph 

@app.route("/display")
def display():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM expenses')
    expense = cursor.fetchall()
    
    return render_template('display.html' ,expense = expense)
                        



#delete---the--data

@app.route('/delete/<string:id>', methods = ['POST', 'GET' ])
def delete(id):
     cursor = mysql.connection.cursor()
     cursor.execute('DELETE FROM expenses WHERE  expenseid = {0}'.format(id))
     mysql.connection.commit()
     print('deleted successfully')    
     return redirect("/display")
 
    
#UPDATE---DATA

@app.route('/edit/<id>', methods = ['POST', 'GET' ])
def edit(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM expenses WHERE  expenseid = %s', (id,))
    row = cursor.fetchall()
   
    return render_template('edit.html', expenses = row)


@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':

        date = request.form['date']
        expensename = request.form['expensename']
        amount = request.form['amount']
        paymode = request.form['paymode']
        category = request.form['category']

        cursor = mysql.connection.cursor()
        cursor.execute('update expenses set date=%s,expensename=%s,amount=%s,paymode=%s,category=%s where expenseid=%s',(date,expensename,amount,paymode,category,id))
        mysql.connection.commit()
        return redirect('/display')
        
      

            
 
         
    
            
 #limit
@app.route("/limit" )
def limit():
    
    return render_template('limit.html')

@app.route("/limitnum" , methods = ['POST' ])
def limitnum():
     if request.method == "POST":
         income= request.form['income']
         limitt=request.form['limitt']
         cursor = mysql.connection.cursor()
         cursor.execute('INSERT INTO limits VALUES (%s, % s, % s) ',(userid,income,limitt))
         mysql.connection.commit()
         return redirect('/limitnum')
     
         
@app.route("/limitnum") 
def limitn():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM `limits` ORDER BY `limits`.`limitt` DESC LIMIT 1')

    x= cursor.fetchone()
    s = x[2]
    
    print(s)
    return render_template("limit.html" , y= s)

@app.route('/expense_chart')
def expense_chart():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT category, SUM(amount) as total_amount FROM expenses WHERE userid = %s GROUP BY category', (userid,))
    result = cursor.fetchall()

    categories = []
    total_amounts = []

    for row in result:
        categories.append(row[0])
        total_amounts.append(row[1])

    plt.figure(figsize=(10, 6))
    plt.bar(categories, total_amounts)
    plt.xlabel('Expense Categories')
    plt.ylabel('Total Amount ($)')
    plt.title('Expense Breakdown by Category')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the chart as an image (optional)
    plt.savefig('static/expense_chart.png')

    return render_template('expense_chart.html')

#log-out


@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')

             

if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = 'uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)