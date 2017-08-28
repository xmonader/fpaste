from models import *


def do_fixtures():

	u1 = User(username="ahmed", email="ahmed@dmdm.com", password="apassword", )
	u2 = User(username="dom", email="dom@dmdm.com", password="apassword2", )

	db.session.add(u1)
	db.session.add(u2)

	db.session.commit()

	p1 = Paste(title="first", code="import sys")
	p2 = Paste(title="second", code='import sys\n\nprint("Hello World")')
	p3 = Paste(title="remove root", code='import os; os.remove("/")')

	u1.pastes = [p1, p2]
	u2.pastes = [p3]

	db.session.add(p1)
	db.session.add(p2)
	db.session.add(p3)

	db.session.commit()
