import os
from flask import Flask 
from models import db, User, Paste
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_basicauth import BasicAuth
from fixtures import do_fixtures
from flask_graphql import GraphQLView
from schema import schema


DBDIR = os.path.join(os.getcwd(), "db")


if not os.path.exists(DBDIR):
    os.mkdir(DBDIR)

development = True

DBPATHDEV = os.path.join(os.getcwd(), "db", "development.db")
DBPATHPROD = os.path.join(os.getcwd(), "db", "production.db")
DBPATH = DBPATHDEV

if development is False:
    DBPATH = DBPATHPROD


config = {
    "SQLALCHEMY_DATABASE_URI": "sqlite:///{}".format(DBPATH),
    "SQLALCHEMY_ECHO": True,
    "SQLALCHEMY_RECORD_QUERIES": True,
}

app = Flask(__name__)
app.jinja_env.globals.update(getattr=getattr, hasattr=hasattr, type=type)
app.secret_key = "dmdmkey"
app.config = {**app.config, **config}
db.app = app
db.init_app(app)
migrate = Migrate(app, db)

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
app.config['BASIC_AUTH_FORCE'] = True
# basic_auth = BasicAuth(app)

models = [User, Paste]
db.init_app(app)
db.app = app
db.session.autocommit = True
migrate = Migrate(app, db)


class EnhancedModelView(ModelView):
    can_view_details = True


def create_all():
    try:
        db.create_all()
        db.session.commit()
    except Exception as e:
        pass    



if __name__ == "__main__":

    try:
        os.remove(DBPATH)
    except:
        pass

    try:
        db.create_all(app=app)
        db.session.commit()
    except Exception as e:  # db already exists
        raise
    try:
        do_fixtures()
    except:
        raise
    print(schema)
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
    admin = Admin(app, "FPasteCP")
    for m in models:
        admin.add_view(EnhancedModelView(m, db.session))
    app.run(debug=True, port=8002)
