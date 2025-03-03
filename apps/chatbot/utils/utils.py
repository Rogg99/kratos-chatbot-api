from apps.api.models import FAQ
import pandas as pd 
import logging
logger = logging.getLogger('django')



def save_FAQ_from_file(filepath):
    try:
        df = pd.read_excel(filepath)
        for i in df.shape[0]:
            FAQ.objects.get_or_create(
                question = df[i]['question'],
                answer = df[i]['answer']
            )
    except Exception as e:
        logger.error(str(e))