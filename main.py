from flask import Flask,render_template, request
# from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
app.config['SECRET_KEY']='MAD1_PROJECT'
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
# db = SQLAlchemy(app)


@app.route('/')
def hello():
    return render_template('sample.html')