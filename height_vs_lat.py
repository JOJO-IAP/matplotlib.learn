#==============================================================================

#JOJO, IAP, Beiing, Email:mtjsummer@163.com
#2018-02-07

#练习7目标：
#  1.绘制剖面图

#==============================================================================

import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from netCDF4 import Dataset 
import numpy as np

#==============================================================================

# 读入数据
fu = Dataset('./Data/uwnd.mon.ltm.nc')
fv = Dataset('./Data/vwnd.mon.ltm.nc')
# print(f)
'''levels= [ 1000.   925.   850.   700.   600.   500.   400.   300.   250.   200.
   150.   100.    70.    50.    30.    20.    10.]'''

uwnd      = np.array(fu.variables['uwnd'][0,:,:,'100'])
vwnd      = np.array(fv.variables['vwnd'][0,:,:,'100'])
lats      = np.array(fu.variables['lat'][:])
lons      = np.array(fu.variables['lon'][:])
levels    = np.array(fu.variables['level'][:])
#==============================================================================

# 设置常量
lonstart   = 60
lonstop    = 300
latstart   = -90
latstop    = 90
#
nrows      = 1
ncols      = 1
#
loglev = -1.0 * np.log(levels)
cmap = mpl.cm.RdBu_r
colorlev = mpl.ticker.MaxNLocator(nbin=16).tick_values(-50.,50.)
subtitles = ['a','b']
#==============================================================================

# 开始绘图
# 创建图纸,以及两个子图
fig = plt.figure(figsize=(8,6))
axes = []

for i in range(nrows*ncols):
    ax = fig.add_subplot(nrows, ncols, i+1)
    p = ax.contourf(lats, loglev, uwnd, levels=colorlev, cmap=cmap)
    pl = ax.contour(lats, loglev, uwnd, colors='k', linewidths=0.5)
    ax.set_title(subtitles[i], loc='left')
    ax.set_xlabel('latitudes')
    ax.set_ylabel('pressure')
    ax.set_yticks(loglev)
    ax.set_yticklabels(('1000','925','850','700','600','500','400','300','250','200','150','100','70','50','30','20','10'))
    fig.colorbar(p, ax=ax)
    # ax 传递给axes
    axes.append(ax)
#==============================================================================
#调整布局
fig.subplots_adjust(left=None, bottom=None, right=None, top=0.9, hspace=0.3, wspace=None)
# 添加主标题
figtitle = 'Height vs latitude plot'
t = fig.text(0.5, 0.95, figtitle, horizontalalignment='center')

# 保存图片
# adjust spacing between subplots so ax and ax1 title and ticks labels don't overlay
#plt.show()
fig.savefig('./fig/height_vs_latitude.pdf')
