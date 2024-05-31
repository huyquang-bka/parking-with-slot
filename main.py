import os
import time
import torch
import cv2
import zipfile
import requests
from tqdm import tqdm


def process(location="tdn_left"):
    slots = {}
    txt_name = f"slots/{location}.txt"
    with open(txt_name, "r") as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            x, y, w, h = line.split(",")
            slots[idx] = [int(x), int(y), int(w), int(h)]

    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=True)
    model.conf = 0.25
    model.classes = [2, 5, 7]

    path = f"data-images/{location}"
    original_path = f"original_{location}.jpg"
    processed_path = f"processed_{location}.jpg"
    data_zip_path = f"data_{location}.zip"
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
                result_path = f"results_{location}.txt"
                f = open(result_path, "w")
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
                        cv2.rectangle(
                            img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    else:
                        f.write(f"{key} 0\n")
                        cv2.rectangle(
                            img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                f.close()
                cv2.imwrite(processed_path, img)
                cv2.imwrite(original_path, original)
                with zipfile.ZipFile(data_zip_path, "w") as zip_ref:
                    zip_ref.write(result_path)
                    zip_ref.write(processed_path)
                    zip_ref.write(original_path)
                try:
                    r = requests.post("http://localhost:5518/get-data",
                                      files={"file": open(data_zip_path, "rb")})
                    print(r.json())
                except Exception as e:
                    print("Error: ", e)
                time.sleep(3)


if __name__ == "__main__":
    import threading

    # locations = ["tdn_left", "tdn_right"]
    locations = ["c9"]

    thread_list = []
    for location in locations:
        t = threading.Thread(target=process, args=(location,))
        t.start()
        thread_list.append(t)
