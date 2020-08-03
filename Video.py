import cv2
import threading
from queue import Queue
# 비디오 클래스
# 큐에 데이터가 차면 스레드 대기, Gui 클래스에서 데이터 빼낸 후 스레드 다시 동작  
q = Queue() 
evt = threading.Event()
flag = False


def get_video(path):
    cap = cv2.VideoCapture(path)

    thread = threading.Thread(target=run, args=(cap,))
    thread.start()


def run(cap):
    chars = ' .,-~:;=!*#$@'
    nw = 60
    global flag
    flag = True

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        h, w = img.shape
        nh = int(h / w * nw)
        out_count = 0
        in_count = 0

        img = cv2.resize(img, (nw * 2, nh))
        data = [[0 for col in range(120)] for row in range(len(img))]

        for row in img:

            for pixel in row:
                index = int(pixel / 256 * len(chars))
                data[out_count][in_count] = chars[index]
                in_count += 1

            in_count = 0
            out_count += 1

        q.put((data, evt))
        evt.wait()

        if flag is False:
            break

    flag = False
    cap.release()
