from neo4j.v1 import GraphDatabase


class Neo4jBdd(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def clear_database(self):
        with self._driver.session() as session:
            session.write_transaction(self._clear_database)

    def add_user(self, firstname, lastname, promo, type):
        with self._driver.session() as session:
            id_user = session.write_transaction(self._create_and_return_user, firstname, lastname, promo, type)
            return id_user

    def add_union(self, name):
        with self._driver.session() as session:
            id_union = session.write_transaction(self._create_and_return_union, name)
            return id_union

    def add_contribution(self, id_user, id_union):
        with self._driver.session() as session:
            session.write_transaction(self._create_and_return_contribution, id_user, id_union)

    def add_membership(self, id_user, id_union):
        with self._driver.session() as session:
            session.write_transaction(self._create_and_return_membership, id_user, id_union)

    def get_contributors(self, union):
        with self._driver.session() as session:
            contributors = session.write_transaction(self._query_all_contributor, union)
            return contributors

    def get_members(self, union):
        with self._driver.session() as session:
            members = session.write_transaction(self._query_all_members, union)
            return members

    def get_contributions(self, firstname, lastname):
        with self._driver.session() as session:
            contributions = session.write_transaction(self._query_all_contribution, lastname, firstname)
            return contributions

    def get_unions(self, firstname, lastname):
        with self._driver.session() as session:
            unions = session.write_transaction(self._query_all_union, lastname, firstname)
            return unions

    @staticmethod
    def _clear_database(tx):
        tx.run("MATCH (n) "
               "DETACH DELETE n ")

    @staticmethod
    def _create_and_return_user(tx, firstname, lastname, promo, type):
        result = tx.run("CREATE (a:User) "
                        "SET a.firstname = $firstname "
                        "SET a.lastname = $lastname "
                        "SET a.promo = $promo "
                        "SET a.type = $type "
                        "RETURN id(a)", firstname=firstname, lastname=lastname, promo=promo, type=type)
        return result.single()[0]

    @staticmethod
    def _create_and_return_union(tx, name):
        result = tx.run("CREATE (a:Union) "
                        "SET a.name = $name "
                        "RETURN id(a)", name=name)
        return result.single()[0]

    @staticmethod
    def _create_and_return_contribution(tx, id_user, id_union):
        result = tx.run("MATCH(user: User), (uni: Union) "
                        "WHERE ID(user) = $id_user AND ID(uni) = $id_union "
                        "CREATE(user)-[c: CONTRIBUTE]->(uni) "
                        "RETURN c", id_user=id_user, id_union=id_union)

    @staticmethod
    def _create_and_return_membership(tx, id_user, id_union):
        result = tx.run("MATCH(user: User), (uni: Union) "
                        "WHERE ID(user) = $id_user AND ID(uni) = $id_union "
                        "CREATE(user)-[c: IS_MEMBER_OF]->(uni) "
                        "RETURN c", id_user=id_user, id_union=id_union)

    @staticmethod
    def _query_all_contributor(tx, union):
        result = tx.run("MATCH p=(user: User)-[r:CONTRIBUTE]->(uni: Union {name: $union}) "
                        "RETURN user", union=union)
        return result.values()

    @staticmethod
    def _query_all_members(tx, union):
        result = tx.run("MATCH p=(user: User)-[r:IS_MEMBER_OF]->(uni: Union {name: $union}) "
                        "RETURN user", union=union)
        return result.values()

    @staticmethod
    def _query_all_contribution(tx, lastname, firstname):
        result = tx.run("MATCH p=(user: User {lastname: $lastname, firstname: $firstname})-[r:CONTRIBUTE]->(uni: Union) "
                        "RETURN uni", lastname=lastname, firstname=firstname)
        return result.values()

    @staticmethod
    def _query_all_union(tx, lastname, firstname):
        result = tx.run("MATCH p=(user: User {lastname: $lastname, firstname: $firstname})-[r:IS_MEMBER_OF]->(uni: Union) "
                        "RETURN uni", lastname=lastname, firstname=firstname)
        return result.values()
