import cv2
import numpy as np
import HarrisDetector as har

img = cv2.imread("st_paul.jpg", 0)
# # print(img.shape)
# # print(np.uint8(0))
# cornerStrength = cv2.cornerHarris(img, 3, 3, 0.01)
#
# threshold = 0.0001
# # harrisCorners = np.zeros((height, width, 3), np.uint8)
# harrisCorners = cv2.threshold(cornerStrength, threshold, 255, cv2.THRESH_BINARY_INV)
# # print(list(harrisCorners)[1])
# cv2.imshow("harris", list(harrisCorners)[1])
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# pts = [[0 for j in range(2)] for i in range(10000)]
# print(pts)

harris = har.HarrisDetector()
harris.detect(img)
pts = harris.getCorners(pts, 0.02)
harris.drawOnImage(img, pts)
cv2.imshow('harris', img)
cv2.waitKey(0)
cv2.destroyAllWindows()



# import cv2
# import numpy as  np
#
# img = np.zeros((200, 200, 3), np.uint8)
# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.imshow('image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
