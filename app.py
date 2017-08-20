from flask import Flask 
from models import db, User, Paste
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_basicauth import BasicAuth

import os

app = Flask(__name__)

DBDIR = os.path.join(os.getcwd(), "db")
if not os.path.exists(DBDIR):
	os.mkdir(DBDIR)

DBPATH = os.path.join(DBDIR, "development.sqlite")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DBPATH)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

models = [User, Paste]
db.init_app(app)

migrate = Migrate(app, db)


def create_all():
	try:
		db.create_all()
		db.session.commit()
	except Exception as e:
		pass	

if __name__ == "__main__":
	create_all()
	admin = Admin(app, "FPasteCP")
	for m in models:
		admin.add_view(ModelView(m, db.session))
	app.run(debug=True)