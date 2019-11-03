#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene
import jieba
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def run(searcher, analyzer,command):
        command = ' '.join(jieba.cut(command))
        if command == '':
            return

        query = QueryParser(Version.LUCENE_CURRENT, "contents", analyzer).parse(command)
        scoreDocs = searcher.search(query, 10).scoreDocs
        results = []

        for i, scoreDoc in enumerate(scoreDocs):
            doc = searcher.doc(scoreDoc.doc)
            result = {}
            '''rltd = []
            try:
                pos = doc.get('detail').index(command)
                for i in range(max(0,pos-3),min(pos+4,len(doc.get('detail')))):
                    rltd.append(doc.get('detail')[i])
            except:
                rltd'''
            detail = doc.get('detail')
            museum = detail.split()[-1]
            if(len(detail.split())==2):
                detail = detail.split()[0]
            if(len(detail)>100):
                detail = detail.split()[1] + '......'
            result["detail"]= detail
            result["museum"] = museum
            result["name"] = doc.get('name')
            result["page"] = doc.get('page')
            result["img"] = doc.get('img')
            results.append(result)
            #print 'score:', scoreDoc.score
            # print 'explain:', searcher.explain(query, scoreDoc.doc)
        return results

