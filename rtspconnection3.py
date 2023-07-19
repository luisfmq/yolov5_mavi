import cv2, torch, datetime
import numpy as np

def draw_bounding_boxes(video_path):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='crowdhuman_yolov5m.pt')
    video_capture = cv2.VideoCapture(video_path)
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    frame_count, pIn, pOut, last_ym, counted_people = 0, 0, 0, None, set()
    nome_arq = datetime.datetime.today()
    arquivor = open(str(nome_arq), 'x')

    while True:
        ret, image = video_capture.read()
        if not ret:
            break
        line_position = int(image.shape[0] / 2) + 100
        results = model(image)
        boxes = results.xyxy[0].tolist()
        labels = results.names[0]

        for box in boxes:
            x1, y1, x2, y2, conf, cls = box
            if cls == 0:
                ym = int((y1 + y2) / 2)
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 0), 2)
                cv2.circle(image, (int(image.shape[1] / 2), ym), 5, (0, 0, 0), 5)
                cv2.circle(image, (int(image.shape[1] / 2), last_ym), 5, (255, 255, 255), 5)
                if last_ym is not None:
                    if last_ym < line_position and ym >= line_position:
                        person_id = f'{int(x1)}_{int(y1)}_{int(x2)}_{int(y2)}'
                        if person_id not in counted_people:
                            counted_people.add(person_id)
                            pOut += 1
                            arquivor = open(str(nome_arq), 'a')
                            texte = arquivor.write(str(datetime.datetime.today()) + ' PORTA 01 SAIDA\n')
                            arquivor.close()
                            print('SAINDO')
                    elif last_ym >= line_position and ym < line_position:
                        person_id = f'{int(x1)}_{int(y1)}_{int(x2)}_{int(y2)}'
                        if person_id not in counted_people:
                            counted_people.add(person_id)
                            pIn += 1
                            arquivor = open(str(nome_arq), 'a')
                            texte = arquivor.write(str(datetime.datetime.today()) + ' PORTA 01 ENTRADA\n')
                            arquivor.close()
                            print('ENTRANDO')
                last_ym = ym

        cv2.putText(image, "ENTRARAM = " + str(pIn), (90, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
        cv2.putText(image, "SAIRAM = " + str(pOut), (90, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

        frame_count += 1
        print(f'Processing frame {frame_count}')
        cv2.line(image, (0, line_position), (image.shape[1], line_position), (0, 0, 0), 2)
        cv2.imshow('frame', image)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

#video_path = "dataset.mp4"
video_path = "rtsp://admin:Mavi2022@172.16.16.57:554/cam/realmonitor?channel=1&subtype=1"
draw_bounding_boxes(video_path)
