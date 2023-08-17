import torch, cv2
from models.experimental import attempt_load
from utils.datasets import LoadImages, LoadStreams

link = "rtsp://admin:Mavi2022@172.16.16.57:554/cam/realmonitor?channel=1&subtype=1"

videocapture1 = cv2.VideoCapture(link)


model = attempt_load("yolov5s.pt", map_location='cpu')

while True:
    ret, imagem = videocapture1.read()
    desired_size = (416, 416)  # Dimensões esperadas pelo modelo
    resized_image = cv2.resize(imagem, desired_size)
    normalized_image = resized_image / 255.0
    input_image = torch.unsqueeze(torch.from_numpy(normalized_image).permute(2, 0, 1).float(), 0)
    results = model(input_image)
