import cv2
import time
import threading
from queue import Queue
import math


class FrameGetter:
    def __init__(self):
        self._frame_left, self._frame_right = None, None
        t0 = threading.Thread(target=self.frame_putter, args=(1,))
        t1 = threading.Thread(target=self.frame_putter, args=(2,))
        t0.start()
        t1.start()

    def frame_putter(self, source):
        side = source
        source = cv2.VideoCapture(side, cv2.CAP_DSHOW)
        source.set(3, 320)
        source.set(4, 240)
        source.set(10, .01)
        source.set(15, 16)
        source.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        ret, frame = source.read()
        while True:
            if ret:
                if side == 2:
                    self._frame_left = frame
                    print("left", self._frame_left.shape)
                else:
                    self._frame_right = frame
                    print("right", self._frame_right.shape)
            ret, frame = source.read()
            time.sleep(.1)

    def get_left(self):
        return self._frame_left

    def get_right(self):
        return self._frame_right



def main():
    picture_nb = 0
    start = time.time()
    getter = FrameGetter()
    stitcher = cv2.createStitcher()
    time.sleep(8)
    """
    for i in range(5):
        one = cv2.imread("pairs/left_{}.png".format(i))
        two = cv2.imread("pairs/right_{}.png".format(i))
        status, img = stitcher.stitch((one, two))
        cv2.imwrite("pairs/stitched_{}.png".format(i), img)
    # """
    while True:
        
        status, img = stitcher.stitch((getter.get_right(), getter.get_left()))
        if status == 0:
            cv2.imshow("frame", img)
            key = cv2.waitKey(1)
            if key == 27:
                break
        else:
            print("failing")
            
        if start + 5 < time.time() and picture_nb < 5:

            cv2.imwrite("pairs/left_{}.png".format(picture_nb), getter.get_left())
            cv2.imwrite("pairs/right_{}.png".format(picture_nb), getter.get_right())
            picture_nb += 1
        time.sleep(.1)
        # """

if __name__ == "__main__":
    main()
