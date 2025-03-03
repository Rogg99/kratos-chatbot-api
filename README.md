# KRATOS TEST CHATBOT BACKEND

## Name

Kratos Test Chatbot API

## Description

Ce projet decline le backend du chatbot de test de l'entreprise KRATOS Inc.


## Prerequis
- Docker v4.35 or later


## Installation

- docker compose build

- docker compose up server

### make migration

- docker compose run --rm -it django makemigrations

### migrate

- docker compose run --rm -it django migrate

### telecharger les bibliotheques nltk necessaire au fonctionnement du NLP

- docker compose run --rm -it django initialize_nltk

### charger les données de test dont le compte admin
- docker compose run --rm -it django initialize_datas
 
### URLs

- console d'administration django
    - URL:  http://localhost:7898/chatbot/v1/admin/ 
    - username: admin
    - password: admin

- url de creation de session de chat:
    - POST http://localhost:7898/chatbot/v1/chat/start-session/ AUTHORIZATION BEARER reçu de l'API de Payment.
    - Reponse : {
        'session_id':'145e51-e4521-e45e12'
    }
    
- url d'envoi de message au chatbot:
    - POST http://localhost:7898/chatbot/v1/chat/send-message/ AUTHORIZATION BEARER reçu de l'API de Payment. 
        body :{
            'session_id':'145e51-e4521-e45e12',
            'message':'Bonjour'
        }
    - Reponse : {
        "id": 23,
        "archived": false,
        "created_at": "2025-03-02T20:26:37.172271Z",
        "updated_at": "2025-03-02T20:26:37.172290Z",
        "sender": "bot",
        "message": "Bonjour ! Je suis Coco, comment puis-je vous aider aujourd'hui ?",
        "session": "ba653ca2-7e24-40b5-939f-fd62e28838bc"
    }
