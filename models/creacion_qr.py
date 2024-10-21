import qrcode
import json


from io import BytesIO
import base64

def creacion_qr_json(data):
    # Verificar que 'data' sea un diccionario antes de intentar serializarlo
    if not isinstance(data, dict):
        raise TypeError("El parámetro 'data' debe ser un diccionario.")

    try:
        # Convertir el diccionario a una cadena JSON
        json_data = json.dumps(data)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Error al convertir los datos a JSON: {e}")

    # Crear una instancia de QRCode
    qr = qrcode.QRCode(
        version=1,  # Tamaño del QR (1 es el más pequeño)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Nivel de corrección de errores
        box_size=10,  # Tamaño de cada "cuadrado" en el código QR
        border=4  # Tamaño del borde
    )

    # Añadir los datos al QR
    qr.add_data(json_data)
    qr.make(fit=True)

    # Crear la imagen del código QR
    img = qr.make_image(fill='black', back_color='white')

    # Convertir la imagen a bytes
    buffered = BytesIO()
    img.save(buffered, format="PNG")

    # Codificar la imagen en base64
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Retornar la imagen como una cadena base64 para incrustar en HTML
    return f"data:image/png;base64,{img_base64}"
