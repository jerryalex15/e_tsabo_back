from flask import Flask, render_template,request, jsonify
from flask_cors import CORS
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from routes.user_route import user_route
from decouple import Config,Csv
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
import logging

from config import config
from flask_mail import Mail, Message

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'fyfedsqdohazjepoka785'
app.config['DEBUG'] = True
app.config['JWT_TOKEN_LOCATION'] = ['headers']
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
# Configuration de la journalisation
app.logger.setLevel(logging.INFO)  # Niveau de journalisation (par exemple, INFO, DEBUG, ERROR)
app.logger.addHandler(logging.StreamHandler())  # Enregistrement des journaux dans la sortie standard (console)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
app.logger.addHandler(handler)

#Utilsation de email 
app.config.from_object(config)
mail = Mail(app)

@app.route('/send', methods=['POST'])
def send():
    if request.method == 'POST':
        email_data = request.get_json()
        subject = email_data.get('subject')
        recipient = email_data.get('recipient')
        message = email_data.get('message')

        msg = Message(subject, recipients=[recipient])
        msg.body = message

        try:
            mail.send(msg)
            response = {"message": "E-mail envoyé avec succès"}
            return jsonify(response), 200
        except Exception as e:
            error_message = str(e)
            response = {"error": error_message}
            return jsonify(response), 500

            
app.register_blueprint(user_route)

if __name__ == '__main__':
    app.run()