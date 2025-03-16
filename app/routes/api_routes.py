import base64
import json as json_lib
from flask import Blueprint, request, jsonify, session, current_app
from flask_cors import cross_origin
from app.models.api import obtener_detalle_centro_acopio
from app.prompts import generar_prompt_clasificador
from openai import OpenAI
import os
from .. import socketio  # Importar socketio desde la instancia de la app

bp = Blueprint('api', __name__, url_prefix='/api')

# Variables globales
MAX_COUNT = 10
num_intentos = 0
residuos_clasificados = []

# Cliente OpenAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

@bp.route('/inicio_sesion', methods=['POST'])
@cross_origin()
def inicio_sesion():
    data = request.get_json()

    if data.get('id_centro_acopio') is None or data.get('id_user') is None or data.get('nombre_user') is None:
        return jsonify({'message': 'Datos incompletos.'}), 400

    id_user = data.get('id_user')
    nombre_user = data.get('nombre_user')
    id_centro_acopio = data.get('id_centro_acopio')

    # Guardar los datos en sesión
    session['id_user'] = id_user
    session['nombre_user'] = nombre_user

    # La emisión del evento de socket se manejará en el archivo run.py
    return jsonify({'message': 'Datos guardados en sesión correctamente.'})

@bp.route('/test_envio', methods=['POST'])
@cross_origin()
def test_envio():
    global num_intentos
    global residuos_clasificados
    num_intentos += 1
    data = request.get_json()

    # Validar que el número de intentos no exceda MAX_COUNT
    if num_intentos > MAX_COUNT:
        return jsonify({"error": "Número máximo de intentos alcanzado"}), 400

    if 'img' not in data:
        return jsonify({"error": "Imagen no encontrada en los datos"}), 400

    # Decodificar imagen en base64 si viene como tal
    image_data = data['img']

    # Obtener clasificación
    try:
        json_response = enviar_imagen_a_modelo(image_data)
        print("Respuesta del modelo:", json_response)  # Debug

        # Si la respuesta es una lista, tomar el primer elemento
        if isinstance(json_response, list):
            if len(json_response) > 0:
                json_response = json_response[0]
            else:
                return jsonify({"error": "Respuesta vacía del modelo"}), 500

        if 'id' in json_response:
            # Obtener la URL de la imagen correspondiente al ID
            imagen_url = obtener_imagen_por_id(json_response['id'])
            
            residuos_clasificados_temp = {
                'id': json_response['id'],
                'nombre': json_response['nombre'],
                'img_url': imagen_url,
                'cantidad': json_response['cantidad']
            }
            residuos_clasificados.append(residuos_clasificados_temp)
            
            # Emitir el evento socket con los datos
            print("Emitiendo evento socket con:", residuos_clasificados_temp)  # Debug
            socketio.emit('deteccion_residuo', json_lib.dumps(residuos_clasificados_temp))
            
        elif 'error' in json_response:
            residuos_clasificados_temp = json_response

        return jsonify(residuos_clasificados_temp), 200
    except Exception as e:
        print(f"Error al enviar imagen: {e}")
        return jsonify({"error": "Hubo un problema al clasificar la imagen"}), 500
    
def obtener_imagen_por_id(id):
    # Mapeo de IDs a nombres de archivos de imagen
    imagenes = {
        1: "aluminio.png",
        2: "botellas_plastico.png",
        3: "tapas_botellas.png",
        4: "vidrio.png",
        5: "lamparas.png",
        6: "llantas.png",
        7: "papel_carton.png"
    }
    
    return imagenes.get(id, "default.png")

def enviar_imagen_a_modelo(base64_image):
    prompt_clasificador = generar_prompt_clasificador()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_clasificador,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low",
                        },
                    },
                ],
            }
        ],
    )

    # Extraer solo el contenido JSON del mensaje
    json_content = response.choices[0].message.content

    # Quitar los delimitadores de código (```json y ```)
    json_content = json_content.strip('```json').strip('```')

    # Parsear el contenido como JSON
    try:
        classification = json_lib.loads(json_content)
    except json_lib.JSONDecodeError:
        print("Error al parsear JSON.")
        return {"error": "Error al parsear JSON de la respuesta"}

    return classification 