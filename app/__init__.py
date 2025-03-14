from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from config.settings import Config
import os

# Crear la instancia de SocketIO fuera de la función para que sea accesible globalmente
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Cargar configuración desde objeto Config y variables de entorno
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-secreta-temporal')
    
    # Configurar CORS
    CORS(app)
    
    # Inicializar SocketIO con la aplicación
    socketio.init_app(app)
    
    # Configurar logging
    from config.logging_config import configure_logging
    configure_logging(app)
    
    # Registrar blueprints
    from app.routes import register_blueprints
    register_blueprints(app)
    
    # Imprimir rutas registradas para depuración
    app.logger.info("Rutas registradas:")
    for rule in app.url_map.iter_rules():
        app.logger.info(f"{rule.endpoint}: {rule.rule}")
    
    return app