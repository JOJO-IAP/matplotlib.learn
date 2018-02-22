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
from matplotlib.font_manager import FontProperties
#==============================================================================

# 读入数据
fu = Dataset('Data/uwnd.mon.ltm.nc')
fv = Dataset('Data/vwnd.mon.ltm.nc')
# print(f)
'''levels= [ 1000.   925.   850.   700.   600.   500.   400.   300.   250.   200.
   150.   100.    70.    50.    30.    20.    10.]'''
# uwnd, vwnd 取100E的值
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
#subplot布局
nrows      = 1
ncols      = 1
#设置y轴的刻度
'''首先要把levels转为loglev，乘以-1是为了使1000hPa在y轴底部。
然后将levels转为list传递给set_yticklable(), 注意set_yticklable的lables参数必须为list of str型'''
loglev = -1.0 * np.log(levels)
ylable = levels.tolist()

#设置cmap
cmap = mpl.cm.viridis
#设置填色levels
if abs(uwnd.min()) >= uwnd.max() :
    datamax = abs(uwnd.min())
else:
    datamax = uwnd.max()


colorlev = mpl.ticker.MaxNLocator(nbin=16).tick_values(-datamax, datamax)
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
    ax.set_title(subtitles[i], loc='left', fontproperties=FontProperties(size=14))
    ax.set_xlabel('latitudes', fontproperties=FontProperties(size=14))
    ax.set_ylabel('pressure', fontproperties=FontProperties(size=14) )
    ax.set_yticks(loglev[::2])
    #ax.set_yticklabels(('1000','925','850','700','600','500','400','300','250','200','150','100','70','50','30','20','10'))
    ax.set_yticklabels(ylable[::2])
    fig.colorbar(p, ax=ax)
    # ax 传递给axes
    axes.append(ax)
#==============================================================================
#调整布局
fig.subplots_adjust(left=None, bottom=None, right=None, top=0.9, hspace=0.3, wspace=None)
# 添加主标题
figtitle = 'Height vs latitude plot'
t = fig.text(0.5, 0.95, figtitle, horizontalalignment='center', fontproperties=FontProperties(size=15))

# 保存图片
# adjust spacing between subplots so ax and ax1 title and ticks labels don't overlay
#fig.savefig('./height_vs_latitude.pdf')
plt.show()
