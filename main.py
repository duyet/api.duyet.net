from flask import Flask, Response, render_template, \
	request, json, jsonify, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time
from google.appengine.api import urlfetch
import urllib
import os

from api.gender import name_to_gender
from api.similar_skill import similar_skill
from api.clean_skill import clean_skill 
from api.clean_datetime import clean_datetime
from api.profile_faker import profile_faker

app = Flask(__name__)
app.config['DEBUG'] = True

limiter = Limiter(
	app,
	key_func=get_remote_address,
)

@app.errorhandler(429)
def ratelimit_handler(e):
	return make_response(
		jsonify(error="ratelimit exceeded %s" % e.description), 429
	)

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route('/')
@limiter.exempt
def index():
    content = get_file('index.html')
    return Response(content, mimetype='text/html')

@app.route("/ping")
@limiter.exempt
def ping():
    return "PONG"

""" Male for female gender """
@app.route('/api/v1/gender')
@limiter.limit("5000 per day")
@limiter.limit("500 per hour")
def gender_api():
	s_time = time.time()
	name = request.args.get('name') or request.args.get('first_name', '')
	gender = name_to_gender(name)
	e_time = time.time() - s_time
	return jsonify(name=name, gender=gender, time=e_time)

@app.route('/gender')
@limiter.exempt
def gender_view():
    return render_template('gender.html')

""" Relevant api skills """
@app.route('/api/v1/similar_skill')
@limiter.limit("5000 per day")
@limiter.limit("500 per hour")
def skill_api():
	s_time = time.time()
	skill = request.args.get('skill') or request.args.get('skills', '')
	result = similar_skill(skill)
	print result, skill
	e_time = time.time() - s_time
	return jsonify(similar_skill=skill, time=e_time)

@app.route('/similar_skill')
@limiter.exempt
def similar_skill_view():
    return render_template('similar_skill.html')

""" Skill Cleaning """
@app.route('/api/v1/clean_skill')
@limiter.limit("5000 per day")
@limiter.limit("500 per hour")
def clean_skill():
	s_time = time.time()
	skill = request.args.get('skill') or request.args.get('skills', '')
	result = clean_skill(skill)
	print result, skill
	e_time = time.time() - s_time
	return jsonify(raw=skill, cleaned=result, time=e_time)

""" Skill Cleaning """
@app.route('/api/v1/clean_datetime')
@limiter.limit("5000 per day")
@limiter.limit("500 per hour")
def clean_datetime_api():
	s_time = time.time()
	datetime = request.args.get('datetime') or request.args.get('d', '')
	result = clean_datetime(datetime)
	if result:
		result = result.isoformat()
	else:
		result = ''
	e_time = time.time() - s_time
	return jsonify(raw=datetime, cleaned=result, time=e_time)


""" Profile faker generator """
@app.route('/api/v1/profile_faker')
@limiter.limit("5000 per day")
@limiter.limit("500 per hour")
def profile_faker_api():
	return jsonify(profile_faker())

""" Sentiment analytics  """
@app.route('/api/v1/senti')
@limiter.limit("5000 per day")
@limiter.limit("500 per hour")
def senti_api():
	text = request.args.get('text') or request.args.get('t', '')
	if not text:
		return jsonify(message='error')

	try:
		headers = {'Content-Type': 'application/x-www-form-urlencoded'}
		# form_data = urllib.urlencode('text=%s' % text)
		form_data = 'text=%s' % text
		result = urlfetch.fetch(
			url='http://text-processing.com/api/sentiment/',
			payload=form_data,
			method=urlfetch.POST,
			headers=headers)
		response = app.response_class(
			response=result.content,
			status=200,
			mimetype='application/json'
		)
		return response
	except:
		return jsonify(message='error')

@app.route('/senti')
@limiter.exempt
def senti_view():
    return render_template('senti.html')


###############################################
# Demo UI
###############################################

@app.route('/clean_skill')
@limiter.exempt
def clean_skill_view():
    return render_template('clean_skill.html')

@app.route('/clean_datetime')
@limiter.exempt
def clean_datetime_view():
    return render_template('clean_datetime.html')

@app.route('/profile_faker')
@limiter.exempt
def profile_faker_view():
    return render_template('profile_faker.html')

@app.errorhandler(404)
@limiter.exempt
def page_not_found(e):
	"""Return a custom 404 error."""
	return 'Sorry, nothing at this URL.', 404


@app.route('/nn')
@limiter.exempt
def neural_network():
    return render_template('nn/index.html')
