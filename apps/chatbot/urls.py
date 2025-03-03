from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import start_chatbot_session, send_message
from .viewsets import *

router = DefaultRouter()

urlpatterns = [
    path('start-session/', start_chatbot_session, name='start-chatbot-session'),
    path('send-message/', send_message, name='send-chatbot-message'),
]
