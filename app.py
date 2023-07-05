from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_cors import CORS
import mysql.connector
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
# app.config['SECRET_KEY'] = 'your_secret_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/etsaboDB'  # Remplacez avec vos informations d'identification MySQL
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)



app.config['SECRET_KEY'] = 'your_secret_key'
bcrypt = Bcrypt(app)

# Configuration de la connexion MySQL
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="etsabodb"
)
cursor = db.cursor()



# @app.route("/<name>")
# def hello(name):
#     return f"Hello, {escape(name)}!"


    # class User(db.Model):
    # idPerson = db.Column(db.Integer, primary_key=True)
    # namePerson = db.Column(db.String(255), unique=False, nullable=False)
    # username = db.Column(db.String(255), unique=True, nullable=False)
    # emailAddress = db.Column(db.String(255), unique=True, nullable=False)
    # password = db.Column(db.String(255), nullable=False)
    # birthdate = db.Column(db.Date, nullable=False)
    # gender = db.Column(db.Boolean, nullable=False) #M: 1 ; F:0
        

    # def __repr__(self):
    #     return f"User('{self.username}', '{self.emailAddress}')"


# class RegistrationForm(FlaskForm):
#     # ...

#     def validate_username(self, username):
#         # Vérifier si le nom d'utilisateur est déjà utilisé
#         user = User.query.filter_by(username=username.data).first()
#         if user:
#             raise ValidationError('Ce nom d\'utilisateur est déjà utilisé. Veuillez en choisir un autre.')

#     def validate_email(self, emailAddress):
#         # Vérifier si l'e-mail est déjà utilisé
#         user = User.query.filter_by(emailAddress=emailAddress.data).first()
#         if user:
#             raise ValidationError('Cet e-mail est déjà utilisé. Veuillez en choisir un autre.')

#     def save_user(self):
#         # Enregistrer l'utilisateur dans la base de données
#         hashed_password = bcrypt.generate_password_hash(self.password.data).decode('utf-8')
#         user = User(username=self.username.data, emailAddress=self.email.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()

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
        db.commit()

##########################      

@app.route('/', methods=['GET', 'POST'])
def home():
    registration_form = RegistrationForm()
    # login_form = LoginForm()

    if registration_form.validate_on_submit():
        registration_form.save_user()
        flash('Account created successfully!', 'success')
        return redirect(url_for('home'))
    return "eto isika izao"
    # ...

#######################################################
@app.route('/login', methods=['POST'])
def login():
    # Récupérer les données d'identification de l'utilisateur depuis la requête POST
    username = request.json['username']
    password = request.json['password']

    # Vérifier les informations d'identification dans la base de données
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user:
        # Vérifier le mot de passe
        if password == user['password']:
            # Authentification réussie
            return jsonify({'message': 'Login successful'})
        else:
            # Mot de passe incorrect
            return jsonify({'message': 'Invalid password'})
    else:
        # Utilisateur non trouvé
        return jsonify({'message': 'User not found'})
