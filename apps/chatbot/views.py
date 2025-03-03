from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import FAQ, ChatMessage, ChatbotSession, UserFeedback
from .serializers import FAQSerializer, ChatMessageSerializer, ChatbotSessionSerializer, UserFeedbackSerializer
from .utils.chat_utils import handle_message
from django.conf import settings
import requests
import logging

# Configuration du logger
logger = logging.getLogger('db')

# URL de l'API de paiement
PAYMENT_API = "https://192.168.1.162:454/kratos-payment/api/v1/"

def authenticate(request):
    """
    Authentifie un utilisateur via l'API externe.
    
    Args:
        request (HttpRequest): La requête HTTP contenant les en-têtes d'authentification.
    
    Returns:
        dict | None: Les données de l'utilisateur si l'authentification réussit, sinon None.
    """
    user = None
    auth_header = request.META.get('HTTP_AUTHORIZATION')  # Récupération de l'en-tête Authorization

    if not auth_header:
        return None  # Retourne None si aucun en-tête Authorization n'est présent

    headers = {
        "Authorization": auth_header,
        "X-Kratos-Key": "2025@@@sign-kr@t0$"
    }

    try:
        response = requests.get(
            PAYMENT_API + 'auth/profile/', 
            verify=False,  # Désactive la vérification SSL (à éviter en production)
            headers=headers
        )
        
        logger.debug(f"Réponse de la requête: {response.text}")  # Log de la réponse API

        data = response.json()
        return data  # Retourne les données de l'utilisateur
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de la requête: {e}")  # Log des erreurs de requête
    except ValueError:
        logger.error("Réponse JSON invalide")  # Gestion des réponses JSON non valides

    return user

@api_view(['POST'])
def start_chatbot_session(request):
    """
    Démarre une nouvelle session de chatbot pour un utilisateur authentifié.
    
    Args:
        request (HttpRequest): La requête HTTP contenant les informations de l'utilisateur.
    
    Returns:
        Response: Réponse contenant l'ID de la session créée ou un message d'erreur.
    """
    user = authenticate(request=request)
    if user is not None:
        user_id = user.get('id')
        if user_id:
            session = ChatbotSession.objects.create(user_id=user_id)
            return Response({'session_id': session.pk}, status=status.HTTP_201_CREATED)
        return Response({"error": "user_id et session_id sont requis"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Échec d'authentification de l'utilisateur"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_message(request):
    """
    Gère l'envoi d'un message à la session chatbot et récupère la réponse du bot.
    
    Args:
        request (HttpRequest): La requête HTTP contenant le message de l'utilisateur et l'ID de session.
    
    Returns:
        Response: Réponse contenant le message du chatbot ou un message d'erreur.
    """
    session_id = request.data.get('session_id')
    message = request.data.get('message')

    user = authenticate(request=request)
    if user is None:
        return Response({"error": "Utilisateur non reconnu par le système"}, status=status.HTTP_400_BAD_REQUEST)

    user_id = user['id']

    if session_id and message:
        try:
            session = ChatbotSession.objects.get(id=session_id)
            
            # Sauvegarde du message utilisateur
            ChatMessage.objects.create(session=session, sender='user', message=message)
            
            # Génération de la réponse du chatbot
            answer = handle_message(message, session=session, authorization=request.META.get('HTTP_AUTHORIZATION'))
            
            # Sauvegarde du message du bot
            bot_message = ChatMessage.objects.create(session=session, sender='bot', message=answer)
            
            return Response(ChatMessageSerializer(bot_message).data, status=status.HTTP_201_CREATED)
        except ChatbotSession.DoesNotExist:
            return Response({"error": "Session introuvable"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(str(e))
            return Response({"error": "Erreur inattendue lors du traitement"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"error": "session_id et message sont requis"}, status=status.HTTP_400_BAD_REQUEST)
