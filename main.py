from flask import Flask, render_template, request, flash,session,redirect,flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, ValidationError, IntegerField
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired,InputRequired,Length
import sqlite3
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MAD1_PROJECT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///venueDB.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

class Venue(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	place = db.Column(db.String(255), nullable=False)
	location = db.Column(db.String(255), nullable=False)
	Capacity = db.Column(db.Integer, nullable=False)
	date_added = db.Column(db.DateTime, default=datetime.utcnow())
        
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255),nullable=False)
    password = db.Column(db.String(80),nullable = False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
        
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255),nullable=False)
    password = db.Column(db.String(8),nullable = False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

class venueForms(FlaskForm):
    name = StringField('Add The Name Of The Venue:', validators=[DataRequired()])
    place = StringField('Add The Place Of The Venue:', validators=[DataRequired()])
    location = StringField('Add The Location Of The Venue:', validators=[DataRequired()])
    capacity = IntegerField('Add The Capacity Of The Venue:', validators=[DataRequired()])
    submit = SubmitField("Save")

class AdminForm(FlaskForm, UserMixin):
    admin_username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")
 
class RegisterUserForm(FlaskForm, UserMixin):
    user_username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=3,max=8)])
    submit = SubmitField("Register")
    def validate_username(self,username):
        existing_user_username = Users.query.filter_by(username=username.data).first()
        if(existing_user_username):
            raise ValidationError("This username already exists. Try another")

class LoginUserForm(FlaskForm, UserMixin):
    user_username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=3,max=8)])
    submit = SubmitField("Login")
    def validate_username(self,username):
        existing_user_username = Users.query.filter_by(username=username.data).first()
        if(existing_user_username):
            raise ValidationError("This username already exists. Try another")

#Flask_login stuff
adminlogin_manager = LoginManager()
adminlogin_manager.init_app(app)
adminlogin_manager.login_view= 'adminLogin'

userlogin_manager = LoginManager()
userlogin_manager.init_app(app)
userlogin_manager.login_view= 'user_login'

@adminlogin_manager.user_loader
def load_user(admin_id):
    return Admin.query.filter_by(id = int(admin_id)).first()

@userlogin_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id = int(user_id)).first()


@app.route('/',methods = ['GET','POST'])
def home():
    return render_template('home.html')

#Login page of Admin
@app.route('/admin-login', methods=['GET', 'POST'])
def adminLogin():
    form = AdminForm()
    admin_username = None
    admin_password=None
    if (form.validate_on_submit()):
        admin_username = form.admin_username.data
        admin_password = form.password.data
        if(admin_password != Admin.query.filter_by(username = admin_username).first().password):
            flash('Login Unsuccessful')
        else:
            pwd = Admin.query.filter_by(username = admin_username).first()
            login_user(pwd,remember=True)
            return render_template('admin_login.html', form=form, name=admin_username)
    admin_username=''
    admin_password=''
    return render_template('admin_login.html', form=form, name=admin_username)

@app.route('/admin-dashboard/',methods = ['GET','POST'])
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

#create logout page
@app.route('/admin-logout/', methods=['GET','POST'])
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('adminLogin'))

@app.route("/addvenue",methods=['GET','POST'])
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
            # return render_template('hello.html')
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
    # return render_template('hello.html')

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
    form = LoginUserForm()
    if (form.validate_on_submit()):
        user_username = form.user_username.data
        user_password = form.password.data
        user = Users.query.filter_by(username=user_username).first()
        # if(user_password == '123'):
        #     flash('Login Successful')
        #     return render_template('user_login.html', form=form, name=user_username)
        if user:
            if bcrypt.check_password_hash(user.password, user_password):
                login_user(user)
                return redirect(url_for('user_dashboard'))
    return render_template('user_login.html', form=form)

@app.route('/register_user/',methods=['GET','POST'])
def register_user():
    form=RegisterUserForm()
    if(form.validate_on_submit()):
        user_username = form.user_username.data 
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = Users(username=user_username,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        users = Users.query.order_by(Users.date_added)
        flash('User registered successfully!!')
        return redirect(url_for('user_login'))
    return render_template('user_register.html',form = form)

@app.route('/user-dashboard/',methods = ['GET','POST'])
@login_required
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route('/user-logout/', methods=['GET','POST'])
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))