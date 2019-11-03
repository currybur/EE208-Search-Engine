# Final Project of Introduction to Electric Engineering(type-C)(EE208)
Implemented a searching engine(both text-based and image-based), and set up a website to illustrate. Members include Hua Zeyu and Liu Hanwen.
## Dataset
Crawled text and pictures from official websites of National Museum of China, the Palace Museum, and Shaanxi History Museum.
## Web Framework
[web.py](http://webpy.org/) is used.
## User Interface Design
Thanks to Hua Zeyu, our website seems to be very high-level!
## Text-based Search
Apply Lucene to establish text index and to search. Word segmentation work is done by [jieba](https://github.com/fxsjy/jieba).
## Image-based Search
Based on this [blog](https://blog.csdn.net/coderhuhy/article/details/46575667), use structural and colored features to match queried picture in the picture library. Also can match some unstored similar pictures.
## Additional Functions
Liu Hanwen also implemented some multimedia functions, such as voice-text conversion, OCR and some face detection work, which haven't been attached to final version of our website.