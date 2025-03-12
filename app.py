import base64
from openai import OpenAI
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from models.creacion_qr import *
from models.api import *
from prompts import *
from flask import Flask, render_template, session, request, jsonify
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
import json as json_lib  # Renombrado para evitar conflictos con el nombre `json`
from info_centro_acopio import materiales_aceptados

app = Flask(__name__)
CORS(app)

MAX_COUNT = 10
num_intentos = 0

# Cargar la clave de API de OpenAI desde el archivo .env
load_dotenv()
OpenAIKEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


app.secret_key = 'superkey'
socketio = SocketIO(app)




@app.route('/')
def index():

    datos_acopio = obtener_detalle_centro_acopio('1')

    datos_inicio = {
        "datos_acopio": datos_acopio,
    }

    return render_template('index.html', **datos_inicio)


@app.route('/proceso_acopios', methods=['GET'])
def proceso_acopios():
    datos_acopio = obtener_detalle_centro_acopio('1')
    url_codigo_qr = creacion_qr_json(datos_acopio)
    
    datos_inicio = {
        "qr": url_codigo_qr,
        "materiales": materiales_aceptados["materiales_aceptados"]  # Usamos la estructura correcta
    }

    return render_template('proceso_acopio.html', **datos_inicio)


@app.route('/inicio_sesion', methods=['POST'])
@cross_origin()
def inicio_sesion():

    data = request.get_json()

    print(data)

    if data.get('id_centro_acopio') is None or data.get('id_user') is None or data.get('nombre_user') is None:
        return jsonify({'message': 'Datos incompletos.'}), 400

    id_user = data.get('id_user')
    nombre_user = data.get('nombre_user')
    id_centro_acopio = data.get('id_centro_acopio')

    # Guardar los datos en sesión
    session['id_user'] = id_user
    session['nombre_user'] = nombre_user

    print(session)

    # Emitir un evento de socket sin el argumento 'broadcast'
    socketio.emit('redireccion', {
                  'url': 'http://127.0.0.1:8002/conteo_residuos'})

    return jsonify({'message': 'Datos guardados en sesión correctamente.'})



# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def enviar_imagen_a_modelo(base64_image):
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


residuos_clasificados = []

@app.route('/test_envio', methods=['POST'])
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
        print(json_response)  # Asegúrate de que esto imprime un diccionario

        if 'id' in json_response:
            residuos_clasificados_temp = {
                'id': json_response['id'],
                'nombre': json_response['nombre'],
                'img_url': 'url',  # Aquí se agregará la función para obtener la imagen de esa categoría luego
                'cantidad': json_response['cantidad']
            }
            residuos_clasificados.append(residuos_clasificados_temp)
        elif 'error' in json_response:
            residuos_clasificados_temp = json_response


        # Emitir un evento de socket sin el argumento 'broadcast'
        socketio.emit('deteccion_residuo', json.dumps(residuos_clasificados_temp))

        print(residuos_clasificados_temp)
        print(residuos_clasificados)
        return jsonify(residuos_clasificados_temp), 200
    except Exception as e:
        print(f"Error al enviar imagen: {e}")
        return jsonify({"error": "Hubo un problema al clasificar la imagen"}), 500

@app.route('/conteo_residuos', methods=['GET', 'POST'])
def conteo_residuos():

    clasificacion_residuos = obtener_clasificacion_residuos()

    print(clasificacion_residuos)

    datos_inicio = {
        "clasificacion_residuos": clasificacion_residuos,
    }

    return render_template('conteo_residuos.html', **datos_inicio)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8002, debug=True)
