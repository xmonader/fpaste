from models import db, User as UserModel, Paste as PasteModel
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType


class Paste(SQLAlchemyObjectType):

    class Meta:
        model = PasteModel


class User(SQLAlchemyObjectType):

    class Meta:
        model = UserModel



class CreateUser(graphene.Mutation):
    class Input:
        username = graphene.String(required=True)
        email = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(lambda : User)

    def mutate(self, args, context, info):
        username = args.get('username')
        email = args.get('email', '')
        user = UserModel(username=username, email=email) # not nullable.
        db.session.add(user)
        db.session.commit()
        return CreateUser(user=user, ok=True)


# class Person(graphene.ObjectType):
#     name = graphene.String()
#     age = graphene.Int()

# class CreatePerson(graphene.Mutation):
#     # class Arguments:
#     #     name = graphene.String()
#     class Input:
#         name = graphene.String()

#     ok = graphene.Boolean()
#     person = graphene.Field(lambda: Person)

#     def mutate(self, args, context, info):
#         name = args.get('name')
#         person = Person(name=name)
#         ok = True
#         return CreatePerson(person=person, ok=ok)

# class CreateUser(graphene.Mutation):
#     class Input:
#         name = graphene.String(required=True)


# class CreatePerson(graphene.Mutation):
#     class Input:
#         name = graphene.String()

#     ok = graphene.Boolean()
#     person = graphene.Field(lambda: Person)

#     def mutate(self, args, context, info):
#         name = args.get('name')
#         person = Person(name=name)
#         ok = True
#         return CreatePerson(person=person, ok=ok)


class MyMutations(graphene.ObjectType):
    # create_person = CreatePerson.Field()
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    pastes = graphene.List(Paste)
    users = graphene.List(User, username=graphene.String())
    # person = graphene.Field(Person)
    user = graphene.Field(User)

    def resolve_pastes(self, args, context, info):
        query = Paste.get_query(context)  # SQLAlchemy query
        return query.all()

    def resolve_users(self, args, context, info):
        query = User.get_query(context)  # SQLAlchemy query
        if args and args['username']:
            username = args['username']
            query = query.filter_by(username=username)
        return query.all()



schema = graphene.Schema(query=Query, mutation=MyMutations, types=[User, Paste])
