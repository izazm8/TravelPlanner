import urllib.request
from urllib.parse import urlparse, urljoin

from flask import redirect, render_template, request, session, url_for
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/views/#decorating-views
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc

def get_neighbours(place_id, db_conn):
    return db_conn.execute('SELECT * FROM Neighbours WHERE place_id = {}'.format(place_id))

def get_optimal_path(places):
    # TODO: Write algo
    optimal_path = [] # not just includes the selected places, but also the ones we have to go through
    return optimal_path

def get_path_cost(path):
    # TODO: Using the neighbours table, calculate total cost
    return 0

def get_path_travel_time(path):
    # TODO: Using neighbours table, calculate total travel time
    return 0

def get_last_id(db_conn, col_name, table_name):
    x = db_conn.execute('SELECT MAX({}) as last_insert_id FROM {}'.format(col_name, table_name))[0]['last_insert_id']
    last_booking_id = 0 if x is None else x
    return last_booking_id
