from flask import Blueprint, flash, request, redirect, url_for, jsonify,current_app
import jwt
from flask_cors import cross_origin
from decouple import config
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
from database import create_new_connection
import bcrypt


user_route = Blueprint('user', __name__)

@user_route.route('/api/user_route/registration', methods=[ 'POST'])
@cross_origin()
def registration():
    
    try:
        if request.headers['Content-Type'] == 'application/json':
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            name = data.get('name')
            gender = data.get('gender')
            birthdate = data.get('birthdate')


            # Validez les données comme vous le feriez normalement
            if not username or not email or not password or not confirm_password:
                return jsonify({'error': 'Tous les champs sont requis'}), 400

            #Testez si le nom d'utilisateur est déjà pris
            connection = create_new_connection()
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE username = %s"
            
            cursor.execute(query, (username,))
            test = cursor.fetchone()
            cursor.close()
            connection.close()

            if test:

                return jsonify({'error': 'Ce nom d\'utilisateur est déjà pris'}), 400

            #Testez si l'adresse email est déjà utiliser
            connection = create_new_connection()
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            if result:

                return jsonify({'error': 'Cet adresse email est déjà utilisé'}), 400

            if password != confirm_password:
                return jsonify({
                
                    'error': 'Les mots de passe ne correspondent pas'}), 400

            #Enregistrer utilisateur
            connection = create_new_connection()
            cursor = connection.cursor()
            query = "INSERT INTO users (username, email, password,name,birthdate,gender) VALUES  (%s, %s, %s,%s,%s,%s)"
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute(query, (username, email,hashed_password, name,birthdate,gender))
            connection.commit()
            cursor.close()
            connection.close()

            response_data = {
                "success" : True,
                "message" : "Inscription réussie"
            }
            current_app.logger.info('Inscription réussie')  # Enregistrement d'une information
            return jsonify(response_data),200
        else:
            return jsonify({'error': 'Content-Type non pris en charge'}), 415
   
    except Exception as e:
        # Gérez les exceptions en fonction de vos besoins
        error_message = str(e)
        current_app.logger.error(f'Erreur lors de l\'inscription : {e}')  # Enregistrement d'une erreur
        return jsonify({'error': error_message}), 500
    # ...



@user_route.route('/api/user_route/login', methods=['POST'])
@cross_origin()
def login():
    try:
    # Récupérer les données d'identification de l'utilisateur depuis la requête POST
        username = request.json['username']
        password = request.json['password']

        # Vérifier les informations d'identification dans la base de données
        connection = create_new_connection()
        cur = connection.cursor()
        cur.execute("SELECT id,username,password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        connection.close()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # connection.close()

        if user:
            user_tuple= (('id',user[0]),('username',user[1]),('password',user[2]))
            dict_user= dict(user_tuple)
            # Vérifier le mot de passe
            if bcrypt.checkpw(password.encode('utf-8'), dict_user['password'].encode('utf-8')):
                # Authentification réussie
                
                user_id = dict_user['id'] 
               
                user_info = get_user_info(user_id)
                access_token = create_access_token(identity=user_id, additional_claims=user_info)
                response = {
                    
                    'success': True,
                    'message': 'Authentification réussie',
                    'token' : access_token
                }
                current_app.logger.info('Authentification réussie') 
                return jsonify(response),200
            else:
                # Mot de passe incorrect
                response = {
                    'success': False,
                    'message': 'Votre mot de passe est incorrect',
                    
                }
            
            current_app.logger.info('Authentification échouée: mot de passe incorrect')
            return jsonify(response),401
        else:
            # Utilisateur non trouvé
            response = {
                    'success': False,
                    'message': 'Utilisateur non trouvé',
                    
                }
           
            current_app.logger.info('Username not found')
            return jsonify(response),401
    except Exception as e:
        # Gérez les exceptions en fonction de vos besoins
        error_message = str(e)
        current_app.logger.error(f'Erreur lors de l\'inscription : {e}')
        return jsonify({'error': error_message}), 500

#Pour déchiffrer et vérifier un token dans un route protégée, on utilise le décorateur 'jwt_required()' de la bibliothèque Flask-JWT-Extended
#ou implémenter un vérification de token en utilisant la méthode 'jwt.decode'



@user_route.route('/api/user_route/listdocs', methods=['GET'])
@cross_origin()
def getListDocs():
    # try:
    #     connection = create_new_connection()
    #     cur = connection.cursor()
    #     cur.execute("SELECT id,name,spectialite FROM users WHERE isDoc = 1")
    #     doctors = cur.fetchall();
    #     cur.close()
    #     connection.close()

    #     if doctors:
    #         response = {
    #             'success' : True,
    #             'doctors' : doctors
    #         }
    #     else:
    #         response = {
    #             'success' : False,
    #             'message' : "Il n'y a pas de docteur disponible "
    #         }
    #         return jsonify(response)
        
    # except Exception as e:
    #     error_message = str(e)
    #     current_app.logger.error(f'Erreur lors de la récupération des docteurs : {e}')
   #     return jsonify({'error': error_message}), 500
    return print('ok')
@user_route.route('/protected', methods=['GET'])
@jwt_required(locations=["headers"])
def protected():
    try:
        #obtenir l'identiter de l'utilisateur à partir du token
        current_user = get_jwt_identity() 
        #print(current_user)  #pour vérifier ce qu'il y a dedans
        
        response = {
                    'current_user': current_user
                    }
        #effectuez des opérations protégées avec l'identité de l'utilisateur
        current_app.logger.info('info current user')
        return jsonify(response);

    except Exception as e:
    # Gérez les exceptions en fonction de vos besoins
        error_message = str(e)
        current_app.logger.error(f'Erreur lors de l\'inscription : {e}')
        return jsonify({'error': error_message}), 500


def get_user_info(userId):

    try:

        connection = create_new_connection()
        cur = connection.cursor()

        cur.execute("SELECT username,email,name,gender,isDoc,birthdate,specialite FROM users WHERE id = %s", (userId,))
        user = cur.fetchone()

        cur.close()
        connection.close()

        claims = {
            "username": user[0],
            "email": user[1],
            "name": user[2],
            "gender": user[3],
            "isDoc": user[4],
            "birthdate": user[5],
            "specialite":user[6]

        }

        return claims

    except Exception as e:
    # Gérez les exceptions en fonction de vos besoins
        error_message = str(e)
        current_app.logger.error(f'Erreur lors de la collection des informations de l\'utilisateur : {e}')
        return {'error': error_message}
