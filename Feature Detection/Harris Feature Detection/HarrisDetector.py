import cv2
import numpy as np

class HarrisDetector :
    cornerStrength = np.zeros(0)
    cornerTh = np.zeros(0)
    localMax = np.zeros(0)
    neighbourhood = 0
    aperture = 0
    k = 0.0
    maxStrength = 0.0
    threshold = 0.0
    nonMaxSize = 0
    kernel = np.zeros(0)

    def setLocalMaxWindowSize(self, size) :
        self.nonMaxSize = size
        self.kernel = np.zeros((self.nonMaxSize, self.nonMaxSize), np.uint8)

    def __init__(self, size=3):
        self.neighbourhood = 3
        self.aperture = 3
        self.k = 0.1
        self.maxStrength = 0.0
        self.threshold = 0.01
        self.nonMaxSize = size
        self.kernel = self.setLocalMaxWindowSize(self.nonMaxSize)

    def detect(self, img) :
        ## 1. 해리스코너 검출
        self.cornerStrength = cv2.cornerHarris(img, self.neighbourhood, self.aperture, self.k)
        corners = cv2.goodFeaturesToTrack(self.cornerStrength, 500, 0.01, 10)
        # print(corners)
        self.drawOnImage(img, corners)
        cv2.imshow('cornerHarris', self.cornerStrength)
        cv2.waitKey(0)
        ## 2. 내부 경계값 계산, 이 이미지 안에서 최대값, 최소값, 최대값이 있는 위치, 최소값이 있는 위치
        [minVal, self.maxStrength, minLoc, maxLoc] = cv2.minMaxLoc(self.cornerStrength) #####
        print(self.maxStrength)
        tmp = np.zeros((0,0), np.uint8)
        ## 3. 검출된 코너 중 지역 최대값 찾기, 이 때 지역은 해리스 코너 검출시 지정한 지역이 됨.
        dilated = cv2.dilate(self.cornerStrength, tmp)
        print(type(dilated), dilated.shape)
        cv2.imshow('dilated', dilated)
        cv2.waitKey(0);
        ## 4. 검출된 최대값 영상이 이전에 찾았던 코너점들과 비교해서 최대값이라고 값이 판명되었는지 비교.
        ## 지역 최대치 위치에 있을 때만 TRUE, 그 후, 비최대치 특징을 억제하면 된다.
        self.localMax = cv2.compare(self.cornerStrength, dilated, cv2.CMP_EQ)
        cv2.imshow("localMax", self.localMax)
        cv2.waitKey(0)

    def arrayToTuple(self, a):
        try:
            return tuple(self.arrayToTuple(i) for i in a)
        except TypeError:
            return a

    def getCornerMap(self, qualityLevel) :
        self.threshold = qualityLevel * self.maxStrength
        ## 4.5 이진화해서 확 뚜렷! 하게
        self.cornerTh = cv2.threshold(self.cornerStrength, self.threshold, 255, cv2.THRESH_BINARY)
        cornerMap = self.cornerTh[1].astype('uint8')
        cv2.imshow('pre_cornerMap', cornerMap);
        cv2.waitKey(0);
        ## 5. 비최대치 특징 억제, bitwise_and연산은 각 원소들끼리 대치해서 and연산 수행
        cornerMap = cv2.bitwise_and(cornerMap, self.localMax) #####
        cv2.imshow('bitwise_cornerMap', cornerMap);
        cv2.waitKey(0);

        return cornerMap

    def getCorners(self, points, qualityLevel) :
        cornerMap = self.getCornerMap(qualityLevel)
        points = self.getCornersVec(points, cornerMap) ## points = list, cornerMap = Mat
        return points

    def getCornersVec(self, points, cornerMap) :
        for y in range(len(cornerMap)) :
            rows = [i[y] for i in cornerMap]
            for x in range(len(rows)) :
                if(rows[x]) :
                    points.append([y,x]) ###
        return points

    def drawOnImage(self, img, points, radius=3, color=(255,0,0), thickness=1) :
        it = iter(points)
        while True :
            try :
                i = next(it)
                i = tuple(i)
                cv2.circle(img, i, radius, color, thickness)
            except StopIteration :
                break
