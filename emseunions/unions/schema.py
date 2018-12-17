import graphene
from graphene_django import DjangoObjectType

from .models import Union


class UnionType(DjangoObjectType):
    class Meta:
        model = Union


class Query(graphene.ObjectType):
    unions = graphene.List(UnionType)

    def resolve_unions(self, info, **kwargs):
        return Union.objects.all()

    def resolve_union(self, info, name, **kwargs):
        return Union.objects.filter(name=name).first()



#1
class CreateUnion(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()

    #2
    class Arguments:
        id = graphene.Int()
        name = graphene.String()

    #3
    def mutate(self, info, name):
        union = Union(name=name)
        union.save()

        return CreateUnion(
            id=union.id,
            name=union.name
        )


#4
class Mutation(graphene.ObjectType):
    create_union = CreateUnion.Field()