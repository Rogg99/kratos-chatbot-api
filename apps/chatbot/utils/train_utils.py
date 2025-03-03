
import pickle
import nltk
import os
import logging
from .models_utils import preprocess_text

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import random
import pandas as pd
import pickle
logger = logging.getLogger('django')


def train():
    # Télécharger les ressources NLTK nécessaires
    print('Téléchargement des ressources NLTK nécessaires ...')
    nltk.download('punkt')
    nltk.download('stopwords')
    print('Téléchargement terminé')

    # repositionnement dans le dossier du projet
    os.getcwd()
    os.chdir("D:\\Projects\\STEPS\\Kratos-chatbot-API\\chatbot-API")
    corpus = pd.read_excel("models/FAQ_EGOPASS.xlsx")

    # Separation du corpus
    texts, labels = corpus['Question'],corpus['Reponse']

    # Entrainement du Classifieur Multinomial Naive Bayes 
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)
    clf = MultinomialNB()
    clf.fit(X, labels)

    f = open('models/coco_classifier.pickle', 'wb')
    pickle.dump(clf, f)
    f.close()

    f = open('models/coco_vectorizer.pickle', 'wb')
    pickle.dump(vectorizer, f)
    f.close()

    print('Entrainement terminé')

