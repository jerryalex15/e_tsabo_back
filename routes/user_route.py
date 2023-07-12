from flask import Blueprint, flash, request, redirect, url_for, jsonify
from classes.RegistrationForm import RegistrationForm
from database import connection
import jwt
from decouple import config
from flask_jwt_extended import jwt_required, get_jwt_identity


user_route = Blueprint('user', __name__)

@user_route.route('/api/user_route/registration', methods=['GET', 'POST'])
def registration():
    registration_form = RegistrationForm()
    # login_form = LoginForm()

    if registration_form.validate_on_submit():
        registration_form.save_user()
        flash('Account created successfully!', 'success')
        return redirect(url_for('home'))
   
    # ...

@user_route.route('/api/user_route/login', methods=['POST'])
def login():
    # Récupérer les données d'identification de l'utilisateur depuis la requête POST
    username = request.json['username']
    password = request.json['password']

    # Vérifier les informations d'identification dans la base de données
    cur = connection.cursor()
    cur.execute("SELECT id,username,password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    connection.close()
    user_tuple= (("id",user[0]),("username",user[1]),("password",user[2]))
    dict_user= dict(user_tuple)
    

    if user:
        # Vérifier le mot de passe
        if password == dict_user['password']:
            # Authentification réussie
            
            payload = {'username':dict_user['username']}
            # secret_key ="gdfsfdhgfdgv"
            secret_key = config('SECRET_KEY')
            
            response = {
                'idUser': dict_user['id'],
                'success': True,
                'message': 'Authentification réussie',
                'token': jwt.encode(payload, secret_key, algorithm='HS256')  # jeton d'accès généré
            }
            
        else:
            # Mot de passe incorrect
            response = {
                'success': False,
                'message': 'Votre mot de passe est incorrect',
                
            }
        return jsonify(response)
    else:
        # Utilisateur non trouvé
        response = {
                'success': False,
                'message': 'Utilisateur non trouvé',
                
            }
        return jsonify(response)

#Pour déchiffrer et vérifier un token dans un route protégée, on utilise le décorateur 'jwt_required()' de la bibliothèque Flask-JWT-Extended
#ou implémenter un vérification de token en utilisant la méthode 'jwt.decode'

@user_route.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    #obtenir l'identiter de l'utilisateur à partir du token
    current_user = get_jwt_identity() 
    #print(current_user)  #pour vérifier ce qu'il y a dedans
    
    #effectuez des opérations protégées avec l'identité de l'utilisateur
    return f"Utilisateur authentifié : {current_user}"