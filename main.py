from flask import Flask,render_template, request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired
import sqlite3
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
app = Flask(__name__)
app.config['SECRET_KEY']='MAD1_PROJECT'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///adminDB.db'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# login_manager=LoginManager()
# login_manager.init_app(app)
# login_manager.login_view='login'
# @login_manager.user_loader
# def load_admin(admin_id):
#      return Admin.query.get(int(admin_id))
conn= sqlite3.connect('admin.db',check_same_thread=False)
cursor=conn.cursor()    

#Inserting a new user in the admin_database




# class Admin(db.Model, UserMixin):
#     __tablename__='Admin'
#     admin_id = db.Column(db.Integer, primary_key=True, nullable=False)
#     admin_username=db.Column(db.String(50))
#     password_hash=db.Column(db.String(50))

#     @property
#     def password(self):
#         raise AttributeError('Password is not a readable attribute!')
	    
#     @password.setter
#     def password(self,password):
#         self.password_hash=generate_password_hash(password)
#     def verify_password(self,password):
# 	    return check_password_hash(self.password_hash,password)

class AdminForm(FlaskForm):

    admin_username = StringField('username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Login")

@app.route('/admin-login',methods=['GET','POST'])
def adminLogin():
    form=AdminForm()
    admin_username=None
    if(form.validate_on_submit()): 
         admin_username=form.admin_username.data
         admin_password=form.password.data
         
         db_password = cursor.execute("select password from adminLogin").fetchone()[0]
         #return render_template('new.html', name = db_password)
        #  hash_password=generate_password_hash(password,"sha256")
        #  if(Admin.verify_password(password)):
        #       flash('Login Successful')
        #     #   return render_template('<h1>Hello {{ admin_username }}<h1>')
        #  else:
        #       flash('Login Unsuccessful')
        #     #   return render_template('<h1>Not admin {{ admin_username }}<h1>')
        #  res_username = cursor.execute('select username from adminLogin')
        #  res_pwd = cursor.execute('select password from adminLogin')
         if(str(admin_password) == str(db_password)):
            return render_template('new.html', name=db_password)
        #  if admin_username==cursor.execute('select username from adminLogin').fetchall()[0][0]:
        #     return render_template('new.html')
        #  password_hash=generate_password_hash(password1)
        #
        #  return print("hqll")
        #  if(admin_username==res_username.fetchall()):
        #     return 1
         
    # admin_username=''
    # admin_list=Admin.query.all()
    return render_template('admin_login.html',form = form, name=admin_username)
