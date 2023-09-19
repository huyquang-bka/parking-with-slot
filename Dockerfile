FROM ultralytics/yolov5
COPY . /app
WORKDIR /app
CMD ["python3", "main.py"]