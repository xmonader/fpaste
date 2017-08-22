from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin

import sqlalchemy.types
from sqlalchemy import schema, orm, ForeignKey, types, event
from sqlalchemy.ext.declarative import (declarative_base, DeclarativeMeta)
from sqlalchemy.orm import (scoped_session, sessionmaker, deferred,
                            column_property, mapper, relationship)

db = SQLAlchemy()


# Define User model. Make sure to add flask_user UserMixin !!!
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # User Authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')

    # User Email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')

    # user has many pastes
    pastes = db.relationship("Paste", backref="user")

    def is_active(self):
        return self.is_enabled

    def __str__(self):
        return self.username


class Paste(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50))
    code = db.Column(db.Text())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # user = db.relationship("User", back_populates="pastes")

    def __str__(self):
        return self.username
