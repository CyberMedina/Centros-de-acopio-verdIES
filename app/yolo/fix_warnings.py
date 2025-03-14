import torch
import warnings
import os
import sys
import app.yolo.fix_warnings

# Silenciar todas las advertencias relacionadas con torch.cuda.amp
warnings.filterwarnings("ignore", category=FutureWarning, module="torch.cuda.amp")
warnings.filterwarnings("ignore", category=UserWarning, message="torch.cuda.amp.autocast")

# Parche para torch.cuda.amp.autocast
original_autocast = torch.cuda.amp.autocast

def patched_autocast(*args, **kwargs):
    return torch.amp.autocast('cuda', *args, **kwargs)

torch.cuda.amp.autocast = patched_autocast

print("Parche aplicado para torch.cuda.amp.autocast") 