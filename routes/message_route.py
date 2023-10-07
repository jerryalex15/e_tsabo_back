from flask import Flask, jsonify, request, Blueprint
from database import connection
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


message_route = Blueprint('message', __name__,url_prefix='/api/messages')
# # Route principale des messages
# @message_route.route('/index')
# def index():
#     return "Bienvenue sur l'API de messagerie"

# Route pour récupérer tous les messages
# @message_route.route('/', methods=['GET'])
# def get_messages():
#     # Logique pour récupérer tous les messages depuis la base de données
#     messages = [...]  # Liste de messages
#     return jsonify(messages)

# Route pour envoyer un nouveau message
@message_route.route('/', methods=['POST'])
def send_message():
    data = request.get_json()
    # Logique pour enregistrer le nouveau message dans la base de données
    # Utilisation des données reçues dans 'data'
    return jsonify({'message': 'Message envoyé avec succès'})

# Route pour récupérer un message par son ID
@message_route.route('/<int:user_id>', methods=['GET'])
def get_message(user_id):
    # Logique pour récupérer le message avec l'ID spécifié depuis la base de données
    cur = connection.cursor()
    cur.execute("SELECT sender,receiver,content,sent_at FROM messages WHERE sender = %s", (user_id,))
    messages = cur.fetchall()
    cur.close()
    connection.close()
    
    return jsonify(messages)

# Route pour supprimer un message par son ID
@message_route.route('/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    # Logique pour supprimer le message avec l'ID spécifié de la base de données
    return jsonify({'message': 'Message supprimé avec succès'})


def send_email(expediteur, destinataire, sujet , contenu):
    #configuration du serveur smtp
    serveur_smtp = 'smtp.gmail.com'
    port_smtp = 465

    #création du message a envoyé
    message = MIMEMultipart()
    message['From'] = expediteur
    message['To'] = destinataire
    message['Subject'] = sujet

    #Cors du message
    message.attach(MIMEText(contenu,'plain'))

    #connexion au serveur SMTP de GMail
    with smtplib.SMTP_SSL(serveur_smtp, port_smtp) as server:
        try:
            # Création du contexte SSL
            server.login('nysandratra177@gmail.com','MIRANTSOA')

            server.sendmail(expediteur,destinataire,message.as_string())
            server.quit()
            return True

        except Exception as e:
            print(f"Erreur lors de l'envoi e-mail : {e}")
            return False



#Envoyer un email 
@message_route.route('/send_email', methods=['POST'])
def send_email_route():

    #paramètres de l'éxpéditeur et du serveur SMTP
    data = request.json
    destinataire = data['destinataire']
    objet = data['objet']
    contenu = data['contenu']
    expediteur = data['expediteur']

    if send_email(expediteur,destinataire,objet,contenu):

        return jsonify({"message":"votre bilan a été bien envoyé"}) 

    else:
        return jsonify({"message":"Erreur! votre bilan n'a pas été envoyé"})