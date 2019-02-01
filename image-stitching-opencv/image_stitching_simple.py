import cv2

print("[INFO] loading images...")
imagePaths = "C:/Users/gcper/Code/VisionDeepSpace/image-stitching-opencv/images/scottsdale/IMG_1786-2.jpg C:/Users/gcper/Code/VisionDeepSpace/image-stitching-opencv/images/scottsdale/IMG_1787-2.jpg C:/Users/gcper/Code/VisionDeepSpace/image-stitching-opencv/images/scottsdale/IMG_1788-2.jpg".split()
images = []

for imagePath in imagePaths[:2]:
	image = cv2.imread(imagePath)
	images.append(image)

print("[INFO] stitching images...")
stitcher = cv2.createStitcher()
import time
start = time.time()
(status, stitched) = stitcher.stitch(images)
print(images[0].shape, images[1].shape)
print([i.shape for i in images])
print(status, stitched.shape)

print(time.time() - start)

if status == 0:
	cv2.imwrite("done.png", stitched)

	cv2.imshow("Stitched", stitched)
	cv2.waitKey(0)