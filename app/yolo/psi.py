import torch
import cv2
import base64
import time
import warnings
import requests

warnings.filterwarnings("ignore", category=FutureWarning, module="torch")
warnings.filterwarnings("ignore", category=UserWarning, message="torch.cuda.amp.autocast")
warnings.filterwarnings("once")

class YOLODetector:
    def __init__(self):
        self.detection_state = "no_detected"
        self.detection_start_time = None
        self.no_detection_start_time = None
        self.last_detection = None
        self.detection_threshold = 0.1
        self.absence_threshold = 1.5
        self.confidence_threshold = 0.5
        self.MAX_COUNT = 20
        self.img_count = 1
        
        try:
            self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s',
                                pretrained=True, trust_repo=True)
        except Exception as e:
            print("Error al cargar el modelo:", e)
            
    def iniciar_camara(self, camera_index=1):
        self.cap = cv2.VideoCapture(camera_index)
        
    def detener_camara(self):
        if hasattr(self, 'cap'):
            self.cap.release()
            cv2.destroyAllWindows()
            
    def enviar_a_api(self, imagen):
        if self.img_count >= self.MAX_COUNT:
            print("Se ha alcanzado el límite de imágenes a enviar")
            return
            
        _, img_encoded = cv2.imencode('.jpg', imagen)
        with open('imagen_enviada.jpg', 'wb') as f:
            f.write(img_encoded.tobytes())

        self.img_count += 1
        
        print("Imagen enviada a la API")
        url = 'http://127.0.0.1:8002/api/test_envio'
        data = {'img': base64.b64encode(img_encoded.tobytes()).decode('utf-8')}
        response = requests.post(url, json=data)
        print(f"Respuesta de la API: {response.status_code}")

    def objeto_se_movio(self, nueva_deteccion, umbral=20):
        if self.last_detection is None:
            self.last_detection = nueva_deteccion
            return False

        last_detection_rounded = {k: round(v, 0) for k, v in self.last_detection.items() if k in [
            'xmin', 'ymin', 'xmax', 'ymax']}
        nueva_deteccion_rounded = {k: round(v, 0) for k, v in nueva_deteccion.items() if k in [
            'xmin', 'ymin', 'xmax', 'ymax']}

        distancia = ((nueva_deteccion_rounded['xmin'] - last_detection_rounded['xmin']) ** 2 +
                    (nueva_deteccion_rounded['ymin'] - last_detection_rounded['ymin']) ** 2 +
                    (nueva_deteccion_rounded['xmax'] - last_detection_rounded['xmax']) ** 2 +
                    (nueva_deteccion_rounded['ymax'] - last_detection_rounded['ymax']) ** 2) ** 0.5

        if distancia > umbral:
            self.last_detection = nueva_deteccion
            return True

        self.last_detection = nueva_deteccion
        return False

    def procesar_frame(self):
        if not hasattr(self, 'cap'):
            raise Exception("La cámara no ha sido iniciada")
            
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        results = self.model(frame)
        detections = results.xyxy[0]
        
        results.render()
        return frame, len(detections) > 0

    def ejecutar_deteccion(self):
        if not hasattr(self, 'cap'):
            self.iniciar_camara()
            
        image_sent = False
        
        while True:
            frame, hay_detecciones = self.procesar_frame()
            if frame is None:
                break

            if hay_detecciones:
                if self.detection_start_time is None:
                    self.detection_start_time = time.time()
                elif time.time() - self.detection_start_time >= 3 and not image_sent:
                    print("Objeto detectado durante 3 segundos. Enviando imagen...")
                    self.enviar_a_api(frame)
                    image_sent = True
                self.no_detection_start_time = None
            else:
                if self.no_detection_start_time is None:
                    self.no_detection_start_time = time.time()
                elif time.time() - self.no_detection_start_time >= 3:
                    print("Objeto ausente durante 3 segundos. Reiniciando detección...")
                    self.detection_start_time = None
                    image_sent = False

            cv2.imshow("Detecciones YOLOv5", frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        self.detener_camara()

if __name__ == "__main__":
    detector = YOLODetector()
    detector.ejecutar_deteccion()
