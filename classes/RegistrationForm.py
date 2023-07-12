from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

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
