from flask import Flask, flash, redirect, request, render_template, session, url_for, abort, jsonify
from flask_session import Session
from tempfile import mkdtemp
from datetime import datetime

from cs50 import SQL
from helpers import *

app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# connect to database
# parameters are in the format: driver://username:password@server[:port]/database_name
db = SQL("oracle+cx_oracle://TRAVEL_PLANNER:travel@localhost:1521/xe")

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user_id'] = '1'

        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        return render_template("login.html")

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    places_list = db.execute('SELECT * FROM Places')
    places_list = sorted(places_list, key=lambda k : k['place_name'])

    packages_list = db.execute('SELECT * FROM Packages')

    return render_template("dashboard.html", places=places_list, packages=packages_list)

@app.route('/booking', methods=['POST'])
def booking():
    return str(request.form)
    # 1. get user input from request.form
    package_id = request.form['package']
    total_people = request.form['total_people']
    destinations = request.form['destinations[]']

    # 2. using MCM, calculate optimal path. Then derive total duration and travel time of that path
    optimal_path = get_optimal_path(destinations)
    #standard_charges = get_path_cost(optimal_path)
    #total_charges = standard_charges * package_factor
    #travel_time = get_path_travel_time(optimal_path)
    #total_duration = travel_time + stay_duration

    # 3. store booking data in Bookings table
    x = db.execute('SELECT MAX(booking_id) FROM Bookings')[0]['booking_id']
    last_booking_id = 0 if x is None else x
    booking_id = last_booking_id + 1

    db.execute('INSERT INTO Bookings (booking_id, user_id, package_id, booking_date, booking_total_people,'
               'booking_total_charges, booking_total_duration)'
               'VALUES ({}, {}, {}, {}, {}, {}, {})'
               .format(booking_id, session.get('user_id'), package_id, datetime.today(), total_people,
                       total_charges, total_duration))

    # 4. store each booking destination and its stay duration in Booking_destinations table

    # 5. redirect to booking confirmation page
    return redirect(url_for('booking_confirmed', booking_id=booking_id))

@app.route('/booking-confirmed/<booking_id>', methods=['GET'])
def booking_confirmed(booking_id):
    return "You have booked successfully!"

@app.route('/contact', methods=['GET'])
def contact_us():
    return render_template("contact-us.html")

@app.route('/about', methods=['GET'])
def about_us():
    return render_template("about-us.html")

@app.route('/test')
def test():
    data = get_neighbours(1, db)
    return str(data)