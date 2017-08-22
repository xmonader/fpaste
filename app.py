from flask import Flask
from models import db, User, Paste
from models.schema import schema
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
db.app = app
migrate = Migrate(app, db)


def create_all():
    try:
        db.create_all()
        db.session.commit()
    except Exception as e:
        pass


def do_fixtures():
    global db
    u1 = User(username="ahmed", password="dmdm", email="ahmed@dmdm.com")
    u2 = User(username="xmon", password="dmdm", email="axmon@dmdm.com")
    u3 = User(username="rms", password="dmdmrms", email="rms@gnu.com")

    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)
    db.session.commit()
    p1 = Paste(title="no itle", code="import os")
    p2 = Paste(title="import many", code="import sys, os")
    p3 = Paste(title="print 5", code="print 5")
    p4 = Paste(title="import syse", code="import sys")
    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.add(p4)
    u1.pastes = [p1, p2]
    u2.pastes = [p3, p4]

    db.session.commit()


if __name__ == "__main__":
    if os.path.exists(DBPATH):
        os.remove(DBPATH)
    create_all()
    do_fixtures()
    admin = Admin(app, "FPasteCP")
    for m in models:
        admin.add_view(ModelView(m, db.session))

    from flask_graphql import GraphQLView

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

    app.run(debug=True)
