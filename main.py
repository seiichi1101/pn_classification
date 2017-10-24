# -*- coding: utf-8 -*-
import re
import MeCab
import sys
import io
import time
import csv

def getDocs(documents):
    m='(((http|https).+?($|\n|\z))|(@.+?(:| |\n))|(\n))'
    documents = [re.sub(m, " ", text) for text in documents]
    return documents

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # Here
    args = sys.argv

    documents = {}
    f = open(args[1])
    line = f.readline() # 1行を文字列として読み込む(改行文字も含まれる)
    while line:
        documents.update({line.replace('\n',''): 0})
        line = f.readline()
    f.close
    print(documents)

    f = open('vocabulary.trim')
    line = f.readline() # 1行を文字列として読み込む(改行文字も含まれる)
    vocabularies={}
    while line:
        vocabularies.update({line.split('\t')[0] : int(line.split('\t')[1])})
        line = f.readline()
    f.close


    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse('')
    for key_d in documents:
        node = tagger.parseToNode(key_d)
        while node:
            if (node.surface in vocabularies):
                documents[key_d] += vocabularies[node.surface]
            node = node.next

    f = open('output-files/'+time.strftime("%Y%m%d%H%M%S")+'.txt','a')
    for key_d in documents:
#        if (documents[key_d] not in [-1, 0, 1]):
        print (documents[key_d], "\t", key_d)
        f.write(str(documents[key_d])+"\t"+key_d+"\n")
    f.close()
