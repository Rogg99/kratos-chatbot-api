from rest_framework import status, viewsets
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import FAQ, ChatMessage, ChatbotSession, UserFeedback
from .serializers import FAQSerializer, ChatMessageSerializer, ChatbotSessionSerializer, UserFeedbackSerializer

class FAQViewSet(viewsets.ModelViewSet):
    permission_classes([IsAuthenticated])
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

class ChatbotSessionViewSet(viewsets.ModelViewSet):
    permission_classes([IsAuthenticated])
    queryset = ChatbotSession.objects.all()
    serializer_class = ChatbotSessionSerializer