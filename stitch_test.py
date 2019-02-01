import cv2
import threading
import time
import itertools
from queue import Queue
"""
queue = Queue()


def count(q):
    i = itertools.count()
    for _ in range(1000):
        q.put(next(i))
        time.sleep(.02)

t1 = threading.Thread(target=count, args=(queue, ))
t2 = threading.Thread(target=count, args=(queue, ))
t1.start()
t2.start()
while 1:
    while queue.empty():
        time.sleep(.01)
    print(queue.get())
    break


one = cv2.VideoCapture(1)
one.set(3, 160)
one.set(4, 120)
two = cv2.VideoCapture(2)
two.set(3, 160)
two.set(4, 120)
time.sleep(5)

stitcher = cv2.createStitcher(True)
print(type(stitcher))
while True:
    try:
        ret_0, frame_0 = one.read()
        assert ret_0
        ret_1, frame_1 = two.read()
        assert ret_1
        # print(frame_0.shape, frame_1.shape)
        a, s = stitcher.stitch((frame_0, frame_1))
        if a == 0:
            cv2.imshow("sitched",s)
        key = cv2.waitKey(20)
        if key == 27:
            break
    except:
        pass

"""

class cam_thread(threading.Thread):
    def __init__(self, preview_name, camID):
        threading.Thread.__init__(self)
        self.preview_name = preview_name
        self.camID = camID

    def run(self):
        print("Starting " + self.preview_name)
        cam_preview(self.preview_name, self.camID)



def cam_preview(preview_name, camID):
    cv2.namedWindow(preview_name)
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(preview_name, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(preview_name)


# Create two threads as follows
thread1 = cam_thread("Camera 1", 1)
thread2 = cam_thread("Camera 2", 2)
thread1.start()
thread2.start()
