import numpy
import csv
import re

class Searcher:
    __slot__ = ["colorIndexPath", "structureIndexPath"]

    def __init__(self, colorIndexPath, structureIndexPath):
        self.colorIndexPath, self.structureIndexPath = colorIndexPath, structureIndexPath

    def solveColorDistance(self, features, queryFeatures, eps = 1e-5):  # 计算两张图颜色空间的距离
        distance = 0.5 * numpy.sum([((a - b) ** 2) / (a + b + eps) for a, b in zip(features, queryFeatures)])
        return distance

    def solveStructureDistance(self, structures, queryStructures, eps = 1e-5):  # 计算两张图结构空间的距离
        distance = 0
        normalizeRatio = 5e3
        distance = numpy.sqrt(numpy.sum(numpy.square(structures - queryStructures)))
        return distance / normalizeRatio

    def searchByColor(self, queryFeatures):  # 计算每张图与目标图的颜色空间距离并存储到字典里
        searchResults = {}
        with open(self.colorIndexPath) as indexFile:
            reader = csv.reader(indexFile)
            for line in reader:
                features = []
                for feature in line[1:]:
                    feature = feature.replace("[", "").replace("]", "")
                    findStartPosition = 0
                    feature = re.split("\s+", feature)
                    rmlist = []
                    for index, strValue in enumerate(feature):
                        if strValue == "":
                            rmlist.append(index)
                    for _ in range(len(rmlist)):
                        currentIndex = rmlist[-1]
                        rmlist.pop()
                        del feature[currentIndex]
                    feature = [float(eachValue) for eachValue in feature]
                    features.append(feature)
                distance = self.solveColorDistance(features, queryFeatures)
                searchResults[line[0]] = distance

            indexFile.close()
        # print "feature", sorted(searchResults.iteritems(), key = lambda item: item[1], reverse = False)
        return searchResults

    def searchByStructure(self, queryStructures):  # 计算每张图与目标图的结构空间距离并存储到字典里
        searchResults = {}

        with open(self.structureIndexPath) as indexFile:
            reader = csv.reader(indexFile)
            for line in reader:
                structures = []
                for structure in line[1:]:
                    structure = structure.replace("[", "").replace("]", "")
                    structure = re.split("\s+", structure)
                    if structure[0] == "":
                        structure = structure[1:]
                    structure = [float(eachValue) for eachValue in structure]
                    structures.append(structure)
                distance = self.solveStructureDistance(structures, queryStructures)
                searchResults[line[0]] = distance
            indexFile.close()
        # print "structure", sorted(searchResults.iteritems(), key = lambda item: item[1], reverse = False)
        return searchResults
		
    def search(self, colorFeatures, structureFeatures, limit = 5):
        colorResults = self.searchByColor(colorFeatures)
        structureResults = self.searchByStructure(structureFeatures)
        results = {}
        for key, value in colorResults.items():
            results[key] = value + structureResults[key]

        # 通过匹配分数来排序结果
        results = sorted(results.items(), key = lambda item: item[1], reverse = False)
        return results[ : limit]
