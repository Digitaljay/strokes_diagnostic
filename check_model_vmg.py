import torch
import pickle
import numpy as np
from pathlib import Path
from torch.utils.data import DataLoader
import torch.nn as nn

from Dataset import KTDataset
from VMGNet import SimpleVMG
import pathlib

num_classes=4
base_model=SimpleVMG(num_classes)
base_model.load_state_dict(torch.load("KT_vmg_2.pth", map_location=torch.device('cpu')))
label_encoder={0: "ВМГ консерва",
               1: "ВМГ отсутствует",
               2: "ВМГ операция"}

def predict(model, test_loader):
    with torch.no_grad():
        logits = []

        for inputs in test_loader:
            model.eval()
            outputs = model(inputs).cpu()
            logits.append(outputs)

    probs = nn.functional.softmax(torch.cat(logits), dim=-1).numpy()
    return probs

def predict_picture():
    TEST_DIR = Path('test_img')
    test_files=list(TEST_DIR.rglob('*.jpg'))
    # test_files=[str(pathlib.PurePosixPath("C:/Users/Digitaljay/Documents/GitHub/strokes_diagnostic/test_img/ВЖК_1.jpg"))]
    for file in test_files:
        test_dataset = KTDataset([file], mode="test")
        test_loader = DataLoader(test_dataset, shuffle=False, batch_size=64)
        probs = predict(base_model, test_loader)
        predicted_proba = np.max(probs)*100
        y_pred = np.argmax(probs)
        predicted_label = label_encoder[y_pred]
        print(file, y_pred, predicted_label, predicted_proba)

predict_picture()
