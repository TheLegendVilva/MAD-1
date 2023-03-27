from flask import Flask, render_template, request, flash, session, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField,DateTimeField, ValidationError, IntegerField,FloatField
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired, InputRequired, Length
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
    shows = db.relationship('Show', backref = 'shows')
    Capacity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
# name can be accessed by venue.name and similarly place location can be accessed by venue.location , venue.place caused by backref

# A venue can have multiple shows
class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # foreign key that maps shows to venue
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    tags = db.Column(db.String(255))
    show_timing = db.Column(db.DateTime)
    ticket_price = db.Column(db.Integer,nullable=False)
    available_seats=db.Column(db.Integer,nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    # ven = db.relationship("Venue", back_populates="shows")

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(8), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())


class venueForms(FlaskForm):
    name = StringField('Add The Name Of The Venue:',validators=[DataRequired()])
    place = StringField('Add The Place Of The Venue:',validators=[DataRequired()])
    location = StringField('Add The Location Of The Venue:',validators=[DataRequired()])
    capacity = IntegerField('Add The Capacity Of The Venue:', validators=[DataRequired()])
    submit = SubmitField("Save")


class AdminForm(FlaskForm, UserMixin):
    admin_username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")

class ShowForm(FlaskForm):
    show_name = StringField('Show name', validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired()])
    timing = DateTimeField('Date & Time',validators=[DataRequired()])
    tags = StringField('Tags')
    ticket_price = IntegerField('Ticket Price', validators=[DataRequired()])
    available_seats = IntegerField('Available Seats:',validators=[DataRequired()])
    submit = SubmitField("Add show")



class RegisterUserForm(FlaskForm, UserMixin):
    user_username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=3, max=8)])
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = Users.query.filter_by(
            username=username.data).first()
        if (existing_user_username):
            raise ValidationError("This username already exists. Try another")


class LoginUserForm(FlaskForm, UserMixin):
    user_username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=8)])
    submit = SubmitField("Login")
    def validate_username(self, username):
        existing_user_username = Users.query.filter_by(
            username=username.data).first()
        if (existing_user_username):
            raise ValidationError("This username already exists. Try another")

class bookingForm(FlaskForm):
    number_of_seats = IntegerField('Number of seats: ',validators=[DataRequired()])
    submit=SubmitField("Confirm Booking") 
    

# Flask_login stuff
adminlogin_manager = LoginManager()
adminlogin_manager.init_app(app)
adminlogin_manager.login_view = 'adminLogin'

userlogin_manager = LoginManager()
userlogin_manager.init_app(app)
userlogin_manager.login_view = 'user_login'


@adminlogin_manager.user_loader
def load_user(admin_id):
    return Admin.query.filter_by(id=int(admin_id)).first()


@userlogin_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=int(user_id)).first()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

# Login page of Admin


@app.route('/admin-login', methods=['GET', 'POST'])
def adminLogin():
    form = AdminForm()
    admin_username = None
    admin_password = None
    if (form.validate_on_submit()):
        admin_username = form.admin_username.data
        admin_password = form.password.data
        if (admin_password != Admin.query.filter_by(username=admin_username).first().password):
            flash('Login Unsuccessful')
        else:
            pwd = Admin.query.filter_by(username=admin_username).first()
            login_user(pwd, remember=True)
            return render_template('admin_login.html', form=form, name=admin_username)
    admin_username = ''
    admin_password = ''
    return render_template('admin_login.html', form=form, name=admin_username)


@app.route('/admin-dashboard/', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

# create logout page


@app.route('/admin-logout/', methods=['GET', 'POST'])
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('adminLogin'))


@app.route("/addvenue", methods=['GET', 'POST'])
@login_required
def addvenue():
    form = venueForms()
    name = None
    if (form.validate_on_submit):
        name = form.name.data
        place = form.place.data
        location = form.location.data
        Capacity = form.capacity.data

        if (name != None and place != None and location != None and Capacity != None):
            # return render_template('hello.html')
            venue = Venue(name=name, place=place,
                          location=location, Capacity=Capacity)
            db.session.add(venue)
            db.session.commit()
            venues = Venue.query.order_by(Venue.date_added)
            flash('Venue added successfully!!')
            shows=Show.query.order_by(Show.date_added)
            return render_template('viewVenues.html', venues=venues,shows=shows)
            # return render_template('dummy.html')
        form.name.data = ''
        form.place.data = ''
        form.location.data = ''
        form.capacity.data = ''
        venues = Venue.query.order_by(Venue.date_added)
        return render_template('addvenue.html',form=form, venues=venues)

@app.route('/updatevenue/<int:id>', methods=['POST','GET'])
@login_required
def updatevenue(id):
    form = venueForms()
    venue_to_update = Venue.query.get_or_404(id)
    if (request.method == 'POST'):
        venue_to_update.name = request.form['name']
        venue_to_update.place = request.form['place']
        venue_to_update.location = request.form['location']
        venue_to_update.Capacity = request.form['capacity']
        try:
            db.session.commit()
            venues = Venue.query.order_by(Venue.date_added)
            return render_template('viewVenues.html',venues=venues)
        except:
            flash('Error')
            return render_template("updatevenue.html", form=form, venue_to_update=venue_to_update)
    else:
        # return render_template('dummy.html')
        return render_template("updatevenue.html", form=form, venue_to_update=venue_to_update)

@app.route('/viewvenue/',methods=['GET','POST'])
@login_required
def viewvenue():
    venues = Venue.query.order_by(Venue.date_added)
    shows = Show.query.order_by(Show.date_added)
    return render_template('viewVenues.html',venues=venues, shows=shows)

@app.route('/deletevenue/<int:id>', methods=['GET', 'POST'])
@login_required
def deletevenue(id):
    venue_to_delete = Venue.query.get_or_404(id)
    form = venueForms()
    name = None
    try:
        db.session.delete(venue_to_delete)
        db.session.commit()
        flash('Venue deleted')
        try:
            for show in Show.query.filter_by(venue_id=None):
                db.session.delete(show)
                db.session.commit()
            venues = Venue.query.order_by(Venue.date_added)
            shows = Show.query.order_by(Show.date_added)
            return render_template('viewVenues.html',venues=venues, shows=shows)
        except:
            return redirect('/addvenue')
    except:
        flash('Venue not deleted')
        venues = Venue.query.order_by(Venue.date_added)
        return render_template('addvenue.html', form=form, venues=venues, name=name)


@app.route('/shows/<int:id>',methods=['POST','GET'])
@login_required
def addshow(id):
    form = ShowForm()
    show_name=None
    if (form.validate_on_submit):
        show_name = form.show_name.data
        show = Show(venue_id = id, name = show_name,rating = form.rating.data,tags = form.tags.data,show_timing = form.timing.data,ticket_price = form.ticket_price.data,available_seats=form.available_seats.data)
        if(show_name!=None):
            db.session.add(show)
            db.session.commit()
            Shows = Show.query.order_by(Show.date_added)
            # return render_template('dummy.html',show_to_update = Shows)
            return render_template('displayAllShows.html', form=form, Shows=Shows , name=show_name)
        form.show_name.data = ''
        form.rating.data = ''
        # form.timing.data = ''
        form.tags.data = ''
        form.ticket_price.data = ''  
        Shows = Show.query.order_by(Show.date_added)
    return render_template('displayAllShows.html', form=form, Shows=Shows , name=show_name)

@app.route('/viewshows/',methods=['GET','POST'])
@login_required
def viewshows():
    shows = Show.query.order_by(Show.date_added)
    return render_template('viewShows.html',shows=shows)

# @app.route('/dummy')
# def dummy():
#     id=1
#     show_to_update = Show.query.get_or_404(id)
#     show_to_update.show_timing = '2007-10-29 22:30:20'
#     return render_template('dummy.html',show_to_update=show_to_update)

@app.route('/updateshow/<int:id>',methods=['POST','GET'])
@login_required
def updateshow(id):
    form = ShowForm()
    show_to_update = Show.query.get_or_404(id)
    if (request.method == 'POST'):
        show_to_update.name = request.form['show_name']
        show_to_update.rating = request.form['rating']
        show_to_update.timing = request.form['timing']
        show_to_update.tags = request.form['tags']
        show_to_update.ticket_price = request.form['ticket_price']
        try:
            db.session.commit()
            # return render_template('dummy.html')
            shows = Show.query.order_by(Show.date_added)
            return render_template('viewShows.html',shows=shows)
        except:
            flash('Error')
            # return render_template('dummy.html',show_to_update=show_to_update)
            return render_template("updateshow.html", form=form, show_to_update = show_to_update)
    else:
        # return render_template('dummy.html',show_to_update=show_to_update)
        return render_template("updateshow.html", form=form, show_to_update=show_to_update)


@app.route('/deleteshow/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteshow(id):
    show_to_delete = Show.query.get_or_404(id)
    form = venueForms()
    name = None
    try:
        db.session.delete(show_to_delete)
        db.session.commit()
        flash('Show deleted')
        try:
            shows = Venue.query.order_by(Show.date_added)
            show = Venue.query.order_by(Show.date_added).first()
            return render_template('displayAllShows.html', form=form, shows=shows, name=name)
        except:
            # return redirect(url_for('addshow',id=show_to_delete.id))
            return redirect(url_for('viewshows'))
    except:
        flash('Venue not deleted')
        shows = show.query.order_by(show.date_added)
        return render_template('displayAllShows.html', form=form, shows=shows, name=name)
    


# Actor = User
@app.route('/user-login/', methods=['POST', 'GET'])
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


@app.route('/register_user/', methods=['GET', 'POST'])
def register_user():
    form = RegisterUserForm()
    if (form.validate_on_submit()):
        user_username = form.user_username.data
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = Users(username=user_username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        users = Users.query.order_by(Users.date_added)
        flash('User registered successfully!!')
        return redirect(url_for('user_login'))
    return render_template('user_register.html', form=form)


@app.route('/user-dashboard/', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    venues = Venue.query.order_by(Venue.date_added)
    shows = Show.query.order_by(Show.date_added)
    return render_template('user_dashboard.html',venues=venues, shows=shows)


@app.route('/user-logout/', methods=['GET', 'POST'])
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))

@app.route('/user-booking/<int:venue_id>/<int:show_id>',methods=['GET','POST'])
@login_required
def booking(venue_id,show_id):
    form =bookingForm()
    venue_id=1
    show_id=1
    venue = Venue.query.get_or_404(venue_id)
    show = Show.query.get_or_404(show_id)
    if(form.validate_on_submit() and form.number_of_seats.data <= show.available_seats):
        # return render_template('dummy.html')
        flash('Booking Confirmed')
        show.available_seats = int(show.available_seats) - int(form.number_of_seats.data)
        db.session.commit()
        return render_template('ticket_confirmation.html',form=form, venue=venue, show=show)
    elif(form.validate_on_submit() and show.available_seats==0):
        flash('Show Houseful')
        return render_template('booking_show.html',show=show,venue=venue,form=form)
    elif(form.validate_on_submit() and show.available_seats<form.number_of_seats.data):
        flash('Enter valid number of seats to confirm booking')
        return render_template('booking_show.html',show=show,venue=venue,form=form)
    return render_template('booking_show.html',show=show,venue=venue,form=form)
