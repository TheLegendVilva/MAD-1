from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField,DateTimeField, ValidationError, IntegerField,FloatField
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from database import Users

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
    rating = FloatField('Rating', validators=[DataRequired(), NumberRange(min=0, max=10)])
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
    
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Search")

class RatingForm(FlaskForm):
    rating = FloatField("Rating: ", validators=[DataRequired()])
    submit = SubmitField("Enter")