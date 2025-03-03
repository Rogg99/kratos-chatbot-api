from rest_framework import status, viewsets
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import FAQ, ChatMessage, ChatbotSession, UserFeedback
from .serializers import FAQSerializer, ChatMessageSerializer, ChatbotSessionSerializer, UserFeedbackSerializer
from .utils.chat_utils import handle_message                                                                                                                                                                        
from django.conf import settings
import requests
import logging


logger = logging.getLogger('db')

PAYMENT_API = "https://192.168.1.162:454/kratos-payment/api/v1/"

def authenticate(request):
    user = None
    auth_header = request.META.get('HTTP_AUTHORIZATION')  # Use .get() to prevent KeyError

    if not auth_header:
        return None  # Return None if no Authorization header is present

    headers = {
        "Authorization": auth_header,
        "X-Kratos-Key": "2025@@@sign-kr@t0$"
    }

    try:
        response = requests.get(
            PAYMENT_API + 'auth/profile/', 
            verify=False,
            # verify=settings.CRT_PATH, 
            headers=headers
        )
        
        logger.debug(f"Request response: {response.text}")  # Log request errors

        # response.raise_for_status()  # Raises an error for HTTP errors (4xx, 5xx)

        data = response.json()
        id = data["id"]
        return data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")  # Log request errors
    except ValueError:
        logger.error("Invalid JSON response")  # Handle invalid JSON responses

    return user


@api_view(['POST'])
def start_chatbot_session(request):
    user = authenticate(request=request)
    # user = {
    #     'id':'uiojjh'
    # }
    if user!=None:
        user_id = user['id']
        if user_id:
            session = ChatbotSession.objects.create(user_id=user_id)
            return Response({'session_id': session.pk}, status=status.HTTP_201_CREATED)
        return Response({"error": "user_id and session_id are required"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Echec d'authentification de l'utilisateur"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_message(request):
    session_id = request.data.get('session_id')
    message = request.data.get('message')

    user = authenticate(request=request)
    if user == None:
        return Response({"error": "Utilisateur non reconnu par le système"}, status=status.HTTP_400_BAD_REQUEST)

    user_id = user['id']

    if session_id and message:
        try:
            session = ChatbotSession.objects.get(id=session_id)
            ChatMessage.objects.create(session=session, sender='user', message=message)
            answer = handle_message(message,session=session,authorization=request.META.get('HTTP_AUTHORIZATION'))
            bot_message = ChatMessage.objects.create(session=session, sender='bot', message=answer)
            return Response(ChatMessageSerializer(bot_message).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(str(e))
            return Response({"error": "unexpected error during processing "}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"error": "session_id, and message are required"}, status=status.HTTP_400_BAD_REQUEST)
