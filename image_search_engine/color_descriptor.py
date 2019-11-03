import cv2
import numpy

class ColorDescriptor:

    __slot__ = ["bins"]

    def __init__(self, bins):
        self.bins = bins

    def getHistogram(self, image, mask, isCenter):
        # get histogram
        imageHistogram = cv2.calcHist([image], [0, 1, 2], mask, self.bins, [0, 180, 0, 256, 0, 256])
        # normalize
        imageHistogram = cv2.normalize(imageHistogram, imageHistogram).flatten()
        if isCenter:
            weight = 3.0
            for index in range(len(imageHistogram)):
                imageHistogram[index] *= weight
        return imageHistogram

    def describe(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []

        # 图片长宽以及中心位置
        height, width = image.shape[0], image.shape[1]
        centerX, centerY = int(width * 0.5), int(height * 0.5)

        # 初始中心的椭圆
        axesX, axesY = int(width * 0.75) / 2, int (height * 0.75) / 2
        ellipseMask = numpy.zeros([height, width], dtype="uint8")
        cv2.ellipse(ellipseMask, (int(centerX), int(centerY)), (int(axesX), int(axesY)), 0, 0, 360, 255)

        # 初始掩模
        segments = [(0, centerX, 0, centerY), (0, centerX, centerY, height), (centerX, width, 0, centerY), (centerX, width, centerY, height)]

        for startX, endX, startY, endY in segments:
            cornerMask = numpy.zeros([height, width], dtype="uint8")
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            cornerMask = cv2.subtract(cornerMask, ellipseMask)
            # 边角的直方图
            imageHistogram = self.getHistogram(image, cornerMask, False)
            features.append(imageHistogram)

        # 中心区域的直方图
        imageHistogram = self.getHistogram(image, ellipseMask, True)
        features.append(imageHistogram)
        # return
        return features
