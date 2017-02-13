import os
import sys
sys.path.append(os.path.dirname(__file__) + "/..")
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import unittest
import urllib2
from flask_testing import TestCase, LiveServerTestCase


class VisitDBTests(LiveServerTestCase):

	def create_app(self):
		app = Flask(__name__)
		app.config.from_object(os.environ['TEST_SETTINGS']) #get the config from the config.py file
		self.db = SQLAlchemy(app)
		return app

	def setUp(self):
		self.db.create_all()

	def tearDown(self):
		pass

	def testGet(self):
		print self.get_server_url()
		print resp

if __name__ == '__main__':
	unittest.main()