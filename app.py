from flask import Flask, render_template, session, request, jsonify
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
app = Flask(__name__)
CORS(app)
from dotenv import load_dotenv


from models.api import *
from models.creacion_qr import *

load_dotenv()

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
    print(url_codigo_qr)



    datos_inicio = {
        "qr": url_codigo_qr,
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
    socketio.emit('redireccion', {'url': 'http://127.0.0.1:8002/conteo_residuos'})

    return jsonify({'message': 'Datos guardados en sesión correctamente.'})


@app.route('/conteo_residuos', methods=['GET','POST'])
def conteo_residuos():

    clasificacion_residuos = obtener_clasificacion_residuos()
    
    print(clasificacion_residuos)

    datos_inicio = {
        "clasificacion_residuos": clasificacion_residuos,
    }

    return render_template('conteo_residuos.html', **datos_inicio)




    




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8002, debug=True)
 