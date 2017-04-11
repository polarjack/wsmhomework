#!/usr/bin/python3

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


def returnquery(index, doct):
    for d in doct:
        if d[0] == index:
            return d[1]


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
        print(len(self.documents))
    def calculateidf(self):
        length = len(self.documents)
        for eachword in self.all_dict:
            countofword = self.all_dict[eachword]
            thiswordcount = 0
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
            upper = 0
            dl = 0.0
            for q in query:
                if q in doc[1]:
                    if doc[1][q] <= 1:
                        upper += doc[1][q]
                        dl -= doc[1][q]
                        dl += 1
                    else:
                        upper += 1
                        
            for d in doc[1]:
                dl += doc[1][d]
            ranking[doc[0]] = upper/dl
        rankingsort = sorted(ranking.items(), key=operator.itemgetter(1))
        rankingsort.reverse()
        self.showfirstfive(rankingsort)


    def tfidfcos(self, query):
        ranking = {}
        for doc in self.documentstfidf:
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
                    if doc[1][q] <= 1:
                        upper += doc[1][q]
                        dl -= doc[1][q]
                        dl += 1
                    else:
                        upper += 1
            for d in doc[1]:
                dl += doc[1][d]
            ranking[doc[0]] = upper/dl
        
        rankingsort = sorted(ranking.items(), key=operator.itemgetter(1))
        rankingsort.reverse()
        self.showfirstfive(rankingsort)

    def feedback(self, query):
        ranking = {}
        for doc in self.documentstfidf:
            upper = 0
            dl = 0.0
            for q in query:
                if q in doc[1]:
                    if doc[1][q] <= 1:
                        upper += doc[1][q]
                        dl -= doc[1][q]
                        dl += 1
                    else:
                        upper += 1
            for d in doc[1]:
                dl += doc[1][d]
            ranking[doc[0]] = upper/dl
        
        rankingsort = sorted(ranking.items(), key=operator.itemgetter(1))
        rankingsort.reverse()
        
        feedin = rankingsort[0][0] 
        feedinq = returnquery(feedin,self.documentstfidf)
        
        for fdq in feedinq:
            feedinq[fdq] *= 0.5
        for q in query:
            if q in fdq:
                feedinq[fdq] += 1
                del query[query.index(q)]
        
        if len(query) != 0:
            for q in query:
                feedinq[q] = 1
        ranking2 = {} 
        for doc in self.documentstfidf:
            upper = 0
            dl = 0.0
            for q in feedinq:
                if q in doc[1]:
                    if doc[1][q] <= 1:
                        upper += doc[1][q]
                        dl -= doc[1][q]
                        dl += 1
                    else:
                        upper += 1
            for d in doc[1]:
                dl += doc[1][d]
            ranking2[doc[0]] = upper/dl
        
        rankingsort2 = sorted(ranking2.items(), key=operator.itemgetter(1))
        rankingsort2.reverse()
        self.showfirstfive(rankingsort2)
        

    def showfirstfive(self, rankingsort):
        i = 0
        print('\n')
        print("DocId      Score")
        for item, v in rankingsort:
            print(item,"   ",round(v, 8))
            i += 1
            if i+1 == 6: #change the nubmer if you want to see more ranking results
                break

dictionary = build();

for filenames in os.listdir(path):
    f = open(path+'/'+filenames,'r+')
    todic = filenames[:-8]
    text = f.read()
    text = text.lower()

    tokenizer = RegexpTokenizer(r'\w+')
    aftertoken = tokenizer.tokenize(text)    
    
    steemer = PorterStemmer()
    afterstem = [steemer.stem(aftertokeneach) for aftertokeneach in aftertoken]
    
    aftertokennostop = [word for word in afterstem if word not in stopwords.words('english')]
    dictionary.addDocument(todic, aftertokennostop)
    
#caaulate idf of each words
print("Building..... Please wait (About 120 seconds sorry= =||) there will be done message after done")
dictionary.calculateidf()
print("Building DONE!!")

aquery = input('input query:')
back = querytogo(aquery)

print('Term Frequency (TF) Weighting + Cosine Similarity: ')
dictionary.tfcos(back)

print('Term Frequency (TF) Weighting + Jaccard Similarity: ')
dictionary.tfjaccard(back)

print('TF-IDF Weighting + Cosine Similarity: ')
dictionary.tfidfcos(back)

print('TF-IDF Weighting + Jaccard Similarity: ')
dictionary.tfidfjaccard(back)

print('Feedback Queries + TF-IDF Weighting + Jaccard Smilarity; ')
dictionary.feedback(back)

