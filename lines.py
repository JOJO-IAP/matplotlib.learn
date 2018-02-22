#==============================================================================

#JOJO, IAP, Beiing, Email:mtjsummer@163.com
#2018-02-09

#练习1目标：
#  1.绘制线图
#  2.添加legend
#  3.添加title


#==============================================================================
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt

#read in EAWM index
f = Dataset("./index.nc")
EAWMI = np.array(f.variables['EAWMI_ra'])
EAWMIres = np.array(f.variables['EAWMIres_ra'])
year = np.arange(1948,2017,1)
#print(EAWMI,EAWMIres)

#plot the index
fig, ax = plt.subplots(figsize=(9,4))

ax.plot(year, EAWMI, 'r--', linewidth=1.0, label='EAWMI')
ax.plot(year, EAWMIres, 'b--', label='EAWMIres')
ax.set(xlabel='year', ylabel='index', title='EAWM index')
ax.legend(loc='best')
plt.savefig('../fig/index.eps')
