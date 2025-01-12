import os
from datetime import timedelta

class Config:
    # Application Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    TESTING = os.getenv('TESTING', 'False').lower() == 'true'
    
    # API Settings
    API_TITLE = 'AI Voice Chat API'
    API_VERSION = '1.0'
    OPENAPI_VERSION = '3.0.2'
    
    # Security Settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    
    # Database Settings
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_API_KEY = os.getenv('SUPABASE_API_KEY')
    SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    
    # AI Service Settings
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    
    # Audio Settings
    AUDIO_OUTPUT_DIR = 'temp_audio'
    AUDIO_CACHE_SIZE = 1000
    
    # Thread Pool Settings
    MAX_WORKERS = 12

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 