from ultralytics import YOLO

model = YOLO("yolov8.yaml")

results = model.train(data = "Czech_something.yaml",epochs = 130)
