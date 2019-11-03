import color_descriptor
import structure_descriptor
import glob
import argparse
import cv2

idealBins = (8, 12, 3)
colorDesriptor = color_descriptor.ColorDescriptor(idealBins)

output = open("colorindex.csv","w")#arguments["colorindex"], "w")

for imagePath in glob.glob("D:/Photos/airplanes_side"+ "/*.jpg"): #arguments["dataset"] + "/*.jpg"):
    imageName = imagePath[imagePath.rfind("/") + 1 : ]
    image = cv2.imread(imagePath)
    features = colorDesriptor.describe(image)
    # write features to file
    features = [str(feature).replace("\n", "") for feature in features]
    output.write("%s,%s\n" % (imageName, ",".join(features)))
# close index file
output.close()

kps = 100
structureDescriptor = structure_descriptor.StructureDescriptor(kps)

output = open("structureindex.csv", "w")#arguments["structureindex"], "w")

for imagePath in glob.glob("D:/Photos/airplanes_side" + "/*.jpg"):
    imageName = imagePath[imagePath.rfind("/") + 1 : ]
    image = cv2.imread(imagePath)
    structures = structureDescriptor.describe(image)
    # write structures to file
    structures = [str(structure).replace("\n", "") for structure in structures]
    output.write("%s,%s\n" % (imageName, ",".join(structures)))
# close index file
output.close()
