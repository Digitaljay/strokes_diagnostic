import numpy as np
from PIL import Image
from pathlib import Path
from sklearn.neighbors import NearestNeighbors
from torchvision import transforms
import torch

import warnings
warnings.filterwarnings(action='ignore', category=DeprecationWarning)

RESCALE_SIZE = 224

def to_tensor(file_name):
    transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    x = Image.open(file_name)
    x.load()
    x = x.crop((470, 0, 1449, 979))
    x = x.resize((RESCALE_SIZE, RESCALE_SIZE))
    x = np.array(x)
    x = np.array(x / 255, dtype='float32')
    x = transform(x)
    x = torch.reshape(x, (-1,))
    return x.tolist()

TRAIN_DIR = Path('C:/all_kt')
train_files = sorted(list(TRAIN_DIR.rglob('*.jpg')))

# print(len(train_files))
X=[to_tensor(file_name) for file_name in train_files]
nbrs = NearestNeighbors().fit(X)

print("ready")
