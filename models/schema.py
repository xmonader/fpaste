from . import User as UserModel, Paste as PasteModel
from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel


class Paste(SQLAlchemyObjectType):
    class Meta:
        model = PasteModel


class Query(graphene.ObjectType):
    users = graphene.List(User)
    pastes = graphene.List(Paste)

    def resolve_users(self, args, context, info):
        query = User.get_query(context)  # SQLAlchemy query
        return query.all()

    def resolve_pastes(self, args, context, info):
        query = Paste.get_query(context)  # SQLAlchemy query
        return query.all()


schema = graphene.Schema(query=Query)