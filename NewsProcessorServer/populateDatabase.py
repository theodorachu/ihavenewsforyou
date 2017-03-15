from server import app, db #, login_manager
from server.models import Article, User, Visit, NewsSource 
import random
from datetime import datetime

name = raw_input("Please enter User's name: ")

user = User.query.filter_by(name=name).first()
if not user:
  print "User does not exist in the database. Aborting."
  5/0

while True:
  # Creates a visit from the URL
  url = raw_input("Visit URL: ")
  yearStart = random.randint(2010, 2017)
  monthStart = random.randint(1, 12) 
  dayStart = random.randint(1, 28)
  hourStart = random.randint(0, 24 - 1) # inclusive
  secondStart = random.randint(0, 60 - 1)
  startDate = datetime(yearStart, monthStart, dayStart, hourStart, secondStart)

  yearEnd = random.randint(yearStart, 2017)
  monthEnd = random.randint(monthStart, 12)
  dayEnd = random.randint(dayStart, 28)
  hourEnd = random.randint(hourStart, 24 - 1)
  if (yearEnd == yearStart) and (monthEnd == monthStart) and (dayEnd == dayStart):
    secondStart = 0
  secondEnd = random.randint(secondStart + 1, 60 - 1)
  endDate = datetime(yearEnd, monthEnd, dayEnd, hourEnd, secondEnd)

  newVisit = Visit(url, user.id, startDate, endDate)
  success = newVisit.add(newVisit)
  if success:
    print("Visit added!")
    print(str(len(Visit.query.all())) + " visits for this user in the database.")
  else:
    print("Visit adding failed")





