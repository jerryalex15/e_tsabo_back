from flask import Flask, render_template,request, jsonify
from flask_cors import CORS
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from routes.user_route import user_route
from routes.doctor_route import doctor_route
from decouple import Config,Csv
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
import logging      
from database import create_new_connection            

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

# @app.route('/api/doctor_route/listdocs', methods=['GET'])
# def getListDocs():
#     try:
#         connection = create_new_connection()
#         cur = connection.cursor()
#         cur.execute("SELECT id,name,spectialite FROM users WHERE isDoc = 1")
#         doctors = cur.fetchall();
#         cur.close()
#         connection.close()

#         if doctors:
#             response = {
#                 'success' : True,
#                 'doctors' : doctors
#             }
#         else:
#             response = {
#                 'success' : False,
#                 'message' : "Il n'y a pas de docteur disponible "
#             }
#             return jsonify(response)
        
#     except Exception as e:
#         error_message = str(e)
#         app.logger.error(f'Erreur lors de la récupération des docteurs : {e}')
#         return jsonify({'error': error_message}), 500
            
app.register_blueprint(user_route)
app.register_blueprint(doctor_route)

if __name__ == '__main__':
    app.run()