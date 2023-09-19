import os
import time
import torch
import cv2
import zipfile
import requests
from tqdm import tqdm

slots = {}
with open("slots.txt", "r") as f:
    lines = f.readlines()
    for idx, line in enumerate(lines):
        x, y, w, h = line.split(",")
        slots[idx] = [int(x), int(y), int(w), int(h)]

model = torch.hub.load('ultralytics/yolov5', 'yolov5l', pretrained=True)
model.conf = 0.1
model.classes = [2, 5, 7]

path = "images"

while True:
    for root, dirs, files in os.walk(path):
        for file in tqdm(files):
            if not file.endswith(".jpg"):
                continue
            fp = os.path.join(root, file)
            img = cv2.imread(fp)
            if img is None:
                continue
            original = img.copy()
            results = model(img)
            f = open("results_tdn.txt", "w")
            bboxes = []
            for idx, result in enumerate(results.xyxy[0].cpu().numpy()):
                x1, y1, x2, y2, conf, cls = result
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                bboxes.append([cx, cy])
            for key, box in slots.items():
                is_busy = False
                x, y, w, h = box
                for bbox in bboxes:
                    cx, cy = bbox
                    if x <= cx <= x + w and y <= cy <= y + h:
                        is_busy = True
                        break
                if is_busy:
                    f.write(f"{key} 1\n")
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                else:
                    f.write(f"{key} 0\n")
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            f.close()
            cv2.imwrite("processed_tdn.jpg", img)
            cv2.imwrite("original_tdn.jpg", original)
            with zipfile.ZipFile("data.zip", "w") as zip_ref:
                zip_ref.write("results_tdn.txt")
                zip_ref.write("processed_tdn.jpg")
                zip_ref.write("original_tdn.jpg")
            try:
                r = requests.post("http://localhost:5518/get-data",
                                  files={"file": open("data.zip", "rb")}, timeout=3)
                print(r.json())
            except Exception as e:
                print("Error: ", e)
            time.sleep(3)
