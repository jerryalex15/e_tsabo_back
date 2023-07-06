from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_cors import CORS
import mysql.connector
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from config import SECRET_KEY
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
# app.config['SECRET_KEY'] = 'your_secret_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/etsaboDB'  # Remplacez avec vos informations d'identification MySQL
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)



app.config['SECRET_KEY'] = '794b05a8a28df217be8ad971574efd1c4cbfe430c76048ab2e5825c81a958a8e'

bcrypt = Bcrypt(app)

# Configuration de la connexion MySQL
connection = mysql.connector.connect(
  host='localhost',
  user='root',
  password='',
  database='etsabodb'
)
cursor = connection.cursor()

#######################################################
class RegistrationForm(FlaskForm):
    # ...

    def validate_username(self, username):
        # Vérifier si le nom d'utilisateur est déjà utilisé
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username.data,))
        if cursor.fetchone():
            raise ValidationError('Ce nom d\'utilisateur est déjà utilisé. Veuillez en choisir un autre.')

    def validate_email(self, email):
        # Vérifier si l'e-mail est déjà utilisé
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email.data,))
        if cursor.fetchone():
            raise ValidationError('Cet e-mail est déjà utilisé. Veuillez en choisir un autre.')

    def save_user(self):
        # Enregistrer l'utilisateur dans la base de données
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        hashed_password = bcrypt.generate_password_hash(self.password.data).decode('utf-8')
        cursor.execute(query, (self.username.data, self.email.data, hashed_password))
        connection.commit()

##########################      

@app.route('/api/registration', methods=['GET', 'POST'])
def registration():
    registration_form = RegistrationForm()
    # login_form = LoginForm()

    if registration_form.validate_on_submit():
        registration_form.save_user()
        flash('Account created successfully!', 'success')
        return redirect(url_for('home'))
   
    # ...

@app.route('/')
def home():
    return ''

#######################################################
@app.route('/api/login', methods=['POST'])
def login():
    # Récupérer les données d'identification de l'utilisateur depuis la requête POST
    username = request.json['username']
    password = request.json['password']

    # Vérifier les informations d'identification dans la base de données
    cur = connection.cursor()
    cur.execute("SELECT username,password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    connection.close()

    if user:
        # Vérifier le mot de passe
        if password == user[1]:
            # if password == user['password']:
            # Authentification réussie
            response = {
                'success': True,
                'message': 'Authentification réussie',
                'token': 'abc123'  # Exemple de jeton d'accès généré
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

if __name__ == '__main__':
    app.run()