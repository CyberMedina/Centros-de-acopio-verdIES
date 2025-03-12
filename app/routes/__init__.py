from app.routes.main_routes import bp as main_bp
from app.routes.api_routes import bp as api_bp
from app.routes.yolo_routes import yolo_bp

def register_blueprints(app):
    """
    Registra todos los blueprints de la aplicación.
    """
    app.logger.info("Registrando blueprints...")
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(yolo_bp, url_prefix='/yolo')
    app.logger.info(f"Blueprint registrado: {main_bp.name} con prefijo: {main_bp.url_prefix or '/'}")
    app.logger.info(f"Blueprint registrado: {api_bp.name} con prefijo: {api_bp.url_prefix or '/'}")
    app.logger.info(f"Blueprint registrado: yolo con prefijo: /yolo")
