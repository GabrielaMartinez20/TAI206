from flask import Flask,jsonify, render_template, request, url_for, flash, redirect #importaciones
from flask_mysqldb import MySQL 
import MySQLdb

app= Flask(__name__) 

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5010,debug=True)