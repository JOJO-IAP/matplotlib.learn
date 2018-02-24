#==============================================================================

#JOJO, IAP, Beiing, Email:mtjsummer@163.com
#2018-02-09

#练习5目标：
#  1.调整函数形式cartopy.map,绘制区域地图
#  2.绘制4个子图
#  3.调整colorbar，共享一个coloarbar并放在图底
#  4.叠加显著性检验
#  5.解决数据终点白线问题 add_cyclic_point
#  6.mask缺省值

#==============================================================================

import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.util import add_cyclic_point
from netCDF4 import Dataset 
import numpy as np
from matplotlib.font_manager import FontProperties

#==============================================================================

#读入数据
f = Dataset('omega.nc')
#print(f)
data         = np.array(f.variables['varin_C'][::2,0,:,:])
data_mask    = np.ma.masked_where(data > 10**36, data)
prob         = np.array(f.variables['varin_C'][::2,1,:,:])
prob_mask    = np.ma.masked_where(prob > 10**36, prob)
lats         = np.array(f.variables['lat'][:])
lons         = np.array(f.variables['lon'][:])
#print(data.min(), data.max())

'''add cyclic point 
数据为经圈360度时，需要使数据闭环
from cartopy.util import add_cyclic_point
add_cyclic_point(data, coord=None, axis=-1)
returns cyclic_data, cyclic_coord'''
cyclic_data,cyclic_lons = add_cyclic_point(data_mask, coord=lons)
cyclic_prob = add_cyclic_point(prob_mask)

#==============================================================================

#绘制区域地图函数
def make_map(ax, projection, resolution, mapextent, xnum, ynum):
    ax.set_extent(mapextent, crs=projection)
    ax.coastlines(resolution, linewidth=0.5)
    '''标注坐标轴 注意lon的取值范围为-180:180；lat取值范围为-90：90'''
    ax.set_xticks(np.linspace(mapextent[0], mapextent[1], num=xnum, endpoint=True), crs=projection)
    ax.set_yticks(np.linspace(mapextent[2], mapextent[3], num=ynum, endpoint=True), crs=projection)
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    return ax

'''注意画经圈360的设置：projection=ccrs.PlateCarree(central_longitude=180),
lonstart=60, lonstop=360(即代表0E), xnum=6'''
#==============================================================================

#定义常量
projection = ccrs.PlateCarree()
resolution = '110m'
lonstart   = 60. 
lonstop    = 180.
latstart   = -10.
latstop    = 80.
mapextent  = [lonstart, lonstop, latstart, latstop]
xnum       = 5
ynum       = 4
nrows      = 2
ncols      = 2
siglevel   = np.array([-1.0, -0.95, 0.95, 1.0])
subtitles  = ['1)', '2)', '3)', '4)']
#==============================================================================

#设置colorbar
# Set the colormap and norm to correspond to the data for which the colorbar will be used
# 指定colorbar
cmap = mpl.cm.PiYG
# 设定每个图的colormap和colorbar所表示范围是一样的，归一化
levelmin = data.min()
levelmax = abs(levelmin)
norm = mpl.colors.Normalize(vmin=levelmin, vmax=levelmax)
# 设置levels
levels = mpl.ticker.MaxNLocator(nbin=16).tick_values(levelmin, levelmax)

#==============================================================================

#创建图纸,以及两个子图
fig  = plt.figure(figsize=(8, 8))

axes = []

for i in range(nrows*ncols):
    '''创建ax'''
    ax = fig.add_subplot(nrows, ncols, i+1, projection=ccrs.PlateCarree(central_longitude=180) )
    '''绘地图'''
    ax = make_map(ax, projection, resolution, mapextent, xnum, ynum)
    '''添加标题'''
    ax.set_title(subtitles[i], loc='left')
    '''填色'''
    p = ax.contourf(cyclic_lons, lats, cyclic_data[i,:,:], levels=levels, cmap=cmap, transform=projection)
    '''绘等值线'''
    #pl = ax.contour(cyclic_lons, lats, cyclic_data[i,:,:], levels=levels, linewidths=0.4, colors='w', transform=projection)
    '''叠加显著性检验'''
    pp = ax.contourf(cyclic_lons, lats, cyclic_prob[i,:,:], levels=siglevel, colors='none', hatches=['.', None, '.'], transform=projection)
    #ppl= ax.contour(cyclic_lons, lats, cyclic_prob[i,:,:], levels=siglevel, linewidths=0.5, colors='r', transform=projection)

    '''将ax传递给数组'''
    axes.append(ax)

#添加colorbar
#调整画布布局，给colorbar空间
fig.subplots_adjust(bottom=0.2, right=0.9, top=0.85, wspace=0.2,hspace=0.2)
#添加coloarbar
cax = fig.add_axes([0.2, 0.14, 0.6, 0.02])
cb  = fig.colorbar(p, cax=cax, orientation='horizontal')

#添加主标题
figtitle = 'Title'
t = fig.text(0.5, 0.9, figtitle, horizontalalignment='center', fontproperties=FontProperties(size=16))
#保存图片
fig.savefig("./fig/cartopy.contourf.eps")
