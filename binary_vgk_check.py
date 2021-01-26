import torch
from pathlib import Path
from torch.utils.data import DataLoader
from Dataset import KTDataset
from model_small import SmallCnn

num_classes=1
base_model=SmallCnn(num_classes)
base_model.load_state_dict(torch.load("weights/KT_binary_vgk_smalla_v2_last.pth", map_location=torch.device('cpu')))

def predict(model, test_loader):
    with torch.no_grad():
        logits = []

        for inputs in test_loader:
            model.eval()
            outputs = model(inputs).cpu()
            logits.append(outputs)
    # print(logits)
    probs = torch.sigmoid(torch.cat(logits)).numpy()
    probs_pro = [1 if i>=0.5 else 0 for i in probs]
    return probs, probs_pro

def predict_picture():
    TEST_DIR = Path('test_img')
    test_files=list(TEST_DIR.rglob('*.jpg'))
    # test_files=[str(pathlib.PurePosixPath("C:/Users/Digitaljay/Documents/GitHub/strokes_diagnostic/test_img/ВЖК_1.jpg"))]
    for file in test_files:
        test_dataset = KTDataset([file], mode="test")
        test_loader = DataLoader(test_dataset, shuffle=False, batch_size=64)
        probs, probs_pro = predict(base_model, test_loader)
        print(file, probs, probs_pro)
        # predicted_proba = np.max(probs)*100
        # y_pred = np.argmax(probs)
        # predicted_label = label_encoder[y_pred]
        # print(file, y_pred, predicted_label, predicted_proba)

predict_picture()
