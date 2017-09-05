from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin

from uuid import uuid4
db = SQLAlchemy()


generate_id = lambda : str(uuid4())[:4] 

class AdminLinksMixin:
    ADMIN_EDIT_LINK = "/{modelname}/edit/?id={modelid}&url=/{modelname}/"
    ADMIN_VIEW_LINK = "/{modelname}/details/?id={modelid}&url=/{modelname}/"

    def admin_edit_link(self):
        modelname = self.__class__.__name__.lower()
        # if modelname in "Telephone"
        return AdminLinksMixin.ADMIN_EDIT_LINK.format(modelname=modelname, modelid=self.id)

    def admin_view_link(self):
        modelname = self.__class__.__name__.lower()

        return AdminLinksMixin.ADMIN_VIEW_LINK.format(modelname=modelname, modelid=self.id)

# Define User model. Make sure to add flask_user UserMixin !!!


class Tag(db.Model, AdminLinksMixin):

    id = db.Column(db.String(4), default=generate_id, primary_key=True)

    tag = db.Column(db.String(50), nullable=False)
    # tag has many pastes
    pastes = db.relationship("Paste", backref="tag")

    def __str__(self):
        return self.tag


class User(db.Model, UserMixin, AdminLinksMixin):
    id = db.Column(db.String(4), default=generate_id, primary_key=True)

    # User Authentication information
    username = db.Column(db.String(50), nullable=False)
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
        return self.usernaxme


class Paste(db.Model, AdminLinksMixin):
    id = db.Column(db.String(4), default=generate_id, primary_key=True)
    title = db.Column(db.String(50))
    code = db.Column(db.Text())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    language = db.Column(db.String(50))

    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))

    def __str__(self):
        return self.title
