import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Configuration class to manage environment variables.
    """
    # core settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    # debug mode
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    TESTING = os.getenv('TESTING', 'False').lower() in ('true', '1', 't')

    # database settings
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() in ('true', '1', 't')

    # task queue settings
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

    # crawler settings
    CRAWL_DELAY = int(os.getenv('CRAWL_DELAY', '30'))
    FEEDS_PER_DAY = int(os.getenv('FEEDS_PER_DAY', '10'))


class ProductionConfig(Config):
    """
    Production configuration.
    """
    DEBUG = False
    TESTING = False
