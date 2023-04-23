
from flask import Flask, render_template, request, flash, session, redirect, flash, url_for
from flask_login import login_user,login_required, logout_user,  LoginManager
from flask_bcrypt import Bcrypt
from database import Venue,Show, Admin,app,db,user_hist_rating
from forms import venueForms, AdminForm, ShowForm
import sqlalchemy
from werkzeug.exceptions import InternalServerError

adminlogin_manager = LoginManager()
adminlogin_manager.init_app(app)
adminlogin_manager.login_view = 'adminLogin'
@adminlogin_manager.user_loader
def load_user(admin_id):
    return Admin.query.filter_by(id=int(admin_id)).first()



@app.route('/admin-login', methods=['GET', 'POST'])
def adminLogin():
    form = AdminForm()
    admin_username = None
    admin_password = None
    if (request.method == "POST"):
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



@app.route('/admin-logout/', methods=['GET', 'POST'])
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/addvenue", methods=['GET', 'POST'])
@login_required
def addvenue():
    form = venueForms()
    name = None
    venues = Venue.query.order_by(Venue.date_added)
    if (request.method == "POST"):
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
        finally:
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
            return render_template('displayAllShows.html', form=form, Shows=Shows , name=show_name)
        form.show_name.data = ''
        form.rating.data = ''
        form.tags.data = ''
        form.ticket_price.data = ''  
        Shows = Show.query.order_by(Show.date_added)
    return render_template('displayAllShows.html', form=form, Shows=Shows , name=show_name)

@app.route('/viewshows/',methods=['GET','POST'])
@login_required
def viewshows():
    shows = Show.query.order_by(Show.date_added)
    return render_template('viewShows.html',shows=shows)



@app.route('/updateshow/<int:id>',methods=['POST','GET'])
@login_required
def updateshow(id):
    form = ShowForm()
    show_to_update = Show.query.get_or_404(id)
    if (request.method == 'POST'):
        show_to_update.name = form.show_name.data
        show_to_update.timing =form.timing.data
        show_to_update.tags = form.tags.data
        show_to_update.ticket_price = form.ticket_price.data
        show_to_update.available_seats=form.available_seats.data
        try:
            show_to_update.rating = form.rating.data
            db.session.commit()
            shows = Show.query.order_by(Show.date_added)
            return render_template('viewShows.html',shows=shows)
        except:
            db.session.rollback()
            flash('Error')
            return render_template("updateshow.html", form=form, show_to_update = show_to_update)
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
            return redirect(url_for('viewshows'))
    except:
        flash('Venue not deleted')
        shows = show.query.order_by(show.date_added)
        return render_template('displayAllShows.html', form=form, shows=shows, name=name)
    
@app.route('/user_bookings',methods=['POST','GET'])
@login_required
def user_bookings():
    user_bookings = user_hist_rating.query.all()
    forVenue=Venue.query.all()
    forShow=Show.query.all()
    for booking in user_bookings:
        venue_id = booking.venue_id
        show_id = booking.show_id
        forVenue.append(Venue.query.filter_by(id=venue_id))
        forShow.append(Show.query.filter_by(id=show_id))
        shows = user_hist_rating.query.filter_by(venue_id=venue_id,show_id=show_id)
        ratings=[]
        for show in shows: 
            ratings.append(show.user_rating) 
        booking.rating = sum(ratings)/len(ratings)
    return render_template('admin-user_bookings.html',user_bookings=user_bookings,forVenue=forVenue,forShow=forShow)