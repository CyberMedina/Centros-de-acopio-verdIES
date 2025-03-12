import os

class Config:
    # Configuración básica
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-temporal')
    
    # Configuración de la aplicación
    HOST = os.environ.get('HOST', '127.0.0.1')
    PORT = int(os.environ.get('PORT', 8002))
    
    # Configuración de la base de datos
    DATABASE_URL = os.environ.get('DATABASE_URL', '')
    
    # Configuración de OpenAI
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    
    # Configuración de seguridad
    SECRET_CODE = os.environ.get('SECRET_CODE', '')
    
    # Configuración de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

    # Añade aquí otras configuraciones necesarias 