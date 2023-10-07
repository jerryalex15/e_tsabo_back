import mysql.connector
from decouple import config


# # Informations de connexion
# host = 'localhost'
# user = 'root'
# password = ''
# database = 'etsabodb'

host = config('host', default='localhost')
user = config('user', default='root')
password = config('password', default='')
database = config('etsabodb', default='')

# Établir la connexion
try:
    connection = mysql.connector.connect(host=host, user=user, password=password, database='etsabodb', charset='utf8')
    print("Connexion réussie !")
except mysql.connector.Error as error:
    print("Erreur de connexion : {}".format(error))
