from flask import Blueprint, jsonify
from ..yolo.psi import YOLODetector
import threading

yolo_bp = Blueprint('yolo', __name__)
detector = None
detection_thread = None

@yolo_bp.route('/iniciar_deteccion', methods=['POST'])
def iniciar_deteccion():
    global detector, detection_thread
    
    if detection_thread and detection_thread.is_alive():
        return jsonify({'mensaje': 'La detección ya está en curso'}), 400
        
    detector = YOLODetector()
    detection_thread = threading.Thread(target=detector.ejecutar_deteccion)
    detection_thread.start()
    
    return jsonify({'mensaje': 'Detección iniciada correctamente'}), 200

@yolo_bp.route('/detener_deteccion', methods=['POST'])
def detener_deteccion():
    global detector, detection_thread
    
    if detector:
        detector.detener_camara()
        if detection_thread:
            detection_thread.join()
        detector = None
        detection_thread = None
        return jsonify({'mensaje': 'Detección detenida correctamente'}), 200
    
    return jsonify({'mensaje': 'No hay detección en curso'}), 400 