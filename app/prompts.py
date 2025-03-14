from app.models.api import *

tipos_de_objetos = obtener_clasificacion_residuos()

# Inicializamos resultado con un valor predeterminado
resultado = "No se pudieron obtener las categorías"

# Verificamos el tipo de datos que recibimos
if isinstance(tipos_de_objetos, dict) and 'materiales_aceptados' in tipos_de_objetos:
    # Si es un diccionario con la clave 'materiales_aceptados'
    categorias = tipos_de_objetos['materiales_aceptados']
    resultado = ", ".join([f"id: {categoria['id']} nombre: {categoria['nombre'].lower()}" for categoria in categorias])
    print(resultado)
elif isinstance(tipos_de_objetos, dict) and 'Categorias' in tipos_de_objetos:
    # Si es un diccionario con la clave 'Categorias'
    categorias = tipos_de_objetos['Categorias']
    resultado = ", ".join([f"id: {categoria['id']} nombre: {categoria['nombre'].lower()}" for categoria in categorias])
    print(resultado)
elif isinstance(tipos_de_objetos, list):
    # Si es una lista de categorías
    try:
        resultado = ", ".join([f"id: {categoria['id']} nombre: {categoria['nombre'].lower()}" for categoria in tipos_de_objetos])
        print(resultado)
    except Exception as e:
        print(f"Error al procesar las categorías como lista: {e}")
else:
    # Si es otro tipo de dato (como una cadena)
    print(f"Tipo de datos recibido: {type(tipos_de_objetos)}")
    print(f"Contenido: {tipos_de_objetos}")

prompt_clasificador = f"""
Eres una IA que clasifica fotos de objetos en 
{resultado} o {{'error': 'el objeto no es clasificable'}}
Devuelve solo la clasificación en JSON unicamente genera la información del objeto y la cantidad de objetos en la imagen. Ejemplo:
{{
    "id": ,
    "nombre": "",
    "cantidad": 
}}
{{
    "id": ,
    "nombre": "",
    "cantidad": 
}}
"""
print(prompt_clasificador)