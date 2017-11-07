#!/usr/bin/python
#import matplotlib.pyplot as plt
#plt.plot([1,2,3,4])
#plt.ylabel('some numbers')
#plt.show()

import re
import os
import numpy as np
import itertools
import matplotlib.pyplot as plt
from decimal import Decimal
from matplotlib.backends.backend_pdf import PdfPages
colors =['b','r','g','k','c']
cc = itertools.cycle(colors)
# plot figure1
plt.figure()
plt.clf()
for i in range(1):
  mfileName= 'qyyresult'+str(i+7)
  filename = '/home/qyy/'+mfileName+'/part-00000'

  x = []
  y = []

  f1=open(filename,'r')
  c = next(cc)
  while True:
      line = f1.readline()
      if not line:
         break
      parts = re.split(r'[,|( |) ]',line)
      x.append(parts[1])
      y.append(parts[2])
      #print(parts[1],parts[2])
  f1.close()
  plt.yscale('log') 
  plt.xscale('log') 
  plt.plot(x,y,'-x', color = c)
  


plt.xlabel('Rank')
plt.ylabel('Number of Views')
#plt.yticks(y_pos,y) 
#plt.legend(['0-4 weeks','1-4 weeks','2-4 weeks','3-4 weeks'], loc=3)

figure_name = 'qyyresult'+str(7)+'.pdf'
pp=PdfPages(figure_name)
pp.savefig()
pp.close()

plt.show()
plt.close()

