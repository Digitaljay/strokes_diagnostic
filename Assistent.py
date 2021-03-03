import torch
import pickle
import numpy as np
from torch.utils.data import DataLoader
import torch.nn as nn
from Dataset import KTDataset
from Net import SimpleCnn
from model_small import SmallCnn
import pathlib

vmg_model=SimpleCnn(4)
vmg_model.load_state_dict(torch.load("weights/KT_vmg_4.pth", map_location=torch.device('cpu')))
vmg_encoder={0: "ВМГ задняя яма",
             1: "ВМГ консерва",
             2: "ВМГ отсутствует",
             3: "ВМГ операция"}

vgk_model=SimpleCnn(2)
vgk_model.load_state_dict(torch.load("weights/KT_vgk_6.pth", map_location=torch.device('cpu')))
vgk_encoder={0: "ВЖК",
             1: "ВЖК отсутствует"}

sak_model=SmallCnn(1)
sak_model.load_state_dict(torch.load("weights/KT_binary_sak_smalla_29.pth", map_location=torch.device('cpu')))
sak_encoder = {0:"САК отсутствует",
               1:"САК"}

ish_model=SmallCnn(2)
ish_model.load_state_dict(torch.load("weights/KT_ish_small_7.pth", map_location=torch.device('cpu')))
ish_encoder = pickle.load(open("encoders/label_ish_encoder.pkl", 'rb'))

sdg_model=SimpleCnn(2)
sdg_model.load_state_dict(torch.load('weights/KT_sdg_1.pth', map_location=torch.device('cpu')))
sdg_encoder=pickle.load(open("encoders/label_sdg_encoder.pkl", 'rb'))

tumor_model=SimpleCnn(2)
tumor_model.load_state_dict(torch.load("weights/KT_tumor_1.pth", map_location=torch.device('cpu')))
tumor_encoder=pickle.load(open("encoders/label_tumor_encoder.pkl", 'rb'))

class Diagnose():
    def __init__(self, file_name):
        test_files=[str(pathlib.PurePosixPath(file_name))]
        test_dataset = KTDataset(test_files, mode="test")
        test_loader = DataLoader(test_dataset, shuffle=False, batch_size=64)
        vmg_dictionary={"ВМГ отсутствует": 0,
                        "ВМГ задняя яма": 1,
                        "ВМГ консерва": 2,
                        "ВМГ операция": 3}

        probs = self.predict(vmg_model, test_loader)
        self.vmg_proba = np.max(probs)*100
        self.vmg_pred = np.argmax(probs)
        self.vmg_label = vmg_encoder[self.vmg_pred]
        self.vmg=vmg_dictionary[self.vmg_label]

        probs = self.predict(vgk_model, test_loader)
        self.vgk_proba = np.max(probs)*100
        self.vgk_pred = np.argmax(probs)
        self.vgk_label = vgk_encoder[self.vgk_pred]
        self.vgk=1-self.vgk_pred

        probs = self.predict_binary(sak_model, test_loader)
        self.sak_proba=probs[0]
        self.sak=1 if self.sak_proba>=0.5 else 0
        self.sak_label = sak_encoder[self.sak]

        probs = self.predict(sdg_model, test_loader)
        self.sdg_proba = np.max(probs)*100
        self.sdg_pred = np.argmax(probs)
        self.sdg_label = sdg_encoder.classes_[self.sdg_pred]
        self.sdg=1 if self.sdg_label=="СДГ" else 0

        probs = self.predict(ish_model, test_loader)
        self.ish_proba = np.max(probs)*100
        self.ish_pred = np.argmax(probs)
        self.ish_label = ish_encoder.classes_[self.ish_pred]
        self.ish=1 if self.ish_label=="ишемия" else 0

        probs = self.predict(tumor_model, test_loader)
        self.tumor_proba = np.max(probs)*100
        self.tumor_pred = np.argmax(probs)
        self.tumor_label = tumor_encoder.classes_[self.tumor_pred]
        self.tumor = 1 if self.tumor_label=="опухоль" else 0


    def predict(self, model, test_loader):
        with torch.no_grad():
            logits = []

            for inputs in test_loader:
                model.eval()
                outputs = model(inputs).cpu()
                logits.append(outputs)

        probs = nn.functional.softmax(torch.cat(logits), dim=-1).numpy()
        return probs

    def predict_binary(self, model, test_loader):
        with torch.no_grad():
            logits = []
            for inputs in test_loader:
                model.eval()
                outputs = model(inputs).cpu()
                logits.append(outputs)
        probs = torch.sigmoid(torch.cat(logits)).numpy()
        return probs





def adapter(case):
    classes=[]
    if case.vmg and case.vgk:
        classes.append(1)
    if case.vmg and case.ish:
        classes.append(6)
    if case.vmg and case.sak:
        classes.append(9)
    if case.vmg and not case.vgk and not case.ish and not case.sak:
        classes.append(case.vmg+1)
    if case.vgk and not case.vmg:
        classes.append(0)
    if case.ish and not case.vmg:
        classes.append(5)
    if case.tumor:
        classes.append(7)
    if case.sak and not case.vmg:
        classes.append(8)

    return classes

name_decoder={
    0: "Внутрижелудочновое кровоизлияние",
    1: "Внутримозговая гематома с вентрикулярным компонентом",
    2: "Внутримозговая гематома в задней ямке",
    3: "Внутримозговая гематома для консервативного лечения",
    4: "Внутримозновая гематома под операцию",
    5: "Ишемия",
    6: "Ишемия с реперфузией",
    7: "Опухоль",
    8: "Субарахноидальное кровоизлияние",
    9: "Внутримозговая гематома с субарахноидальным кровоизлиянием"
}

# for i in range(1, 41):
#     d=Diagnose("C:/Users/Digitaljay/Documents/GitHub/strokes_diagnostic/final_tests/"+str(i)+".jpg")
#     if d.vmg:
#         print("Снимок", i)
#         print(d.vmg_label)
#         if d.vgk:
#             print(d.vgk_label)
#         if d.sak:
#             print(d.sak_label)
#         if d.tumor:
#             print(d.tumor_label)
#         if d.ish:
#             print(d.ish_label)
#         print()


    # print(d.vmg_label)
    # print(d.vgk_label)
    # print(d.ish_label)
    # # print(d.sdg_label)
    # print(d.sak_label)
    # print(d.tumor_label)
    #
    # print(adapter(d))

d=Diagnose("C:/Users/Digitaljay/Documents/GitHub/strokes_diagnostic/test_img/калугина.jpg")
print(d.vmg_label)
print(d.vgk_label)
print(d.ish_label)
# print(d.sdg_label)
print(d.sak_label)
print(d.tumor_label)

print(adapter(d))
