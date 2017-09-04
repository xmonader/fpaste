from flask_admin.contrib.sqla import ModelView
from models import *
from flask_admin.form.rules import Field


class EnhancedModelView(ModelView):
    can_view_details = True


class UserModelView(EnhancedModelView):
    column_filters = column_list = column_details_list = (
        'username', 'password', 'email', 'first_name', 'last_name', 'pastes')
    column_searchable_list = ('username', 'email', 'first_name', 'last_name')
    form_edit_rules = ('username', 'first_name', 'last_name', 'password', 'email', 'pastes'
                       )
    form_rules = ('username', 'email', 'password', 'first_name', 'last_name')

    inline_models = [(Paste, {'form_columns': ['id', 'title', 'code']}), ]


class PasteModelView(EnhancedModelView):
    form_rules = column_filters = column_list = column_details_list = (
        'user', 'title', 'language', 'code')
    column_searchable_list = ('title', 'language')
