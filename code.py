#!/usr/bin/env python
import web
from web import form
from image_search_engine_example import searchEngine as simg
from voice import combine
from ocr import baidu
from web.wsgiserver import CherryPyWSGIServer
import urllib
import os
#import SearchFiles_site as sc
#import SearchFiles_img as sci
import SearchFiles as sc


import sys, os, lucene
import jieba
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version

import cv2
#from PIL import Image
#CherryPyWSGIServer.ssl_certificate = "/root/final/server.crt"
#CherryPyWSGIServer.ssl_private_key = "/root/final/server.key"
reload(sys)
sys.setdefaultencoding('utf-8')

INDEX_DIR = "IndexFiles.index"



STORE_DIR = "index"


urls = (
      '/', 'text',
  '/audio', 'audio',
    '/imgsrc', 'imgsrc',
    '/imgresult', 'imgresult',
    '/textresult', 'textresult',
    '/audioresult', 'audioresult',
      '/sxm', 'sxm',
      '/ocr','ocr',
  '/cnm', 'cnm',
  '/dpm', 'dpm',
  '/ML', 'MonaLisa',
    '/about', 'about',
     '/Christmas', 'Christmas',
)

render = web.template.render('templates') # your templates




def text_search(command):
    # base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    vm_env.attachCurrentThread()
    result = sc.run(searcher1, analyzer, command)

    return result
'''
def text_img(command):
    # base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    vm_env.attachCurrentThread()
    result = sci.run(searcher2, analyzer, command)

    return result
'''
class text:

    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render.text()

class textresult:
    def GET(self):
        try:
            user_data = web.input()
            a = text_search(user_data.keyword)

            print(a[0]['detail'])
            return render.textresult(a, user_data.keyword, '')
        except:
            web.header("Content-Type", "text/html; charset=utf-8")
            return render.textresult('', '', '')

class audio:

    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render.audio()

    def POST(self):
        try:
            x = web.input(myfile={})

            filedir = './static/stored'  # change this to the directory you want to store the file in.
            if 'myfile' in x:  # to check if the file-object is created
                filepath = x.myfile.filename.replace('\\', '/')  # replaces the windows-style slashes with linux ones.
                filename = filepath.split('/')[-1]  # splits the and chooses the last part (the filename with extension)
                try:
                    fout = open(filedir + '/' + filename, 'wb')  # creates the file where the uploaded file should be stored
                    fout.write(x.myfile.file.read())  # writes the uploaded file to the newly created file.
                    fout.close()  # closes the file, upload complete.
                except:
                    print("exist\n")
                res = combine.recog(filedir + '/' + filename)
                a = text_search(res)
                return render.audioresult(a, res, '')
        except Exception, e:
            print e
            return render.audioresult('', '', '')

class audioresult:
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render.audioresult('', '', '')

    def POST(self):
        x = web.input(myfile={})
        filedir = './static/stored'  # change this to the directory you want to store the file in.
        if 'myfile' in x:  # to check if the file-object is created
            filepath = x.myfile.filename.replace('\\', '/')  # replaces the windows-style slashes with linux ones.
            filename = filepath.split('/')[-1]  # splits the and chooses the last part (the filename with extension)
            fout = open(filedir + '/' + filename, 'wb')  # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read())  # writes the uploaded file to the newly created file.
            fout.close()  # closes the file, upload complete.

            res = combine.recog(filedir + '/' + filename)
            a = text_search(res)
            return render.audioresult(a, res,'')

class imgsrc:

    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render.imgsrc()


    def POST(self):
        try:
            x = web.input(myfile={})

            filedir = './static/stored'  # change this to the directory you want to store the file in.
            if 'myfile' in x:  # to check if the file-object is created
                filepath = x.myfile.filename.replace('\\', '/')  # replaces the windows-style slashes with linux ones.
                filename = filepath.split('/')[-1]  # splits the and chooses the last part (the filename with extension)
                fout = open(filedir + '/' + filename, 'wb')  # creates the file where the uploaded file should be stored
                fout.write(x.myfile.file.read())  # writes the uploaded file to the newly created file.
                fout.close()  # closes the file, upload complete.


                res = simg.search(filedir + '/' + filename)

                imgs = []
                for img in res:
                    info = []
                    url = './static/dataset/' + img
                    info.append(url) #  static url
                    info.append(img) #  name
                    path = './static/details/' + img[:-4] + '.txt'
                    # print path
                    try:
                        f = open(path,'r')
                        detail = f.readlines()
                        hyplk = detail[0]
                        orgimg = detail[1]
                        info.append(hyplk) #  origin page
                        info.append(orgimg) #  origin img url
                        imgs.append(info)
                        f.close()
                    except:
                        info.append('/')
                        info.append('/')
                        imgs.append(info)

                return render.imgresult(imgs)
        except Exception, e:
            print e
            return render.imgresult('')


class imgresult:
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render.imgresult('')

    def POST(self):
        x = web.input(myfile={})
        filedir = './static/stored'  # change this to the directory you want to store the file in.
        if 'myfile' in x:  # to check if the file-object is created
            filepath = x.myfile.filename.replace('\\', '/')  # replaces the windows-style slashes with linux ones.
            filename = filepath.split('/')[-1]  # splits the and chooses the last part (the filename with extension)
            fout = open(filedir + '/' + filename, 'wb')  # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read())  # writes the uploaded file to the newly created file.
            fout.close()  # closes the file, upload complete.

            res = simg.search(filedir + '/' + filename)

            imgs = []
            for img in res:
                info = []
                url = './static/dataset/' + img
                info.append(url)  # static url
                info.append(img)  # name
                path = './static/details/' + img[:-4] + '.txt'
                # print path
                try:
                    f = open(path, 'r')
                    detail = f.readlines()
                    hyplk = detail[0]
                    orgimg = detail[1]
                    info.append(hyplk)  # origin page
                    info.append(orgimg)  # origin img url
                    imgs.append(info)
                    f.close()
                except:
                    info.append('/')
                    info.append('/')
                    imgs.append(info)

            return render.imgresult(imgs)

class ocr:

    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render.ocr()


    def POST(self):
        try:
            x = web.input(myfile={})

            filedir = './static/stored'  # change this to the directory you want to store the file in.
            if 'myfile' in x:  # to check if the file-object is created
                filepath = x.myfile.filename.replace('\\', '/')  # replaces the windows-style slashes with linux ones.
                filename = filepath.split('/')[-1]  # splits the and chooses the last part (the filename with extension)
                try:
                    fout = open(filedir + '/' + filename, 'wb')  # creates the file where the uploaded file should be stored
                    fout.write(x.myfile.file.read())  # writes the uploaded file to the newly created file.
                    fout.close()  # closes the file, upload complete.
                except:
                    print("exist\n")

                res = baidu.search(filedir + '/' + filename)
                print(res)
                try:
                    a = text_search(res)
                except:
                    a = ''
                return render.textresult(a, res, '')
        except Exception, e:
            print e
            return render.audioresult('', '', '')

class sxm:
    def GET(self):
        return render.sxm()


class cnm:
    def GET(self):
        return render.cnm()


class dpm:
    def GET(self):
        return render.dpm()


class MonaLisa:
    def GET(self):
        return render.MonaLisa()


class Christmas:
    def Get(self):
        return render.Christmas()


class about:
    def GET(self):
        return render.about()

if __name__ == "__main__":
    STORE_DIR1 = "bwgindex"
    #STORE_DIR2 = "index_img"
    vm_env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    # base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory1 = SimpleFSDirectory(File(STORE_DIR1))
    searcher1 = IndexSearcher(DirectoryReader.open(directory1))
    #directory2 = SimpleFSDirectory(File(STORE_DIR2))
    #searcher2 = IndexSearcher(DirectoryReader.open(directory2))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    app = web.application(urls, globals(), False)
    app.run()

