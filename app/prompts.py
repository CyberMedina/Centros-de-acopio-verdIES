from app.models.api import obtener_clasificacion_residuos

def generar_prompt_clasificador():
    # Obtenemos la clasificación de residuos desde la API
    tipos_de_objetos = obtener_clasificacion_residuos()

    # Inicializamos 'resultado' con un valor predeterminado
    resultado = "No se pudieron obtener las categorías"

    # Verificamos el tipo de datos que recibimos y extraemos las categorías
    if isinstance(tipos_de_objetos, dict):
        if 'materiales_aceptados' in tipos_de_objetos:
            categorias = tipos_de_objetos['materiales_aceptados']
            resultado = ", ".join(
                [f"id: {categoria['id']} nombre: {categoria['nombre'].lower()}" for categoria in categorias]
            )
        elif 'Categorias' in tipos_de_objetos:
            categorias = tipos_de_objetos['Categorias']
            resultado = ", ".join(
                [f"id: {categoria['id']} nombre: {categoria['nombre'].lower()}" for categoria in categorias]
            )
        else:
            print(f"Diccionario recibido sin claves esperadas: {list(tipos_de_objetos.keys())}")
    elif isinstance(tipos_de_objetos, list):
        try:
            resultado = ", ".join(
                [f"id: {categoria['id']} nombre: {categoria['nombre'].lower()}" for categoria in tipos_de_objetos]
            )
        except Exception as e:
            print(f"Error al procesar las categorías como lista: {e}")
    else:
        print(f"Tipo de datos recibido: {type(tipos_de_objetos)}")
        print(f"Contenido: {tipos_de_objetos}")

    # Construimos el prompt para la IA usando el resultado obtenido
    prompt_clasificador = f"""
Eres una IA especializada en la clasificación de imágenes de objetos reciclables. Tu tarea es analizar una foto y detectar los objetos presentes, clasificándolos según la siguiente lista:
{resultado}

Si en la imagen se detecta un objeto que no se encuentre en esta lista, debes devolver un JSON con la siguiente estructura:
{{{{"error": "el objeto no es clasificable porque es: [nombre del objeto]"}}}}

En el caso de objetos clasificables, responde únicamente con la clasificación en formato JSON. Cada objeto identificado debe expresarse de la siguiente forma:
{{
    "id": <identificador>,
    "nombre": "<nombre del objeto>",
    "cantidad": <cantidad de objetos detectados>
}}

No agregues ningún otro texto o formato adicional; la salida debe ser únicamente el/los JSON resultante(s).
"""
    print(prompt_clasificador)
    return prompt_clasificador

