import os
import logging
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    """
    Configura el sistema de logging para la aplicación.
    """
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
    
    # Asegurarse de que existe el directorio de logs
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configurar el handler para archivo
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(log_level)
    
    # Configurar el handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    console_handler.setLevel(log_level)
    
    # Añadir los handlers al logger de la aplicación
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)
    
    # Mensaje de inicio
    app.logger.info('Aplicación iniciada con nivel de log: %s', app.config.get('LOG_LEVEL', 'INFO'))
    
    return app 