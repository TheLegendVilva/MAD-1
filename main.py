from flask import Flask, render_template,jsonify
from flask_bcrypt import Bcrypt
from database import app,Venue,Show,Users,Admin,user_hist_rating
from user import user_login
from admin import adminLogin
from flask_migrate import Migrate
if __name__=="__main__":
    app.debug=True

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/venueDB/',methods=['GET'])
def get_venues():
    venues = Venue.query.all()
    venue_list = []
    for venue in venues:
        item = {'id': venue.id, 'name': venue.name, 'place': venue.place, 'location': venue.location, 'Capacity': venue.Capacity, 'date_added': venue.date_added}
        venue_list.append(item)
    return jsonify(venue_list)

@app.route('/showDB/',methods=['GET'])
def get_shows():
    shows = Show.query.all()
    show_list = []
    for show in shows:
        item = {'id': show.id, 'venue_id':show.venue_id,'name': show.name, 'rating': show.rating, 'tags': show.tags, 'show_timing': show.show_timing, 'ticket_price': show.ticket_price, 'available_seats':show.available_seats, 'date_added': show.date_added}
        show_list.append(item)
    return jsonify(show_list)

@app.route('/usersDB/',methods=['GET','POST'])
def get_users():
    users = Users.query.all()
    users_list = []
    for user in users:
        item = {'id': user.id, 'username': user.username, 'password': user.password.decode('utf-8'),'date_added': user.date_added}
        users_list.append(item)
    return jsonify(users_list)

@app.route('/adminDB/',methods=['GET','POST'])
def get_admins():
    admins = Admin.query.all()
    admins_list = []
    for admin in admins:
        item = {'id': admin.id, 'username': admin.username, 'password': admin.password,'date_added': admin.date_added}
        admins_list.append(item)
    return jsonify(admins_list)

@app.route('/user_histDB/',methods=['GET','POST'])
def get_hist():
    hists = user_hist_rating.query.all()
    hist_list = []
    for hist in hists:
        item = {'u_id': hist.u_id, 'show_id': hist.show_id, 'user_rating': hist.user_rating,'venue_id': hist.venue_id}
        hist_list.append(item)
    return jsonify(hist_list)

