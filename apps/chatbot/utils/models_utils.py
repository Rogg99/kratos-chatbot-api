import os
import pickle
import random
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
from django.conf import settings
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer


def download_nltk_libraries():
    """
    Télécharge les ressources NLTK nécessaires à l'analyse de texte.
    """
    print('Téléchargement des ressources NLTK nécessaires ...')
    nltk.download('punkt')
    nltk.download('stopwords')
    print('Téléchargement terminé')


def preprocess_text(text):
    """
    Prétraite le texte en le tokenisant, en supprimant les stopwords et la ponctuation.
    
    Args:
        text (str): Texte brut en entrée.
    
    Returns:
        str: Texte nettoyé et filtré.
    """
    # Tokenisation du texte en minuscules
    tokens = word_tokenize(text.lower())
    
    # Suppression des stopwords et de la ponctuation
    stop_words = set(stopwords.words('french') + list(string.punctuation))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    
    return ' '.join(filtered_tokens)


def answer_question(user_input):
    """
    Répond à une question utilisateur en classifiant son entrée.
    
    Args:
        user_input (str): Message de l'utilisateur.
    
    Returns:
        str: Catégorie prédite de la question.
    """
    # Chargement du classificateur entraîné
    with open(settings.MODELS_ROOT + '/coco_classifier.pickle', 'rb') as f:
        classifier = pickle.load(f)
    
    # Chargement du vectorizer utilisé pour la transformation des textes
    with open(settings.MODELS_ROOT + '/coco_vectorizer.pickle', 'rb') as f:
        vectorizer = pickle.load(f)
    
    # Prétraitement de l'entrée utilisateur
    preprocessed_input = preprocess_text(user_input)
    
    # Transformation en vecteur de caractéristiques
    input_vector = vectorizer.transform([preprocessed_input])
    
    # Prédiction de la catégorie du message
    predicted_category = classifier.predict(input_vector)[0]
    
    return predicted_category
