from server import db
from sqlalchemy.exc import SQLAlchemyError

def dbExecute(command):
	session = db.session()
	try:
		command(session)
		session.commit()
	except SQLAlchemyError as e: #An error occurred 
		print e
		session.rollback()
		return False
	return True
