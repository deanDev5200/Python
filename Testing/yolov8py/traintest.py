from ultralytics import YOLO

model = YOLO("D:/Python/yolov8n.pt")  # load a pretrained model (recommended for training)

# Use the model
model.train(data="D:/Python/yolov8py/flame/1/data.yaml", epochs=10)  # train the model
results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image
success = model.export(format="torch")  # export the model to ONNX format