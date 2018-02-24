#==============================================================================
#JOJO, IAP, Beiing, Email:mtjsummer@163.com
#==============================================================================

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.path as mpath
from matplotlib.font_manager import FontProperties

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.util import add_cyclic_point

from netCDF4 import Dataset 
import numpy as np

#==============================================================================

#读入数据
f = Dataset('slp.nc')
#print(f)
data         = np.array(f.variables['reg'][:,0,:,:])
#跟据Missing Value确定where
data_mask    = np.ma.masked_where(data > 10**36, data)
prob         = np.array(f.variables['reg'][:,1,:,:])
prob_mask    = np.ma.masked_where(prob > 10**36, prob)
lats         = np.array(f.variables['lat'][:])
lons         = np.array(f.variables['lon'][:])

'''add cyclic point 
数据为经圈360度时，需要使数据闭环
from cartopy.util import add_cyclic_point
add_cyclic_point(data, coord=None, axis=-1)
returns cyclic_data, cyclic_coord'''
cyclic_data,cyclic_lons = add_cyclic_point(data_mask, coord=lons)
cyclic_prob = add_cyclic_point(prob_mask)

#==============================================================================

#绘制极地投影
def make_map(ax, projection, resolution, mapextent, xnum, ystep):
    ax.set_extent(mapextent, crs=projection)
    ax.coastlines(resolution, linewidth=0.5)
    '''添加边界圆环'''
    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)
    ax.set_boundary(circle, transform=ax.transAxes)
    '''标注坐标轴'''
    line = ax.gridlines(draw_labels=False)
    line.ylocator = mpl.ticker.FixedLocator(np.arange(mapextent[2], mapextent[3], ystep))#手动设置x轴刻度
    line.xlocator = mpl.ticker.FixedLocator(np.linspace(mapextent[0], mapextent[1], num=xnum, endpoint=True))#手动设置x轴刻度
    #创建要标注的labels字符串
    ticks=np.arange(0,210,30)
    etick=['0']+['%dE'%tick for tick in ticks if (tick !=0) & (tick!=180)]+['180']
    wtick=['%dW'%tick for tick in ticks if (tick !=0) & (tick!=180)]
    labels=etick+wtick
    #创建与labels对应的经纬度标注位置
    #xticks=[i for i in np.arange(0,210,30)]+[i for i in np.arange(-32,-180,-30)]
    xticks=[0.,30,60,90,120,150,180,-30,-60,-90,-120,-150]
    yticks=[mapextent[2]-7]*12 #7表示lable与图的距离（以经度为单位），可适当调整
    #标注经纬度    
    for xtick,ytick,label in zip(xticks,yticks,labels):
        ax.text(xtick,ytick,label, horizontalalignment='center', transform=ccrs.Geodetic())
    
    '''添加极点十字线'''
    x=[180, 180, 0, 0]
    y=[50, 90, 90, 50]
    ax.plot([-180,0],[80,80],':',transform=ccrs.Geodetic(),color='k',linewidth=0.4)
    ax.plot([-90,90],[80,80],':',transform=ccrs.Geodetic(),color='k',linewidth=0.5)
    #ax.plot([90,0],[50,50],'-.',transform=ccrs.Geodetic(),color='r',linewidth=6)

    return ax


#==============================================================================

#定义常量
projection = ccrs.PlateCarree()
resolution = '110m'
lonstart   = -180. 
lonstop    = 180.
latstart   = 20.
latstop    = 90.
mapextent  = [lonstart, lonstop, latstart, latstop]
xnum       = 13 #不要修改
ystep       = 20 #纬度间隔
nrows      = 2
ncols      = 1
siglevel   = np.array([-1.0, -0.95, 0.95, 1.0])
subtitles  = ['1)', '2)', '3)', '4)']
figtitle = 'SLP'
#==============================================================================

#设置colorbar
# Set the colormap and norm to correspond to the data for which the colorbar will be used
# 指定colorbar
cmap = mpl.cm.bwr
# 设定每个图的colormap和colorbar所表示范围是一样的，归一化
if abs(data.min()) >= data.max():
    levelmin = data.min()
else:
    levelmin = -data.max()
norm = mpl.colors.Normalize(vmin=levelmin, vmax=-levelmin)
# 设置levels
levels = mpl.ticker.MaxNLocator(nbin=16).tick_values(levelmin, -levelmin)

#==============================================================================

#创建图纸,以及两个子图
fig  = plt.figure(figsize=(6, 8))

axes = []

for i in range(nrows*ncols):
    '''创建ax'''
    ax = fig.add_subplot(nrows, ncols, i+1, projection=ccrs.NorthPolarStereo() )
    '''绘地图'''
    ax = make_map(ax, projection, resolution, mapextent, xnum, ystep)
    '''添加标题'''
    ax.set_title(subtitles[i], x=0.08, y=1.1)
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
#调整主图范围，给colorbar空间
fig.subplots_adjust(bottom=0.2, right=0.9, top=0.85, wspace=0.2,hspace=0.4)
#添加coloarbar
cax = fig.add_axes([0.35, 0.14, 0.3, 0.02])
cb  = fig.colorbar(p, cax=cax, orientation='horizontal')

#添加主标题

t = fig.text(0.5, 0.95, figtitle, horizontalalignment='center', fontproperties=FontProperties(size=16))
#保存图片
fig.savefig("./polar.eps")
