import nltk
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Initialize NLTK by downloading required datasets"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Downloading NLTK datasets..."))

        nltk.download('punkt')        # Tokenizer models
        nltk.download('punkt_tab')        # Tokenizer models
        nltk.download('stopwords')    # Stopwords for different languages
        
        self.stdout.write(self.style.SUCCESS("NLTK datasets downloaded successfully!"))
