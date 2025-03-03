from django.contrib import admin
from .models import (
    ChatbotSession, ChatMessage, FAQ, UserFeedback
)

# Personnalisation de l'interface d'administration pour chaque modèle

@admin.register(ChatbotSession)
class ChatbotSessionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'id', 'created_at')
    search_fields = ('id',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'sender', 'message', 'created_at')
    # search_fields = ('session__session_id', 'message')
    list_filter = ('sender', 'created_at')

# Vous pouvez ajouter d'autres modèles dans le même style.
