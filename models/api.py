import requests
from flask import jsonify

def obtener_detalle_centro_acopio(id):
    # URL de la API
    url = f"http://127.0.0.1:8000/api/v1/centroacopios/{id}"
    
    # Data que enviarías en el POST (si hay alguna)
    data = {}  # Si no necesitas enviar data, deja esto vacío
    
    # Realizar el POST
    response = requests.get(url, json=data)
    
    # Obtener el JSON de la respuesta
    response_json = response.json()
    
    return response_json


def obtener_clasificacion_residuos():
    # URL de la API
    url = "http://127.0.0.1:8000/api/v1/materiales"

    # Data que enviarías en el POST (si hay alguna)
    data = {}  # Si no necesitas enviar data, deja esto vacío

    # Realizar el POST
    response = requests.get(url, json=data)

    # Obtener el JSON de la respuesta
    response_json = response.json()

    return response_json
