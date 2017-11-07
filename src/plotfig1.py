#!/usr/bin/python
#import matplotlib.pyplot as plt
#plt.plot([1,2,3,4])
#plt.ylabel('some numbers')
#plt.show()

import re
import os
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal
from matplotlib.backends.backend_pdf import PdfPages

# plot figure1
mfileName= 'qyyresult'+str(1)
filename = '/home/qyy/'+mfileName+'/part-00000'
x = []
y = []
f1=open(filename,'r')

while True:
      line = f1.readline()
      if not line:
         break
      parts = re.split(r'[,|( |) ]',line)
      x.append(parts[1])
      y.append(parts[2])
     # print(parts[1],parts[2])
f1.close()
plt.rcParams.update({'font.size': 22})
plt.figure(figsize=(25,10))
plt.clf()
y_pos = np.arange(len(x))
y_pos = y_pos[::-1]
temp_x = map(Decimal,x)
sum_x= sum(Decimal(i) for i in x)
result = []
for i in temp_x:
  result.append(i/sum_x*100)
plt.barh(y_pos,result)
plt.xlabel('Percentage (%)')
plt.ylabel('Cagegory(dB)')
plt.yticks(y_pos,y) 
#plt.legend(['x264pt','x265pt'],loc=4)

figure_name = mfileName+'.pdf'
pp=PdfPages(figure_name)
pp.savefig()
pp.close()

plt.show()
plt.close()

