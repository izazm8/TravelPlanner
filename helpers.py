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
			return redirect(url_for("index", next=request.url))
		return f(*args, **kwargs)
	return decorated_function

def is_safe_url(target):
	ref_url = urlparse(request.host_url)
	test_url = urlparse(urljoin(request.host_url, target))
	return test_url.scheme in ('http', 'https') and\
		ref_url.netloc == test_url.netloc
