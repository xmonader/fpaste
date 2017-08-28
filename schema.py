from models import User as UserModel, Paste as PasteModel
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType


class Paste(SQLAlchemyObjectType):

    class Meta:
        model = PasteModel


class User(SQLAlchemyObjectType):

    class Meta:
        model = UserModel


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    pastes = graphene.List(Paste)
    users = graphene.List(User)

    def resolve_pastes(self, args, context, info):
        query = Paste.get_query(context)  # SQLAlchemy query
        return query.all()

    def resolve_users(self, args, context, info):
        query = User.get_query(context)  # SQLAlchemy query
        return query.all()


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(lambda: User)


    def mutate(self, username):
        u = User(username=username)
        ok = True
        return CreateUser(user=u, ok=ok)



class MyMutations(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, types=[
                         User, Paste], mutation=MyMutations)
