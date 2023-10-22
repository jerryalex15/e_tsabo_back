from flask import Blueprint, flash, request, redirect, url_for, jsonify,current_app
from flask_cors import cross_origin
from database import create_new_connection

doctor_route = Blueprint('doctor', __name__)
@cross_origin()
@doctor_route.route('/api/doctor_route/listdocs', methods=['GET'])
def getListDocs():
    try:
        connection = create_new_connection()
        cur = connection.cursor()
        cur.execute("SELECT id,name,specialite FROM users WHERE isDoc = 1")
        doctors = cur.fetchall();
        cur.close()
        connection.close()

        if doctors:
            response = {
                'success' : True,
                'doctors' : doctors
            }
        else:
            response = {
                'success' : False,
                'message' : "Il n'y a pas de docteur disponible "
            }
        return jsonify(response)
        
    except Exception as e:
        error_message = str(e)
        current_app.logger.error(f'Erreur lors de la récupération des docteurs : {e}')
        return jsonify({'error': error_message}), 500