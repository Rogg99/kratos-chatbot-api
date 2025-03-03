import os
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
from django.conf import settings
import string
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import random
import nltk

def download_nltk_libraries():
    # Télécharger les ressources NLTK nécessaires
    print('Téléchargement des ressources NLTK nécessaires ...')
    nltk.download('punkt')
    nltk.download('stopwords')
    print('Téléchargement terminé')



def preprocess_text(text):
    
    # Tokenize the text into individual words
    tokens = word_tokenize(text.lower())
    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('french') + list(string.punctuation))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    # Return the filtered tokens as a string
    return ' '.join(filtered_tokens)

# Define a function to generate a chatbot response
def answer_question(user_input):
    # Preprocess and tokenize the user inputimport pickle
    f = open(settings.MODELS_ROOT+'/coco_classifier.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()
    f = open(settings.MODELS_ROOT+'/coco_vectorizer.pickle', 'rb')
    vectorizer = pickle.load(f)
    f.close()
    preprocessed_input = preprocess_text(user_input)
    input_vector = vectorizer.transform([preprocessed_input])
    predicted_category = classifier.predict(input_vector)[0]
    
    return predicted_category
