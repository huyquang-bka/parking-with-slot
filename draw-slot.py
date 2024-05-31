import cv2

path = "data/C9/C9_base_27.01.2021_12.37.16.jpg"

image = cv2.imread(path)
cv2.namedWindow("image", cv2.WINDOW_NORMAL)

rois = cv2.selectROIs("image", image, fromCenter=False, showCrosshair=True)

with open("slots/c9.txt", "w") as f:
    for roi in rois:
        x, y, w, h = roi
        f.write(f"{x},{y},{w},{h}\n")
