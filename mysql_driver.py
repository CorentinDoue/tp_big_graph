import mysql.connector

class MysqlBdd(object):

    def __init__(self, host, database, user, password):
        self._mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database
        )
        self._mycursor = self._mydb.cursor()

    def get_users(self):
        sql = "SELECT id_user, login_user, prenom, nom, type_user, promo_user, droit_user, droit_cercle FROM user"
        self._mycursor.execute(sql)

        myresult = self._mycursor.fetchall()
        return myresult

    def get_bde_admin(self):
        sql = "SELECT id_user FROM admin"
        self._mycursor.execute(sql)

        myresult = self._mycursor.fetchall()
        return myresult
