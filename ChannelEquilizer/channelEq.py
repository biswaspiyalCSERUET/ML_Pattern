# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 18:37:40 2018

@author: Asus
"""

import numpy as np
from scipy.stats import multivariate_normal

with open('trainOnline.txt') as f:
    content = f.read().split("\n")
with open('testOnline.txt') as f:
    testcontent = f.read().split("\n")
    
    
def split(s, delim):
    words = []
    word = []
    for c in s:
        if c not in delim:
            word.append(c)
        else:
            if word:
                words.append(''.join(word))
                word = []
    if word:
        words.append(''.join(word))
    return words

def loadfile(filename):
    file = open(filename, "r")
    rows = list()
    for line in file:
        vals = split(line, [' ' ,'\t', '\n'])
        rows.append(vals)
    return rows
   
class channelClass:
    def __init__(self,contents,p):
        inputs=loadfile('input.txt')
        self.h = np.array(inputs[0],dtype=float)
        self.n=len(self.h)
        self.mu=float(inputs[1][0])
        self.var=np.array(inputs[1][1],dtype=float)
        lst =[]
        for i in range(len(contents[0])-1):
            ans=float(contents[0][i+1])*self.h[0]+float(contents[0][i])*self.h[1]\
            +np.random.normal(self.mu,self.var)
            lst.append(ans)
        l=p
        dictionary=[]
        clusterMeans=[]
        clusterCovs=[]
        clusterPriorProb=[]
        for i in range(np.power(l+1,2)-1):
            dictionary.append([])
            clusterMeans.append([])
            clusterCovs.append([])
            clusterPriorProb.append([])
        
        for i in range(l,len(content[0])):
            bs=''
            for j in range(0,l+1):
                bs+=content[0][i-j]
            #bs=bs[::-1]
            clss=int(bs,2)
            xv=[]
            for k in range(0,l):
                xv.append(lst[i-l+k])
            xv.reverse()
            dictionary[clss].append(xv)
        for i in range(len(dictionary)):
            countermean=np.mean(np.array(dictionary[i]).T,axis =1)
            countercov=np.cov(np.array(dictionary[i]).T)
            clusterMeans[i]=countermean
            clusterCovs[i]=countercov
            clusterPriorProb[i]=(len(dictionary[i]) / (len(lst)-1))
            
        self.dictionary=dictionary
        self.clusterMeans=clusterMeans
        self.clusterCovs=clusterCovs
        self.clusterPriorProb=clusterPriorProb
    
    def distortedOutput(self,contents):
        lst =[]
        for i in range(len(contents[0])-1):
            ans=float(contents[0][i+1])*self.h[0]+float(contents[0][i])*self.h[1]\
            +np.random.normal(self.mu,self.var)
            lst.append(ans)
        return lst    


l=2
model=channelClass(content,l)
#print(model.clusterCovs)

testXvector=model.distortedOutput(testcontent)



#l=2
pathsarray=np.zeros((len(testXvector)-1,np.power(l+1,2)-1), dtype=float)+np.finfo(np.float).eps


for i in range(len(testXvector)-1):
    #print(i)
    if(i==0):
        xv=[]
        xv.append(testXvector[i])
        xv.append(testXvector[i+1])
        xv.reverse()
        for j in range(np.power(l+1,2)-1):
            pathsarray[i][j]+=np.log(model.clusterPriorProb[j])+multivariate_normal.pdf(xv, model.clusterMeans[j], model.clusterCovs[j])
            #print(multivariate_normal.pdf(xv, model.clusterMeans[j], model.clusterCovs[j]))
    else:
        xv=[]
        xv.append(testXvector[i])
        xv.append(testXvector[i+1])
        xv.reverse()
        for j in range(np.power(l+1,2)-1):
            par=(j%4)*2
            parmax=max(pathsarray[i-1][par],pathsarray[i-1][par+1])
            pathsarray[i][j]+=parmax+np.log(0.5)+multivariate_normal.pdf(xv, model.clusterMeans[j], model.clusterCovs[j])

output=[]
lastNode=0
for i in range(len(pathsarray)-1,0,-1):
    #print(i)
    if(i==len(pathsarray)-1):
        row=pathsarray[i]
        lastNode=np.argmax(row)
        output.append(lastNode)
    #print(lastNode)
    par=(lastNode%4)*2
    if(pathsarray[i-1][par] > pathsarray[i-1][par+1]):
        lastNode=par
    else:
        lastNode=par+1
    output.append(lastNode)

output.reverse()    
newFile=[]
for i in range(len(output)):
    if(i==0):
        strr='{0:03b}'.format(output[i])
        newFile.append(strr[2])
        newFile.append(strr[1])
        newFile.append(strr[0])
        continue
    strr='{0:03b}'.format(output[i])
    #print(strr)
    newFile.append(strr[0])
    
with open('newTest.txt', 'w') as f:
    for item in newFile:
        f.write("%s" % item)        




















