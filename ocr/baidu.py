# encoding=utf-8
from aip import AipOcr

# config
# TOP SECRET CAN NOT UPLOAD!!!
# HANWEN'S MONEY ACCOUNT
config = {
    'appId': '15301589',
    'apiKey': '8Ef6aG6UVuVUk7A4FX7XuliU',
    'secretKey': 'NmoGnZDwq1oNM5Lp1SAs2c4XT4kGzgKr'
}
client = AipOcr(**config)



def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def search(img):
    image = get_file_content(img)

    # 调用通用文字识别（高精度版）
    result = client.basicAccurate(image)
    result= result['words_result']
    for i in result:
        return(i['words'])

#print(search('ocr2.jpg'))
