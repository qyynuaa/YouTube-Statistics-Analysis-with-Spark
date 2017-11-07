#!/usr/bin/python
import re
import os
import numpy as np
import itertools
import matplotlib.pyplot as plt
from decimal import Decimal

#rfileName = 'youtubevideostat.txt'
rfileName = 'merged_num.txt'
wfilename = 'newmerged_num.txt'
f1=open(rfileName,'r')
f2=open(wfilename,'w')
#line = f1.readline()

#parts = re.split(r'[\t]',line)
i = 0
while True:
      line = f1.readline()
      #print line
      if not line:
         break
      parts = line.split()
      mstr= str(i)
      for j in range (1, len(parts)+1):
        mstr= mstr + " " + str(j)+":" + parts[j-1]
      #print mstr
      f2.write(mstr+"\n")
      i= i+1
      #parts = re.split(r'[\t]',line)
      #currentTime = parts[1]
      #YouTubeTime = "2005-02-14T00:00:00.000Z"
      #x.append(parts[1])
      #y.append(parts[2])
      #print(parts[1],parts[2])
f1.close()
f2.close()

