<img src="https://github.com/CyberMedina/Centros-de-acopio-verdIES/blob/main/media/Banner%20VerdIes%20-%20Centro%20acopios.png?raw=true" width="1000">

# 🌍 Centro de Acopio Inteligente para VerdIES  

Prototipo de un centro de acopio inteligente para la aplicación **VerdIES**. Este proyecto permite clasificar materiales reciclables automáticamente mediante reconocimiento de objetos y procesamiento con IA.  

**[Repositorio de VerdIES](#)**  

## 📚 Tabla de Contenidos  
- [Cómo funciona](#-cómo-funciona)  
- [Características](#-características)  
- [Tecnologías Usadas](#-tecnologías-usadas)  
- [Instalación](#-instalación)  
- [Uso](#-uso)  
- [Contacto](#-contacto)  

---

## ⚙️ Cómo funciona  
1. En el archivo `info_centro_acopio.py` se encuentra un JSON que define los tipos de materiales aceptados en el centro de acopio.  
2. Se habilita la cámara y se usa la librería **YOLOv5** con un modelo genérico para reconocer objetos.  
3. Si un objeto es reconocido durante **más de 3 segundos**, se toma una foto y se envía a la API de **OpenAI** para clasificarlo según los materiales definidos en el JSON.  
4. El JSON de respuesta es procesado y se suman los materiales clasificados.  

---

## 🌟 Características  

### ✅ **Configuración de materiales**  
- El archivo `info_centro_acopio.py` permite modificar y definir los materiales aceptados en el centro de acopio.  
- La configuración es dinámica, por lo que puedes agregar o eliminar materiales fácilmente.
<img src="https://github.com/CyberMedina/Centros-de-acopio-verdIES/blob/main/media/Materiales%20aceptados.jpg?raw=true" width="400">  

### 🎯 **Reconocimiento de objetos**  
- Utiliza **YOLOv5** para detectar objetos en tiempo real mediante la cámara.  
- La detección es rápida y eficiente gracias al uso de **Pytorch**.  

### 📸 **Clasificación con IA**  
- Al detectar un objeto durante más de 3 segundos, se captura una foto.  
- La foto es enviada a la **API de OpenAI** para identificar el tipo de material.  
- La clasificación se realiza basándose en los materiales configurados en el JSON.

### 📊 **Registro de materiales**  
- Los materiales clasificados se suman automáticamente en un registro.  
- Esto permite llevar un seguimiento de los materiales reciclados.  


### Ejemplos de detección

- Tapa plastica
<img src="https://github.com/CyberMedina/Centros-de-acopio-verdIES/blob/main/media/tapas_plastica.gif?raw=true" width="400">

- Botella plasticas
<img src="https://github.com/CyberMedina/Centros-de-acopio-verdIES/blob/main/media/botella.gif?raw=true" width="400">

- Bombillo
<img src="https://github.com/CyberMedina/Centros-de-acopio-verdIES/blob/main/media/bombilla.gif?raw=true" width="400">

---

## 🛠️ Tecnologías Usadas  
- **Frontend:** JavaScript (Socket.io)  
- **Backend:** Python, Flask, Flask-SocketIO  
- **IA:** YOLOv5, Pytorch, OpenAI API  

---

## ⚙️ Instalación  
1. Clona el repositorio:  
   ```bash
   git clone https://github.com/CyberMedina/VerdIES.git
   ```  
2. Instala las dependencias:  
   ```bash
   pip install -r requirements.txt
   ```  
3. Crea el archivo `.env` basado en `.env.template` y añade las credenciales de la API de OpenAI:  
   ```bash
   OPENAI_API_KEY="tu-api-key"
   ```  
4. Ejecuta el servidor:  
   ```bash
   flask run
   ```  

---

## 🚀 Uso  
- Abre la aplicación.  
- Habilita la cámara y enfoca un objeto.  
- Si el objeto es detectado por más de **3 segundos**, se enviará a la API de OpenAI para clasificación.  
- Los materiales identificados se sumarán automáticamente en el registro.  

---

## 📬 Contacto

- ✉️ **Correo:** [jhonatanmedina5255@gmail.com](mailto:jhonatanmedina5255@gmail.com)
- 💼 **LinkedIn:** <a href="https://www.linkedin.com/in/jhonatan-jazmil-medina-aguirre-28862a358" target="_blank">www.linkedin.com/in/jhonatan-jazmil-medina-aguirre-28862a358</a>


---

💡 **¡Contribuye al reciclaje inteligente con VerdIES!** 😎  
