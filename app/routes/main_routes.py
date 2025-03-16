from flask import Blueprint, render_template, session, jsonify, current_app
from app.models.api import obtener_detalle_centro_acopio, obtener_clasificacion_residuos
from app.models.creacion_qr import creacion_qr_json
from info_centro_acopio import materiales_aceptados
from flask_cors import cross_origin
from flask_socketio import emit
import os

# Crear el blueprint con un nombre y un prefijo de URL opcional
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Página principal de la aplicación."""
    try:
        datos_acopio = obtener_detalle_centro_acopio('1')
        datos_inicio = {
            "datos_acopio": datos_acopio,
        }
        current_app.logger.info("Renderizando página de inicio")
        return render_template('index.html', **datos_inicio)
    except Exception as e:
        current_app.logger.error(f"Error en la página de inicio: {str(e)}")
        return render_template('index.html', error=str(e))


@bp.route('/proceso_acopios', methods=['GET'])
def proceso_acopios():
    """Página de proceso de acopios."""
    try:
        datos_acopio = obtener_detalle_centro_acopio('1')
        url_codigo_qr = creacion_qr_json(datos_acopio)
        
        datos_inicio = {
            "qr": url_codigo_qr,
            "materiales": materiales_aceptados["materiales_aceptados"]
        }
        
        current_app.logger.info("Renderizando página de proceso de acopios")
        return render_template('proceso_acopio.html', **datos_inicio)
    except Exception as e:
        current_app.logger.error(f"Error en la página de proceso de acopios: {str(e)}")
        return render_template('proceso_acopio.html', error=str(e))


@bp.route('/conteo_residuos', methods=['GET', 'POST'])
def conteo_residuos():
    """Página de conteo de residuos."""
    try:
        clasificacion_residuos = obtener_clasificacion_residuos()
        
        datos_inicio = {
            "clasificacion_residuos": clasificacion_residuos,
        }
        
        current_app.logger.info("Renderizando página de conteo de residuos")
        return render_template('conteo_residuos.html', **datos_inicio)
    except Exception as e:
        current_app.logger.error(f"Error en la página de conteo de residuos: {str(e)}")
        return render_template('conteo_residuos.html', error=str(e))
