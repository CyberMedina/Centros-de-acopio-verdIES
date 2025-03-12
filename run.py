from dotenv import load_dotenv
import os
from app import create_app, socketio

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación
app = create_app()

# Configurar eventos de SocketIO
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

@socketio.on('redireccion')
def handle_redireccion(data):
    # Reenviar el evento de redirección a todos los clientes
    socketio.emit('redireccion', data)

@socketio.on('deteccion_residuo')
def handle_deteccion_residuo(data):
    # Reenviar el evento de detección de residuo a todos los clientes
    socketio.emit('deteccion_residuo', data)

if __name__ == '__main__':
    # Ejecutar la aplicación con SocketIO
    port = int(os.environ.get('PORT', 8002))
    host = os.environ.get('HOST', '127.0.0.1')
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"Iniciando aplicación en {host}:{port} (Debug: {debug})")
    socketio.run(app, host=host, port=port, debug=debug)
