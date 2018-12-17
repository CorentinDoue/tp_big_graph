from mysql_driver import MysqlBdd
from neo4j_driver import Neo4jBdd
from tools import save_obj, load_obj

if __name__ == '__main__':
    neo4j_bdd = Neo4jBdd('bolt://localhost:7687', 'neo4j', '0386479877')
    # mysql_bdd = MysqlBdd("localhost", "bde", "Coco", "0386479877")
    #
    # bde_admins = mysql_bdd.get_bde_admin()
    #
    # # Convert array of tuple in array of id (int)
    # temp=[]
    # for admin in bde_admins:
    #     temp.append(admin[0])
    # bde_admins = temp
    #
    # users = mysql_bdd.get_users()
    #
    # save_obj(bde_admins, "bde_admins.pkl")
    # save_obj(users, "users.pkl")

    bde_admins = load_obj("bde_admins.pkl")
    users = load_obj("users.pkl")

    neo4j_bdd.clear_database()

    id_bde = neo4j_bdd.add_union('BDE')
    id_cercle = neo4j_bdd.add_union('Cercle')

    for user in users:
        # Check if firstname and lastname are defined
        if user[2] == '':
            firstname = user[1].split('.')[0]
            try:
                lastname = user[1].split('.')[1]
            except:
                lastname = ''
        else:
            firstname = user[2]
            lastname = user[3]

        id_user = neo4j_bdd.add_user(firstname, lastname, user[5], user[4])

        # Check if the user is a contributor of the student union
        if user[6] == 'user':
            neo4j_bdd.add_contribution(id_user, id_bde)

        # Check if the user is a contributor of the Cercle
        if user[7] != 'aucun':
            neo4j_bdd.add_contribution(id_user, id_cercle)

        # Check if the user is a member of the Cercle
        if user[7] == 'cercle':
            neo4j_bdd.add_membership(id_user, id_cercle)

        # Check if the user is a member of the student union
        if user[0] in bde_admins:
            neo4j_bdd.add_membership(id_user, id_bde)

    bde_contributors = neo4j_bdd.get_contributors('BDE')
    print('Contributors of the student union :')
    for contributor in bde_contributors:
        print(contributor)

    cercle_members = neo4j_bdd.get_members('Cercle')
    print('Members of the Cercle :')
    for member in cercle_members:
        print(member)

    my_contributions = neo4j_bdd.get_contributions('Corentin', 'DOUE')
    print('Unions where Corentin Doué is contributor :')
    for union in my_contributions:
        print(union)

    my_unions = neo4j_bdd.get_unions('Corentin', 'DOUE')
    print('Unions where Corentin Doué is member :')
    for union in my_unions:
        print(union)