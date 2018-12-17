import graphene

import users.schema
import unions.schema


class Query(users.schema.Query, unions.schema.Query, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, unions.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
