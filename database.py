from flask import Flask
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine,MetaData, Table,CheckConstraint,Float,Column
from sqlalchemy.orm import sessionmaker
app = Flask(__name__)
app.config['SECRET_KEY'] = 'MAD1_PROJECT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///venueDB.db'
engine = create_engine('sqlite:///venueDB.db')
metadata = MetaData()
metadata.bin=engine
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
Session = sessionmaker(bind = engine)
session = Session()
class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    place = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    shows = db.relationship('Show', backref = 'shows')
    Capacity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow(),nullable=False)
# name can be accessed by venue.name and similarly place location can be accessed by venue.location , venue.place caused by backref

# A venue can have multiple shows
class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # foreign key that maps shows to venue
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    rating = Column(Float,CheckConstraint('rating >= 0 AND rating <= 10'))
    tags = db.Column(db.String(255),nullable=False)
    show_timing = db.Column(db.DateTime,nullable=False)
    ticket_price = db.Column(db.Integer,nullable=False)
    available_seats=db.Column(db.Integer,nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow(),nullable=False)
    # ven = db.relationship("Venue", back_populates="shows")

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow(),nullable=False)


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(8), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow(),nullable=False)

class user_hist_rating(db.Model):
    u_id = db.Column(db.Integer,nullable=False)
    show_id = db.Column(db.Integer,nullable=False)
    venue_id = db.Column(db.Integer,nullable=False)
    user_rating = db.Column(db.Float,default=0.0,nullable=False)
    user_rating=Column(Float,CheckConstraint('user_rating >= 0 AND user_rating <= 10'))
    __mapper_args__ = {
        'primary_key':[u_id,show_id,venue_id]
    }
