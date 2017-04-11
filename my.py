#!/usr/bin/python3

from Parser import Parser
import math
import os
import nltk
import sys
import operator
from nltk import stem
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
from nltk.corpus import stopwords

path = './documents'
alltexts = []
i = 0

def querytogo(query):
    
    query = query.lower()

    at = RegexpTokenizer(r'\w+')
    print(at)
    query = at.tokenize(query)
    aq = PorterStemmer()
    aqueryf = [aq.stem(q) for q in query]
    aquerys = [q for q in aqueryf if q not in stopwords.words('english')]
    return aquerys

class build:
    def __init__(self):
        self.documents = []
        self.documentstfidf = []
        self.all_dict ={}
        self.all_dict_idf ={}
        self.all_dict_tfidf = {}
    def addDocument(self, doc_name, list_of_words):
        doc_dict = {}
        for w in list_of_words:
            doc_dict[w] = doc_dict.get(w, 0.) +1.0
            self.all_dict[w] = self.all_dict.get(w, 0.0) + 1.0
        
        self.documents.append([doc_name, doc_dict])
    def getdocuments(self):
        #print(self.documents)
        #print(self.all_dict)
        print(len(self.documents))
    def calculateidf(self):
        length = len(self.documents)
        for eachword in self.all_dict:
            countofword = self.all_dict[eachword]
            #print(eachword)
            thiswordcount = 0
            #spec = lambda L: L[1:] == [eachword]
            for doc in self.documents:
                for a in doc[1]:
                    if a == eachword:
                        thiswordcount += 1
                        break

            self.all_dict_idf[eachword] = 1+math.log(length/thiswordcount)

        for doc in self.documents:
            doc_dict_tfidf = {}
            for a in doc[1]:
                doc_dict_tfidf[a] = doc[1][a]*self.all_dict_idf[a]
            self.documentstfidf.append([doc[0], doc_dict_tfidf])
        
        #print(self.all_dict_idf)
        #print(self.documentstfidf)
    def tfcos(self, query):
        ranking = {}
        for doc in self.documents:
            upper = 0
            dl = 0.0
            ql = len(query)
            for q in query:
                if q in doc[1]:
                    upper += doc[1][q]
            for d in doc[1]:
                dl += math.pow(doc[1][d], 2)
            tfcosdoc = upper/(math.sqrt(dl)* math.sqrt(ql))
            ranking[doc[0]] = tfcosdoc
        rankingsort = sorted(ranking.items(), key=operator.itemgetter(1))
        rankingsort.reverse()
        self.showfirstfive(rankingsort)      
   
  
    def tfjaccard(self, query):
        ranking = {}
        for doc in self.documents:
            print(doc)
            upper = 0
            dl = 0.0
            for q in query:
                if q in doc[1]:
                    upper += doc[1][q]
            for d in doc[1]:
                dl += doc[1][d]
            ranking[doc[0]] = upper/dl
        rankingsort = sorted(ranking.items(), key=operator.itemgetter(1))
        rankingsort.reverse()
        self.showfirstfive(rankingsort)


    def tfidfcos(self, query):
        ranking = {}
        for doc in self.documentstfidf:
            #get the upper place
            upper = 0
            dl = 0.0
            ql = len(query)
            for q in query:
                if q in doc[1]:
                    upper += doc[1][q] 
            
            for d in doc[1]:
                dl += math.pow(doc[1][d], 2)
           
            tfidfdoc = upper/(math.sqrt(dl)*math.sqrt(ql))
            ranking[doc[0]] = tfidfdoc
        
        rankingsort = sorted(ranking.items(), key=operator.itemgetter(1))
        rankingsort.reverse()
        self.showfirstfive(rankingsort)
    def tfidfjaccard(self, query):
        ranking = {}
        for doc in self.documentstfidf:
            upper = 0
            dl = 0.0
            for q in query:
                if q in doc[1]:
                    upper += doc[1][q]
            for d in doc[1]:
                dl += doc[1][d]
            ranking[doc[0]] = upper/dl
        
        rankingsort = sorted(ranking.items(), key=operator.itemgetter(1))
        rankingsort.reverse()
        self.showfirstfive(rankingsort)

    def showfirstfive(self, rankingsort):
        i = 0
        print("DocId      Score")
        for item, v in rankingsort:
            print(item,"   ",round(v, 8))
            i += 1
            if i+1 == 11:
                break
        print('\n\n')

dictionary = build();

for filenames in os.listdir(path):
    #print(filenames)
    if i == 2047:
        break
    i = i+1
    f = open(path+'/'+filenames,'r+')
    todic = filenames[:-8]
    text = f.read()
    text = text.lower()

    tokenizer = RegexpTokenizer(r'\w+')
    aftertoken = tokenizer.tokenize(text)    
    
    steemer = PorterStemmer()
    afterstem = [steemer.stem(aftertokeneach) for aftertokeneach in aftertoken]
    
    #print(afterstem)
    aftertokennostop = [word for word in afterstem if word not in stopwords.words('english')]
    #print(aftertokennostop) 
    dictionary.addDocument(todic, aftertokennostop)
    
#caaulate idf of each words
print("building~~~~ please wait")
dictionary.calculateidf()
print("DONE")

aquery = input('input query:')
back = querytogo(aquery)

print('Term Frequency (TF) Weighting + Cosine Similarity: ')
#dictionary.tfcos(back)

print('Term Frequency (TF) Weighting + Jaccard Similarity: ')
dictionary.tfjaccard(back)

print('TF-IDF Weighting + Cosine Similarity: ')
#dictionary.tfidfcos(back)

print('TF-IDF Weighting + Jaccard Similarity: ')
dictionary.tfidfjaccard(back)

#dictionary.tfidfcos(aquerys)
