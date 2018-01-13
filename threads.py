# -*- coding: utf-8 -*-

"""
@author: t-shaith
"""

"""
1) read() function that randomly generated X data points
2) K-means and affinity propagation functions which use euclidean distances (output: clusters represented by scatter plots)
3) total call to Branch and Bound TSP solution in newBNB.py
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
from itertools import compress
import math

from urllib2 import Request, urlopen, URLError
import json

#Finds road-distances using Bing Maps API
def roaddistbing (X,Y):
    sumdist = 0
    request = Request('http://dev.virtualearth.net/REST/V1/Routes?wp.0='+str(X[0])+','+str(X[1])+'&wp.1='+str(Y[0])+','+str(Y[1])+'&optmz=timeWithTraffic&key=aIjxQkmbJgHm82K9BfqK~Q62TwAi215slF_lEmd3S7A~AliLx1Cuxw-GEvYo0G3d7Zr3w8quBHba4jfc9i2xNrSfiW7WpIP_jmkuAAG7LTKH')
    
    try:
        response = urlopen(request)
        answer = response.read()
        dic = json.loads(answer)
        resSet = dic['resourceSets'][0]
        res = resSet['resources'][0]
        sumdist = res['travelDistance']
    except URLError as e:
        print ('Error code:', e)
        sumdist = roaddistbing([X[0]+0.5,X[1]+0.5],[Y[0]+0.5,Y[1]+0.5]);
        #pass

    return (sumdist)

    
#first and second min for updating lower bound
def firstMin(dist, i):
    s = np.sort(dist)
    return s[i,1]

def secondMin(dist, i):
    s = np.sort(dist)
    return s[i,2]
    


#recursive branch and bound algorithm (as in levitin, but modified method to update lowerbound)

def TSP(dist, level, lbound, visited, curDist, curPath, finDist, finPath):
    if (level == dist.shape[0]):
        if(dist[curPath[level-1],curPath[0]] != 0 ):
            curTot = curDist + dist[curPath[level-1],curPath[0]]
            if(curTot <= finDist):
                for i in range(level):
                    finPath[i] = curPath[i]
                finPath[level] = curPath[0]
                finDist = curTot
                #print(finDist, finPath)
        return finDist, finPath
    else:
        for i in range(dist.shape[0]):
            if (dist[curPath[level-1],i] != 0 and visited[i] == 0):
                tempDist = curDist + dist[curPath[level-1],i] 
                if (level == 1):
                    tempbound = lbound - (firstMin(dist, curPath[level-1]) + firstMin(dist, i))/2 +  dist[curPath[level-1],i]
                else:
                    tempbound = lbound - (secondMin(dist, curPath[level-1]) + firstMin(dist, i))/2 + dist[curPath[level-1],i]
    
                if(tempbound <= finDist):
                    visited[i] = 1
                    curPath[level] = i
                    fin = TSP(dist,level+1,tempbound,visited,tempDist,curPath,finDist,finPath)
                    finDist = fin[0]
                    finPath = fin[1]
                
                visited[i] = 0
                    
        return finDist,finPath

#main call: initializations and call to recursive TSP function

def maincall(data):
    
    dist = np.zeros((len(data),len(data)))
    
    for i in range (len(data) - 1):
        for j in range (i+1, len(data)):
            dist[i,j] = roaddistbing(data[i],data[j])
            dist[j,i] = roaddistbing(data[j],data[i])
    
    for i in range (len(data)):
        dist[i,i] = 0
           
    finDist = float('inf')
    finPath = np.array([0]*(len(data)+1))
    visited = np.array([0]*len(data))
    
    if(dist.shape[0]==2):
        finPath = [0,1,0]
        finDist = dist[0,1]+dist[1,0]
        return finDist,finPath
    
    
    curPath = np.array([0]*(len(data)+1))
    
    lbound = 0
    for i in range(dist.shape[0]):
        lbound += firstMin(dist,i) + secondMin(dist,i)
        
    lbound = lbound /2
    level = 1
    visited[0] = 1
    curPath[0] = 0
    curDist = 0
           
    return TSP(dist, level, lbound, visited, curDist, curPath, finDist, finPath )



#Read randomly, X number of city data points (default = 50)
#Sample Function call: 
#data = read()
 
def read(X=30):
    final = []
    names = []
    df=pd.read_csv('C:\\FILES\\dataa.csv', sep=',',header=None)
    rows = np.random.choice(df.index.values, X)
    sampled_df = df.iloc[rows]
   
    for row in sampled_df.itertuples():
        final.append([float(row[2]),float(row[3])])
        names.append(row[1])
    return final, names

#K-means clustering using Euclidean distances: returns clusters and draws scatter plot for clusters
#Sample function call:
#clusters = kmean(data,4)

def kmean(X,n):
    random_state = 170
    y_pred = KMeans(n_clusters=n, random_state=random_state).fit_predict(X)
    #plt.scatter(list(zip(*X))[0] ,list(zip(*X))[1]  ,c=y_pred)
    return y_pred


#Affinity Propagation clustering with Euclidean distances : returns clusters and draws scatter plot for clusters
#If preference not mentioned, the median of all similarities is chosen as preference. More negative the preference, lesser the number of clusters

#Sample function call:
#clus_centers, clus_labels = affi_prop (data)
#clus_centers, clus_labels = affi_prop (data, -500)

def affi_prop(X, pref = 0):
    
    if pref == 0:
        y_pred = AffinityPropagation().fit(X)
    else:
        y_pred = AffinityPropagation(preference = pref).fit(X)
    y_centers = y_pred.cluster_centers_indices_
    y_labels = y_pred.labels_
    #n =len(y_centers)
    
    #scatter plot
    """
    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n), colors):
        class_mem = y_labels == k
        cluster_center = X[y_centers[k]]
        #print(cluster_center)
        plt.scatter( list(compress(list(zip(*X))[1], class_mem)), list(compress(list(zip(*X))[0], class_mem)), c=col, marker=".")
        plt.scatter( cluster_center[1],cluster_center[0], c=col, marker="P",)
    """
    return (y_centers, y_labels)
    

#Call to affinity clustering, TSP function in file newBNB.py
#Sample function call : 
#totalTSP(n=30) 
#totalTSP(n=25, depo = [[18.53,73.87],[25.33,83]], deponame = ['Pune','Banaras'])

#first call: default starting point : pune. and 30 random points
#second call: default starting point as mentioned in depo and deponame, 25 random points

from threading import Thread

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self._return = None
    def run(self):
        if self._Thread__target is not None:
            self._return = self._Thread__target(*self._Thread__args,
                                                **self._Thread__kwargs)
    def join(self):
        Thread.join(self)
        return self._return



def threadtarget(k,y_centers,y_labels,data,names,depo,deponame):
    resiter = []
    class_mem = y_labels == k
    tspdata = list(compress(data, class_mem))
    tspnames = list(compress(names, class_mem))
    


    clus_center = data[y_centers[k]]
    
    #find the starting point close to cluster center(exemplar)
    minIndex = -1
    minDist = float('inf') 
    for i in range(len(depo)):
        d = math.sqrt((clus_center[0] - depo[i][0])**2 + (clus_center[1] - depo[i][1])**2)
        if (d < minDist):
            minDist = d
            minIndex = i
 
    
    tspdata = [(depo[minIndex])] + tspdata
    tspnames = [deponame[minIndex]] + tspnames
    
    #print('\n\n\nCluster ',k+1, ':')
    #print('\n', tspdata)
    #print('\n\n', tspnames)
    
    """
    f = open("C:\\FILES\\cluster.txt", "a")
    f.write(str(tspnames))
    f.close()
    """
    #TSP for cluster + depo
    
    fin = maincall(tspdata)
    finDist = fin[0]
    finPath = fin[1]
    

    #print('\nFINAL PATH:\n\n',finPath, finDist)
    
    resiter.append(finDist);
    #print (path)
    for j in range (len(finPath) ):
        resiter.append(tspnames[finPath[j]]);
        #print(tspnames[finPath[j]],'-')
    
    return resiter


def totalTSP(choice=0, n=30, pref=0, nclus=-1,depo=[[18.53,73.87],[25.33,83]], deponame =['Pune','Banaras'], data = [], names = []):
    
    if(choice==0):
        data, names = read(20)
    
    """
    for i in range(len(depo)):
        plt.scatter( depo[i][1], depo[i][0], c="black", marker="*")
    """  
    
    if(nclus == -1):
        
        #clustering
        y_centers, y_labels = affi_prop(data,pref)


        num = len(y_centers)
        #print('\n\nNumber of clusters: ',num)
        #print(y_centers)
        result =[]
        threads = []

        for k in range(num):    #for each cluster:
            t = ThreadWithReturnValue(target=threadtarget, args=(k,y_centers,y_labels,data, names, depo, deponame))
            threads.append(t)
            t.start()
            
        for t in threads:
            result = result+ [t.join()]    
        
        return result
                        
            
            
            
            
            
            
    