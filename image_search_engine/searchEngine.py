import color_descriptor
import structure_descriptor
import searcher
import cv2
import numpy as np

def search(Image):
    idealBins = (8, 12, 3)  # 设定HSV的bins
    kps = 100

    # 打开图片，由于图名可能为中文，不能用imread
    queryImage = cv2.imdecode(np.fromfile(Image, dtype=np.uint8), -1)

    # 初始化颜色特征提取器和结构特征提取器
    colorDescriptor = color_descriptor.ColorDescriptor(idealBins)
    structureDescriptor = structure_descriptor.StructureDescriptor(kps)

    colorIndexPath = "colorindex.csv"
    structureIndexPath = "structureindex.csv"

    #获得目标图片的颜色特征和结构特征
    queryFeatures = colorDescriptor.describe(queryImage)
    queryStructures = structureDescriptor.describe(queryImage)

    # 初始化搜索器并进行搜索
    imageSearcher = searcher.Searcher(colorIndexPath, structureIndexPath)
    searchResults = imageSearcher.search(queryFeatures, queryStructures)
    
    result = []
    for imageName, score in searchResults:
    
        #queryResult = cv2.imread(resultPath + "/" + imageName)
        result.append(imageName)
    
    return result
