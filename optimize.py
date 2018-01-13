# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 23:37:57 2017

@author: t-shaith
"""

import threads
import ast

f1 = open("C:\\FILES\\status.txt", "a")

f1.write("Started");
g = open("C:\\FILES\\input.txt", "r")
choice = int(g.readline())
n = int(g.readline())
pref = int(g.readline())
nclus = int(g.readline())
data = ast.literal_eval(g.readline())
names = []
for i in range(1,n+1):
    names.append(str(i)) 

depo = ast.literal_eval(g.readline())
deponame = ast.literal_eval(g.readline())

g.close();

f1.write("Read");
try:
    x = threads.totalTSP(choice,n,pref,data=data,names=names,depo=depo, deponame=deponame)
    print(x)
except Exception as e:
    f1.write("ERROR"+e)
    f1.close()

f1.write("Algo done")

try:
    f = open("C:\\FILES\\outit.txt", "w+")
    for i in range(len(x)):
        line = ""
        for j in range(len(x[i])):
            line = line + str(x[i][j]) + ","
        line = line + "\n"
        f.write(line)
except Exception as e:
    f1.write("Write error")
    f1.close();

f1.write("Write done")
f1.close();
#f.write(str(x))  # python will convert \n to os.linesep
f.close()