import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt

#read in EAWM index
f = Dataset("./data_calc/1EAWM.indices.nc")
idx = np.array(f.variables['idx'])
idx_res = np.array(f.variables['idx_res'])
idx_res2 = np.array(f.variables['idx_res2'])
idx_ra = np.array(f.variables['idx_ra'])
idx_res_ra = np.array(f.variables['idx_res_ra'])
idx_res2_ra = np.array(f.variables['idx_res2_ra'])
year = np.arange(1948,2017,1)
#print(EAWMI,EAWMIres)

#plot the index
fig = plt.figure(figsize=(8,6))
'''i = 0, chen's index; =1 yang's index'''
i = 1
'''透明度'''
alpha_v = 0.4 
ax = fig.add_subplot(211)
ax.plot(year,idx[i,:] , 'ro-', linewidth=1.0, label='org', alpha=alpha_v)
ax.plot(year, idx_res[i,:], 'bo--', label='rm Nino3.4', alpha=alpha_v)
ax.plot(year, idx_res2[i,:], color='navy', marker='o',ls='--', label='rm Nino3', alpha=alpha_v)
ax.set(xlabel='year', ylabel='index', title='(a) Raw')
ax.legend(loc=1)

ax2 = fig.add_subplot(212)
ax2.plot(year, idx_ra[i,:], 'ro-', linewidth=1.0, label='org', alpha=alpha_v)
ax2.plot(year, idx_res_ra[i,:], 'bo--', label='rm Nino3.4', alpha=alpha_v)
ax2.plot(year, idx_res2_ra[i,:], color='navy', marker='o',ls='--', label='rm Nino3', alpha=alpha_v)
ax2.set(xlabel='year', ylabel='index', title='(b) AI component')
ax2.legend(loc=1)
fig.tight_layout()

plt.savefig('./fig/01.2.yang.EAWMI.eps')
