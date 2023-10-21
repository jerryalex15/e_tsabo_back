from flask import Flask, render_template
from flask_cors import CORS
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from routes.user_route import user_route
from decouple import Config,Csv
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
import logging                  

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
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


app.register_blueprint(user_route)

if __name__ == '__main__':
    app.run()