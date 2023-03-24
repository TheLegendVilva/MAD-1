from flask import Flask, render_template, request, flash,session,redirect,flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, ValidationError, IntegerField
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired
import sqlite3
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
app = Flask(__name__)
app.config['SECRET_KEY'] = 'MAD1_PROJECT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///venueDB.db'



db = SQLAlchemy(app)
migrate = Migrate(app, db)

conn = sqlite3.connect('admin.db', check_same_thread=False)
cursor = conn.cursor()

class AdminForm(FlaskForm, UserMixin):
    admin_username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")
 
class UserForm(FlaskForm, UserMixin):
    user_username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")
    register = SubmitField("Register")
# 

class Venue(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	place = db.Column(db.String(255), nullable=False)
	location = db.Column(db.String(255), nullable=False)
	Capacity = db.Column(db.Integer, nullable=False)
	date_added = db.Column(db.DateTime, default=datetime.utcnow())
        
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255),nullable=False)
    password = db.Column(db.String(8),nullable = False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
        
class venueForms(FlaskForm):
    name = StringField('Add The Name Of The Venue:', validators=[DataRequired()])
    place = StringField('Add The Place Of The Venue:', validators=[DataRequired()])
    location = StringField('Add The Location Of The Venue:', validators=[DataRequired()])
    capacity = IntegerField('Add The Capacity Of The Venue:', validators=[DataRequired()])
    submit = SubmitField("Save")

#Flask_login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view= 'adminLogin'



@login_manager.user_loader
def load_user():
    query = 'select password from adminLogin'
    res = cursor.execute(query).fetchone()[0]
    return res

# @app.route('/login',methods = ['GET','POST'])
# def login():
#     form = AdminForm()
#     return render_template('admin_login.html',form=form)

@app.route('/admin-dashboard',methods = ['GET','POST'])
@login_required
def dashboard():
    form = AdminForm()
    return render_template('admin_dashboard.html',form=form)


#Login page of Admin
@app.route('/admin-login', methods=['GET', 'POST'])
def adminLogin():
    form = AdminForm()
    admin_username = None
    admin_password=None
    if (form.validate_on_submit()):
        admin_username = form.admin_username.data
        admin_password = form.password.data
        db_password = cursor.execute(
            "select password from adminLogin where username = '"+admin_username+"'").fetchone()
        if(db_password == None or db_password[0]!=admin_password):
            flash('Login Unsuccessful')
        elif(str(admin_password) == str(db_password[0])):
            return render_template('baseadmin.html', name=db_password)
    admin_username=''
    admin_password=''
    return render_template('admin_login.html', form=form, name=admin_username)

#create logout page
@app.route('/admin-logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash('You have logged out successfully!!')
    return redirect(url_for('adminLogin'))



@app.route("/add-venue",methods=['GET','POST'])
@login_required
def addvenue():
    form=venueForms()
    name=None
    if(form.validate_on_submit):
        name = form.name.data 
        place=form.place.data
        location=form.location.data
        Capacity=form.capacity.data
        if(name!=None and place!=None and location!=None and Capacity !=None):
            venue = Venue(name = name ,place=place,location=location,Capacity=Capacity)
            db.session.add(venue)
            db.session.commit()
            venues = Venue.query.order_by(Venue.date_added)
            flash('Venue added successfully!!')
            return render_template('addvenue.html',form = form, venues= venues,name=name)
        form.name.data=''
        form.place.data=''
        form.location.data=''
        form.capacity.data=''
        venues = Venue.query.order_by(Venue.date_added)
        
    return render_template('addvenue.html',form = form, venues= venues,name=name)

@app.route('/updatevenue/<int:id>',methods=['GET','POST'])
@login_required
def updatevenue(id):
    form = venueForms()
    venue_to_update = Venue.query.get_or_404(id)
    if(request.method == 'POST'):
        venue_to_update.name = request.form['name']
        venue_to_update.place = request.form['place']
        venue_to_update.location = request.form['location']
        venue_to_update.Capacity = request.form['capacity']
        try:
            db.session.commit()
            return render_template("updatevenue.html",form=form,venue_to_update=venue_to_update)
        except:
            flash('Error')
            return render_template("updatevenue.html",form=form,venue_to_update=venue_to_update)
    else:
        return render_template("updatevenue.html",form=form,venue_to_update=venue_to_update)

@app.route('/delete/<int:id>',methods=['GET','POST'])
def deletevenue(id):
    venue_to_delete = Venue.query.get_or_404(id)
    form = venueForms()
    name=None
    try:
        db.session.delete(venue_to_delete)
        db.session.commit()
        flash('Venue deleted')
        try:
            venues = Venue.query.order_by(Venue.date_added)
            venue= Venue.query.order_by(Venue.date_added).first()
            return render_template('addvenue.html',form = form, venues= venues,name=venue.name)
        except:
            return redirect('/addvenue')
    except:
        flash('Venue not deleted')
        venues = Venue.query.order_by(Venue.date_added)
        return render_template('addvenue.html',form = form, venues= venues,name=name)

# User page
@app.route('/user-login/',methods=['POST','GET'])
def user_login():
    form = UserForm()
    user_username = None
    user_password=None
    if (form.validate_on_submit()):
        user_username = form.user_username.data
        user_password = form.password.data
        # db_password = cursor.execute("select password from adminLogin where username = '"+admin_username+"'").fetchone()
        # db_password = select(user_password).where(Users.c.password == user_password)
        if(user_password == '123'):
            flash('Login Successful')
            return render_template('user_login.html', form=form, name=user_username)
        else:
            flash('Login Unsuccessful')
    admin_username=''
    admin_password=''
    return render_template('user_login.html', form=form, name=user_username)

@app.route('/register_user/',methods=['GET','POST'])
def register_user():
    form=UserForm()
    user_username=None
    if(form.validate_on_submit()):
        user_username = form.user_username.data 
        password = form.password.data
        new_user = Users(user_name=user_username,password=password)
        db.session.add(new_user)
        db.session.commit()
        users = Users.query.order_by(Users.date_added)
        flash('Userregistered successfully!!')
        return render_template('user_register.html',form = form, users= users,name=user_username)
    form.user_username.data=''
    users = Users.query.order_by(Users.date_added)
    return render_template('user_register.html',form = form, users= users,name=user_username)