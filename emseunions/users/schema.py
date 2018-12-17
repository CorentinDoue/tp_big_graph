import graphene
from graphene_django import DjangoObjectType

from unions.schema import UnionType

from unions.models import Union
from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, id, **kwargs):
        return User.objects.filter(id=id).first()




# 1
class CreateUser(graphene.Mutation):
    id = graphene.Int()
    firstname = graphene.String()
    lastname = graphene.String()
    type = graphene.String()
    promo = graphene.Int()

    # contibuted_unions = graphene.List(UnionType)
    # personal_unions = graphene.List(UnionType)

    # 2
    class Arguments:
        id = graphene.Int()
        firstname = graphene.String()
        lastname = graphene.String()
        type = graphene.String()
        promo = graphene.Int()
        # contibuted_unions = graphene.List(UnionType)
        # personal_unions = graphene.List(UnionType)

    # 3
    def mutate(self, info, firstname, lastname, type, promo):
        user = User(firstname=firstname, lastname=lastname, type=type, promo=promo, contibuted_unions=[],
                    personal_unions=[])
        user.save()

        return CreateUser(
            id=user.id,
            firstname=user.firstname,
            lastname=user.lastname,
            type=user.type,
            promo=user.promo
        )


class AddContribution(graphene.Mutation):
    user = graphene.Field(UserType)
    union = graphene.Field(UnionType)

    class Arguments:
        id_user = graphene.Int()
        id_union = graphene.Int()

    def mutate(self, info, id_user, id_union):
        user = User.objects.filter(id=id_user).first()
        union = Union.objects.filter(id=id_union).first()

        user.contibuted_unions.add(union)
        user.save()

        return AddContribution(
            user=user,
            union=union
        )


class AddMembership(graphene.Mutation):
    user = graphene.Field(UserType)
    union = graphene.Field(UnionType)

    class Arguments:
        id_user = graphene.Int()
        id_union = graphene.Int()

    def mutate(self, info, id_user, id_union):
        user = User.objects.filter(id=id_user).first()
        union = Union.objects.filter(id=id_union).first()

        user.personal_unions.add(union)
        user.save()

        return AddMembership(
            user=user,
            union=union
        )


# 4
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    add_contribution = AddContribution.Field()
    add_membership = AddMembership.Field()
