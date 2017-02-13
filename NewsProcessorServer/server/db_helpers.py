from server import db

def dbExecute(command):
	session = db.session()
	try:
		command(session)
		session.commit()
	except: #An error occurred 
		session.rollback()
		return False
	return True
