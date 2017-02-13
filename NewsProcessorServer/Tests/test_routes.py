import os
import sys
sys.path.append(os.path.dirname(__file__) + "/..")
from flask import request
import unittest
import json

from datetime import date

from server import app, db

"""
These tests rely on postgression, a dynamic postgres database.
http://www.postgression.com/
"""

def assertError(resp):
	resp = json.loads(resp.data)
	assert not resp['success'] and resp['error']

def assertSuccess(resp):
	resp = json.loads(resp.data)
	assert resp['success'] and not resp['error']

class DBTests(unittest.TestCase):
	def create_app(self):
		app.config['TESTING'] = True
		app.config['SQLALCHEMY_DATABASE_URI'] = get('http://api.postgression.com').text
		return app
	def setUp(self):
		self.client = app.test_client()
		db.create_all()
	def tearDown(self):
		db.session.remove()
		db.drop_all()

class VisitDBTests(DBTests):
	def testMissingFieldsError(self):
		for path in ['/visit_begun', '/visit_ended', '/suggestion_clicked', '/suggestions_received']:
			with self.client as c:
				resp = c.post(path)
				assertError(resp)

	def testVisitBegun(self):
		with self.client as c:
			resp = c.post('/visit_begun', data=dict(
				url='www.url.com',
				timeIn=date.today(),
				id='12345'
			))
			assertSuccess(resp)

if __name__ == '__main__':
	unittest.main()