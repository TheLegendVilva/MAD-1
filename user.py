from flask import Flask, render_template, request, flash, session, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user,  LoginManager
from database import Venue,Show,Users, Admin,user_hist_rating,bcrypt
from forms import RegisterUserForm, LoginUserForm,bookingForm,SearchForm,RatingForm 
from database import Venue,Show,Users, Admin,user_hist_rating,app,db,session

userlogin_manager = LoginManager()
userlogin_manager.init_app(app)
userlogin_manager.login_view = 'user_login'


@userlogin_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=int(user_id)).first()


@app.route('/user-login/', methods=['POST', 'GET'])
def user_login():
    form = LoginUserForm()
    if (request.method == "POST"):
        user_username = form.user_username.data
        user_password = form.password.data
        user = Users.query.filter_by(username=user_username).first()
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
    venue = Venue.query.get_or_404(venue_id)
    show = Show.query.get_or_404(show_id)
    if(form.validate_on_submit() and form.number_of_seats.data <= show.available_seats):
        # return render_template('dummy.html')
        flash('Booking Confirmed')
        show.available_seats = int(show.available_seats) - int(form.number_of_seats.data)
        user_hist=user_hist_rating(u_id=current_user.id,show_id=show_id,venue_id=venue_id)
        db.session.add(user_hist)
        db.session.commit()
        return render_template('ticket_confirmation.html',form=form, venue=venue, show=show)
    elif(form.validate_on_submit() and show.available_seats==0):
        flash('Show Houseful')
        return render_template('booking_show.html',show=show,venue=venue,form=form)
    elif(form.validate_on_submit() and show.available_seats<form.number_of_seats.data):
        flash('Enter valid number of seats to confirm booking')
        return render_template('booking_show.html',show=show,venue=venue,form=form)
    return render_template('booking_show.html',show=show,venue=venue,form=form)


@app.route('/search',methods=['POST','GET'])
@login_required
def search():
    form = SearchForm()
    shows = Show.query
    venues = Venue.query
    searched=''
    if(form.validate_on_submit()):
        searched = form.searched.data
        shows=shows.filter(Show.name.like('%'+searched+'%')).all()
        venues = venues.filter(Venue.name.like('%' +searched+'%')).all()
        tags = Show.query.filter(Show.tags.like('%'+searched+'%')).all()
        rating=Show.query.filter(Show.rating == searched).all()
        return render_template("search.html", form = form, searched = searched, venues=venues, shows=shows,tags=tags,rating=rating)
    else:
        return render_template("search.html", form = form, searched = searched, venues=venues, shows=shows,tags=tags,rating=rating)

@app.route('/user_rating/<int:u_id>/<int:show_id>/<int:venue_id>',methods=['POST','GET'])
@login_required
def rating(u_id,show_id,venue_id):
    form=RatingForm()   
    show = user_hist_rating.query.get_or_404((u_id,show_id,venue_id))
    user_bookings = user_hist_rating.query.all()
    if(request.method=='POST'):
        show.user_rating = form.rating.data
        try:
            db.session.commit()
            history = user_hist_rating.query.filter_by(u_id=u_id)
            shows = Show.query.all()
            return render_template('user_history.html',history=history,shows=shows,form=form)
        except:
            db.session.rollback()
            flash('Rating cannot be negative or greater than 10')
            # return render_template('user_rating.html',show=show,user_bookings=user_bookings,form=form)
    return render_template('user_rating.html',show=show,user_bookings=user_bookings,form=form)



@app.context_processor
def user_navbar():
    form = SearchForm()
    return dict(form=form)

@app.route('/user-history/',methods=['GET','POST'])
@login_required
def user_history():
    form=RatingForm()
    u_id = current_user.id
    # return render_template("dummy.html" , uid=uid)
    history = user_hist_rating.query.filter_by(u_id=u_id)
    shows = Show.query.all()
    # return render_template(history=history)
    return render_template('user_history.html',history=history,shows=shows,form=form)