import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from django.conf import settings
from chatbot.models import ChatbotSession, ChatMessage

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def mock_authenticate():
    with patch('chatbot.views.authenticate') as mock:
        mock.return_value = {'id': 'test_user_id'}
        yield mock

@pytest.mark.django_db
def test_start_chatbot_session_success(api_client, mock_authenticate):
    response = api_client.post('/api/start_chatbot_session/')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'session_id' in response.data

@pytest.mark.django_db
def test_start_chatbot_session_auth_failed(api_client):
    response = api_client.post('/api/start_chatbot_session/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "Echec d'authentification de l'utilisateur"

@pytest.mark.django_db
def test_send_message_success(api_client, mock_authenticate):
    session = ChatbotSession.objects.create(user_id='test_user_id')
    with patch('chatbot.views.handle_message', return_value='Réponse du bot'):
        response = api_client.post('/api/send_message/', {
            'session_id': session.id,
            'message': 'Bonjour'
        })
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['message'] == 'Réponse du bot'
        assert ChatMessage.objects.filter(session=session).count() == 2

@pytest.mark.django_db
def test_send_message_auth_failed(api_client):
    response = api_client.post('/api/send_message/', {
        'session_id': 1,
        'message': 'Bonjour'
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == "Utilisateur non reconnu par le système"

@pytest.mark.django_db
def test_send_message_missing_params(api_client, mock_authenticate):
    response = api_client.post('/api/send_message/', {'session_id': 1})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == "session_id, and message are required"
