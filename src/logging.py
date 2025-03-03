import logging
from elasticsearch import Elasticsearch
from logging.handlers import TimedRotatingFileHandler

class ElasticsearchHandler(logging.Handler):
    """Custom log handler for sending logs to Elasticsearch"""
    def __init__(self, hosts):
        super().__init__()
        self.client = Elasticsearch(hosts)

    def emit(self, record):
        log_entry = self.format(record)
        self.client.index(index="django-logs", document={"message": log_entry})