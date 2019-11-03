import cv2

class StructureDescriptor:
    __slot__ = ["dimension"]

    def __init__(self, kps):
        self.kps = kps

    def describe(self, image):
        sift = cv2.xfeatures2d.SIFT_create(nfeatures=self.kps)
        kp1, des1 = sift.detectAndCompute(image, None)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return des1
