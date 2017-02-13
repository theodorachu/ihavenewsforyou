from server import app, db #, login_manager
from models import Article, User, Visit
from db_helpers import dbExecute
from dateutil import parser as dateparser

from contextlib import contextmanager


from flask import render_template, request
import httplib2
from apiclient import discovery
from oauth2client import client
import json

"""
Docs:
1) Flask Login: 
	- https://flask-login.readthedocs.io/en/latest/
	- https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask
	- https://pythonhosted.org/Flask-Social/

"""

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/recommend_articles', methods=['GET'])
def recommendArticles():
	pass

@app.route('/visit_begun', methods=['POST'])
def storeVisitBegun():
	if areFieldsMissing(request, ['url', 'timeIn', 'id']):
		return createJSONResp(error="missing field(s). fields are %s" % ','.join(fields))

	visit = Visit.createVisitFromRequest(request)
	success = Visit.add(visit)
	if not success:
		return createJSONResp(error='Failed to add visit to db')
	return createJSONResp(success=True)

@app.route('/visit_ended', methods=['POST'])
def storeVisitEnded():
	if areFieldsMissing(request, ['url', 'timeOut', 'id']):
		return createJSONResp(error="missing field(s). fields are %s" % ','.join(fields))

	visit = Visit.getMostRecentVisit(request.form['id'], request.form['url'])
	success = Visit.update(visit, {'timeOut': dateparser.parse(request.form['timeOut'])})
	if not visit:
		return createJSONResp(error='Visit does not exist')
	if not success:
		return createJSONResp(error='Failed to update visit')
	return createJSONResp(success=True)

@app.route('/suggestion_clicked', methods=['POST'])
def suggestionClicked():
	if areFieldsMissing(request, ['url', 'timeIn', 'id']):
		return createJSONResp(error="missing field(s). fields are %s" % ','.join(fields))

	visit = Visit.createVisitFromRequest(request)
	success = Visit.update(visit, {'clickedSuggestion': True})
	if not success:
		return createJSONResp('Failed to update visit')
	return createJSONResp(success=True)

@app.route('/suggestions_received', methods=['POST'])
def suggestionsReceived():
	if areFieldsMissing(request, ['url', 'timeIn', 'id']):
		return createJSONResp(error="missing field(s). fields are %s" % ','.join(fields))

	visit = Visit.createVisitFromRequest(request)
	success = Visit.update(visit, {'receivedSuggestions': True})
	if not success:
		return createJSONResp('Failed to update visit')
	return createJSONResp(success=True)



############## HELPER METHODS #####################
def areFieldsMissing(request, fields):
	for field in fields:
		if field not in request.form.keys(): 
			return True
	return False

def createJSONResp(error=None, success=False):
	return json.dumps({'error': error, 'success': success})




