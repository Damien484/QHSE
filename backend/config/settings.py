"""
Configuration settings for the QHSE application
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Créer le dossier database s'il n'existe pas
    DATABASE_DIR = BASE_DIR / 'database'
    DATABASE_DIR.mkdir(exist_ok=True)

    # Construire l'URI de la base de données de manière compatible Windows/Linux
    # SQLite nécessite 3 slashes après sqlite: pour un chemin absolu
    DATABASE_PATH = DATABASE_DIR / 'qhse.db'

    # Utiliser as_posix() pour convertir les backslashes Windows en forward slashes
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{DATABASE_PATH.as_posix()}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    GENERATED_DOCS_FOLDER = os.path.join(BASE_DIR, 'generated_documents')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # CORS settings
    CORS_HEADERS = 'Content-Type'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
