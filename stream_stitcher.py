import cv2
import time
import threading
from queue import Queue
import math

frame_left, frame_right = None, None

def frame_putter(source, queue):
    side = source
    source = cv2.VideoCapture(source)
    source.set(3, 320)
    source.set(4, 240)
    # source.set(12, 16)
    source.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    ret, frame = source.read()
    while True:
        if ret:
            ret, frame = source.read()
            if side == 0:
                pass
        else:
            pass
        time.sleep(.1)

# TODO: write to left and write frame objects with each frame, merge them

t1 = threading.Thread(target=frame_putter, args=(1, queue))
t2 = threading.Thread(target=frame_putter, args=(2, queue))
t1.start()
t2.start()

stitcher = cv2.createStitcher()
frames = dict()
a, img = None, None
while True:
    while queue.empty():
        time.sleep(0.01)
    index, frame = queue.get()
    if frames.get(math.floor(index)) is not None:  # mate present
        mate = frames.get(math.floor(index))
        # cv2.imshow("img", frame)

        if int(index) == index:  # left
            a, img = stitcher.stitch((frame, mate))
        else:  # right
            a, img = stitcher.stitch((mate, frame))
        #
        # cv2.imshow("mate", mate)
        # key = cv2.waitKey(5)
        # if key == 27:
        #     break
        frames.pop(math.floor(index))

        if a == 0:
            cv2.imshow("frame", img)
            key = cv2.waitKey(10)
            if key == 27:
                break
            print(img.shape)
    else:  # new mate
        frames.update({math.floor(index): frame})