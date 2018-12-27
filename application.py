from flask import Flask, flash, redirect, request, render_template, session, url_for, abort, jsonify
from flask_session import Session
from tempfile import mkdtemp

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

@app.route('/signup', methods=['GET'])
def signup():
    return render_template("signup.html")

@app.route('/login', methods=['GET'])
def login():
    session['user_id'] = 'test'
    return render_template("login.html")

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    places_list = db.execute('SELECT * FROM Places')
    return render_template("dashboard.html", places = places_list)

@app.route('/contact', methods=['GET'])
def contact_us():
    return render_template("contact-us.html")

@app.route('/about', methods=['GET'])
def about_us():
    return render_template("about-us.html")

@app.route('/test')
def test():
    data = db.execute("SELECT * FROM DEMO_USERS")
    return str(data)
