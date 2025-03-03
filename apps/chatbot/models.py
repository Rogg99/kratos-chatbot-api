from django.db import models
from uuid import uuid4
from django.core.exceptions import ValidationError                                                                                                                                                                        
from django.conf import settings

# Classe de base pour ajouter des champs communs à tous les modèles
class BaseModel(models.Model):
    archived = models.BooleanField(default=False, help_text="Indique si l'enregistrement est archivé.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date de création de l'enregistrement.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date de la dernière modification.")

    class Meta:
        abstract = True
        ordering = ["-created_at"]


# Modèle pour les sessions du chatbot
class ChatbotSession(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_id = models.CharField(max_length=100,null=True, blank=True)

# Modèle pour les messages échangés avec le chatbot
class ChatMessage(BaseModel):
    session = models.ForeignKey(ChatbotSession,
                                on_delete=models.CASCADE, 
                                related_name='messages')
    sender = models.CharField(max_length=50, choices=[('user', 'Utilisateur'), ('bot', 'Chatbot')])
    message = models.TextField()

# Modèle pour les questions fréquentes (FAQ)
class FAQ(BaseModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()

# Modèle pour les retours des utilisateurs sur le chatbot
class UserFeedback(BaseModel):
    session = models.ForeignKey(ChatbotSession, on_delete=models.CASCADE)
    rating = models.IntegerField(help_text="Évaluation de l'utilisateur sur 5.")
    comment = models.TextField(null=True, blank=True, help_text="Commentaire optionnel.")


    

