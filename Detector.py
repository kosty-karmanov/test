import cv2
import torch
from numpy import random
import numpy as np

from models.experimental import attempt_load
from models.common import DetectMultiBackend
from utils22.general import check_img_size, non_max_suppression, scale_coords, xyxy2xywh
from utils22.torch_utils import select_device, time_sync


def detect(path="", img2=None):
    weights = r"best.pt"
    device = select_device("cpu")
    model = DetectMultiBackend(weights, device=device, dnn=False)
    names = model.module.names if hasattr(model, 'module') else model.names
    if img2 is None:
        img = cv2.imread(path)
    else:
        img = img2
    im0s = img
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float()
    img /= 255
    if len(img.shape) == 3:
        img = img[None]
    with torch.no_grad():
        pred = model(img, augment=False, visualize=False)
    pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)
    for i, det in enumerate(pred):
        names1 = []
        cords1 = []
        result = []
        if len(det):
            print(det)
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()
            for c in det[:, -1].unique():
                names1.append(names[int(c)])
            for *xyxy, conf, cls in reversed(det):
                cords1.append(torch.tensor(xyxy).view(1, 4).view(-1).tolist())
        for iteration in range(len(names1)):
            result.append([names1[iteration], tuple(cords1[iteration])])
        print(f'Done, {result}')


cap = cv2.VideoCapture(0)

while cv2.waitKey(0) != 27:
    _, image = cap.read()
    detect(img2=image)
