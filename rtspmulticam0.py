import cv2, torch, datetime
import numpy as np

def draw_bounding_boxes(video_path1, video_path2, video_path3, video_path4):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5n.pt')
    video_capture1 = cv2.VideoCapture(video_path1)
    video_capture2 = cv2.VideoCapture(video_path2)
    video_capture3 = cv2.VideoCapture(video_path3)
    video_capture4 = cv2.VideoCapture(video_path4)
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    frame_count, pIn, pOut, last_ym, counted_people = 0, 0, 0, None, set()
    nome_arq = datetime.datetime.today()
    arquivor = open(str(nome_arq), 'x')

    while True:
        ret1, image1 = video_capture1.read()
        ret2, image2 = video_capture2.read()
        ret3, image3 = video_capture3.read()
        ret4, image4 = video_capture4.read()
        image1 = cv2.hconcat([image1, image2])
        image2 = cv2.hconcat([image3, image4])
        image = cv2.vconcat([image1, image2])
        if not ret1 or not ret2 or not ret3 or not ret4:
            break
        line_position_sup = int(image.shape[0] / 2) - 350
        line_position_inf = int(image.shape[0] / 2) + 350
        results = model(image)
        boxes = results.xyxy[0].tolist()
        labels = results.names[0]

        for box in boxes:
            x1, y1, x2, y2, conf, cls = box
            if cls == 0:
                xm = int((x1 + x2) / 2)
                ym = int((y1 + y2) / 2)
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 0), 2)
                cv2.circle(image, (xm, ym), 5, (0, 0, 0), 5)
                cv2.circle(image, (xm, last_ym), 5, (255, 255, 255), 5)
                if last_ym is not None:
                    if last_ym < line_position_sup and ym >= line_position_sup and (abs(ym - line_position_sup) <= 20) and (xm <= image.shape[1]/2):
                        person_id = f'{int(x1)}_{int(y1)}_{int(x2)}_{int(y2)}'
                        if person_id not in counted_people:
                            counted_people.add(person_id)
                            pOut += 1
                            arquivor = open(str(nome_arq), 'a')
                            texte = arquivor.write(str(datetime.datetime.today()) + ' PORTA 01 SAIDA\n')
                            arquivor.close()
                            print('SAINDO')
                    elif last_ym >= line_position_sup and ym < line_position_sup and (abs(ym - line_position_sup) <= 20) and (xm <= image.shape[1]/2):
                        person_id = f'{int(x1)}_{int(y1)}_{int(x2)}_{int(y2)}'
                        if person_id not in counted_people:
                            counted_people.add(person_id)
                            pIn += 1
                            arquivor = open(str(nome_arq), 'a')
                            texte = arquivor.write(str(datetime.datetime.today()) + ' PORTA 01 ENTRADA\n')
                            arquivor.close()
                            print('ENTRANDO')
                last_ym = ym

        cv2.putText(image, "ENTRARAM P1 = " + str(pIn), (90, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        cv2.putText(image, "SAIRAM P1 = " + str(pOut), (90, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.putText(image, "ENTRARAM P2 = " + str(pIn), (int(image.shape[1]/2), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        cv2.putText(image, "SAIRAM P2 = " + str(pOut), (int(image.shape[1]/2), 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        frame_count += 1
        print(f'Processing frame {frame_count}')
        cv2.line(image, (0, line_position_sup), (image.shape[1], line_position_sup), (0, 0, 0), 2)
        cv2.line(image, (0, line_position_inf), (image.shape[1], line_position_inf), (0, 0, 0), 2)
        cv2.imshow('frame', image)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    video_capture1.release()
    video_capture2.release()
    video_capture3.release()
    video_capture4.release()
    cv2.destroyAllWindows()

'''video_path1 = "dataset.mp4"
video_path2 = "dataset.mp4"
video_path3 = "dataset.mp4"
video_path4 = "dataset.mp4"'''
video_path1 = "rtsp://admin:Mavi2022@172.16.16.57:554/cam/realmonitor?channel=1&subtype=1"
video_path2 = "rtsp://admin:Mavi2022@172.16.16.57:554/cam/realmonitor?channel=1&subtype=1"
video_path3 = "rtsp://admin:Mavi2022@172.16.16.57:554/cam/realmonitor?channel=1&subtype=1"
video_path4 = "rtsp://admin:Mavi2022@172.16.16.57:554/cam/realmonitor?channel=1&subtype=1"
draw_bounding_boxes(video_path1, video_path2, video_path3, video_path4)
