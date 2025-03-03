import nltk
import re
import requests
from .models_utils  import answer_question
from apps.chatbot.models import ChatMessage,ChatbotSession                                                                                                                                                                
from django.conf import settings
import logging

nltk.download('punkt')

logger = logging.getLogger('django')

PAYMENT_API = "http://localhost:7899/kratos-payment/api/v1/api"
PAYMENT_STATUS_PATH = "/payments/"
PAYMENT_START_PATH = "/payments/"
PAYMENT_STOP_PATH = "/payments/stop/"
PAYMENT_SET_AMOUNT_PATH = "/payment/set-amount/"


# Fonction pour détecter l'intention
def detect_intent(message):
    intents = {
        "verifier_paiement": ["vérifier", "état", "paiement", "transaction", "statut"],
        "initier_paiement": ["initier", "payer", "effectuer", "paiement", "transaction"],
        "annuler_paiement": ["annuler", "supprimer", "retirer", "paiement", "transaction"],
        "modifier_montant_transaction": ["modifier", "changer", "montant", "paiement", "transaction"]
    }
    
    tokens = nltk.word_tokenize(message.lower())
    
    for intent, keywords in intents.items():
        if any(word in tokens for word in keywords):
            return intent
    
    return "autre"

# Fonction pour extraire le numéro de transaction
def extract_transaction_id(message):
    match = re.search(r'(\d{5,})', message)
    if match:
        return match.group(1)
    return None


def request_payment_api(endpoint,authorization,body = {},method='get'):
    response = requests.Response(400)
    try:
        headers = {
            "Authorization": authorization,
            "X-Kratos-Key": "2025@@@sign-kr@t0$"
        }
        if method == "get":
            params = "?"
            for key in body.keys():
                if len(params.split('='))>0:
                    params += "&"
                params += key+"="+body[key]
            response = requests.get(PAYMENT_API+endpoint+params, verify=settings.CRT_PATH,headers=headers)
        else:
            response = requests.post(PAYMENT_API+endpoint, verify=settings.CRT_PATH,json=body,headers=headers)
    except Exception as e:
        logger.error(str(e))
    return response


# Fonction pour vérifier l'état du paiement via une requête API
def verifier_etat_paiement(transaction_id,authorization):
    url = PAYMENT_STATUS_PATH + f"/{transaction_id}"
    try:
        response = request_payment_api(url,authorization)
        if response.status_code == 200:
            data = response.json()
            return f"Le statut de votre paiement est : {data['status']}"
        else:
            return "Désolé, je n'ai pas pu vérifier l'état de votre paiement."
    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la connexion au serveur : {e}"

# Fonction pour initier un paiement via une requête API
def initier_paiement(egopass_name,mode_paiment,telephone=''):
    url = PAYMENT_START_PATH
    body = {
        "egopass":egopass_name,
        "mode_paiment":mode_paiment,
        "telephone":telephone,
    } 
    try:
        response = request_payment_api(url,body=body,method='post')
        if response.status_code == 200:
            data = response.json()
            return f"Le paiement {data['id']} a été initié avec succès, veuiller confirmer la transaction sur votre terminal bancaire ou mobile {telephone}"
        else:
            return "Désolé, je n'ai pas pu initié votre paiement. Veuiller reessayer à nouveau."
    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la connexion au serveur : {e}"


# Fonction pour annuler un paiement via une requête API
def annuler_paiement(transaction_id):
    url = PAYMENT_STOP_PATH + f"/{transaction_id}/"
    try:
        response = request_payment_api(url,method="post")
        if response.status_code == 200:
            data = response.json()
            if {data['status']} == "success":
                return "Votre paiement a été annulé avec succès"
            else:
                return """Votre paiement n'a pas pu être annulé car la transaction n'est plus annulable automatiquement. 
                    Veuiller contacter le support client pour exprimer votre souci."""
        else:
            return "Désolé, je n'ai pas pu annuler votre paiement."
    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la connexion au serveur : {e}"


# Fonction pour modifier le montant d'un paiement via une requête API
def modifier_montant_transaction(transaction_id,montant):
    url = PAYMENT_SET_AMOUNT_PATH + f"/{transaction_id}/"
    body = {
        'amount':montant
    }
    try:
        response = request_payment_api(url,method="patch",body=body)
        if response.status_code == 200:
            data = response.json()
            if {data['status']} == "success":
                return f"Votre paiement a été modifié avec succès"
            else:
                return """Votre paiement n'a pas pu être modifié car la transaction n'est plus modifiable automatiquement. 
                    Veuiller contacter le support client pour exprimer votre souci."""
        else:
            return "Désolé, je n'ai pas pu modifier le montant de votre paiement."
    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la connexion au serveur : {e}"


# Fonction pour detecter l'intention du message precedent
def get_previous_intent(session:int):
    intent = None
    last_bot_message = ChatMessage.objects.filter(session=session,sender='bot')
    if last_bot_message:
        last_bot_message = last_bot_message.first().message
        if last_bot_message == "Pouvez-vous me donner le numéro de votre transaction ?":
            intent = 'verifier_paiement'
        if last_bot_message == "D'accord, quel montant souhaitez-vous payer et par quel moyen ?":
            intent = 'initier_paiement'
        if last_bot_message == "Quel est le numéro de la transaction que vous souhaitez annuler ?":
            intent = 'annuler_paiement'
        if last_bot_message == "Veuillez fournir le numéro de la transaction que vous souhaitez modifier.":
            intent = 'modifier_montant_transaction'

    return intent



# Fonction principale pour gérer le message utilisateur
def handle_message(message:str,session:ChatbotSession,authorization=None):
    TROUBLE_ANSWER = "Je ne suis pas sûr de comprendre. Pouvez-vous reformuler ?"
        
    if(message.isnumeric()):
        intent = detect_intent(message)
        if intent == "verifier_paiement":
            transaction_id = extract_transaction_id(message)
            if transaction_id:
                return verifier_etat_paiement(transaction_id,authorization)
            else:
                return "Pouvez-vous me donner le numéro de votre transaction ?"
        elif intent == "initier_paiement":
            return "D'accord, quel montant souhaitez-vous payer et par quel moyen ?"
        elif intent == "annuler_paiement":
            transaction_id = extract_transaction_id(message)
            if transaction_id:
                return f"Je vais annuler la transaction {transaction_id}."
            else:
                return "Quel est le numéro de la transaction que vous souhaitez annuler ?"
        elif intent == "modifier_montant_transaction":
            transaction_id = extract_transaction_id(message)
            if transaction_id:
                return f"Quel est le nouveau montant pour la transaction {transaction_id} ?"
            else:
                return "Veuillez fournir le numéro de la transaction que vous souhaitez modifier."
        else:
            return answer_question(message) 
    elif get_previous_intent(session.id)!=None:
        intent = get_previous_intent()
        if intent == "verifier_paiement":
            transaction_id = extract_transaction_id(message)
            if transaction_id:
                return verifier_etat_paiement(transaction_id)
            else:
                return TROUBLE_ANSWER
        if intent == "initier_paiement":
            transaction_id = extract_transaction_id(message)
            if transaction_id:
                return initier_paiement(transaction_id)
            else:
                return TROUBLE_ANSWER
        if intent == "annuler_paiement":
            transaction_id = extract_transaction_id(message)
            if transaction_id:
                return annuler_paiement(transaction_id)
            else:
                return TROUBLE_ANSWER
        if intent == "modifier_montant_transaction":
            transaction_id = extract_transaction_id(message)
            if transaction_id:
                return modifier_montant_transaction(transaction_id)
            else:
                return TROUBLE_ANSWER
    else:
        return answer_question(message) 

