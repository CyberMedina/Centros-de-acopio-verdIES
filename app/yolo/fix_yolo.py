import torch
import warnings
import os
import sys
import importlib

# Silenciar todas las advertencias relacionadas con torch.cuda.amp
warnings.filterwarnings("ignore", category=FutureWarning, module="torch.cuda.amp")
warnings.filterwarnings("ignore", category=UserWarning, message="torch.cuda.amp.autocast")
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Parche para torch.cuda.amp.autocast
original_autocast = torch.cuda.amp.autocast

def patched_autocast(*args, **kwargs):
    if 'enabled' in kwargs:
        enabled = kwargs.pop('enabled')
    else:
        enabled = True
    return torch.amp.autocast(device_type='cuda' if torch.cuda.is_available() else 'cpu', enabled=enabled)

# Aplicar el parche
torch.cuda.amp.autocast = patched_autocast

# Intentar modificar directamente el archivo common.py
try:
    import torch.hub
    hub_dir = os.path.join(torch.hub.get_dir(), 'ultralytics_yolov5_master')
    common_path = os.path.join(hub_dir, 'models', 'common.py')
    
    if os.path.exists(common_path):
        print(f"Modificando {common_path}")
        
        # Leer el archivo
        with open(common_path, 'r') as file:
            content = file.read()
        
        # Buscar y reemplazar la línea problemática
        if 'with amp.autocast(autocast):' in content:
            content = content.replace(
                'with amp.autocast(autocast):',
                "with torch.amp.autocast(device_type='cuda' if torch.cuda.is_available() else 'cpu', enabled=autocast):"
            )
            
            # Guardar el archivo modificado
            with open(common_path, 'w') as file:
                file.write(content)
            
            print(f"Archivo {common_path} modificado correctamente")
        else:
            print("No se encontró la línea problemática en el archivo")
    else:
        print(f"No se encontró el archivo {common_path}")
except Exception as e:
    print(f"Error al intentar modificar el archivo: {e}")
    print("Se aplicó el parche en memoria, pero no se pudo modificar el archivo")

print("Parche aplicado para torch.cuda.amp.autocast") 