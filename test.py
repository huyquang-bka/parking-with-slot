import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=True)
