#==============================================================================

#JOJO, IAP, Beiing, Email:mtjsummer@163.com
#2018-02-07

#练习6目标：
#  1.绘制矢量图
#  2.调整vector大小，密度
#  3.绘制矢量图例
#  4.叠加显著性检验

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
level = 2

uwnd      = np.array(fu.variables['uwnd'][0,level,:,:])
vwnd      = np.array(fv.variables['vwnd'][0,level,:,:])
lats      = np.array(fu.variables['lat'][:])
lons      = np.array(fu.variables['lon'][:])
levels    = np.array(fu.variables['level'][:])
#print(uwnd.max())

#mask较小的vector
speed = np.sqrt(np.square(uwnd)+np.square(vwnd))
threshold = 3.0
u_mask = np.ma.masked_where(speed < threshold, uwnd)
v_mask = np.ma.masked_where(speed < threshold, vwnd)

#计算显著性检验
prob = np.fmax(np.absolute(uwnd), np.absolute(vwnd))
prob = prob/np.std(prob)
#print(prob.shape, prob.min(), prob.max())
#==============================================================================

#函数形式，调用cartopy，绘制全球地图
def make_map(ax, projection, resolution, box, xnum, ynum):
    
    ax.set_extent(box,crs=projection)
    ax.coastlines(linewidth=0.5)
    '''标注坐标轴'''
    ax.set_xticks(np.linspace(box[0], box[1], xnum, endpoint=True), crs=projection) 
    ax.set_yticks(np.linspace(box[2], box[3], ynum, endpoint=True), crs=projection)
    '''zero_direction_label=True 有度的标识，False则去掉'''
    lon_formatter = LongitudeFormatter(zero_direction_label=True) 
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    '''添加网格线'''
    #gl = ax.gridlines()
    #ax.grid()
    return ax

#==============================================================================

# 设置常量
projection = ccrs.PlateCarree()
resolution = '110m'
lonstart   = 60
lonstop    = 300
latstart   = 0
latstop    = 90
box        = np.array([lonstart, lonstop, latstart, latstop])
# x，y轴标签个数
xnum       = 5
ynum       = 4
#
nrows      = 2
ncols      = 1
# prob_level
levels_prob = [0., 0.5, 0.95]
subtitles = ['a','b']
#==============================================================================

# 开始绘图
# 创建图纸,以及两个子图
fig = plt.figure(figsize=(8,6))
axes = []
# quiver位置参数
X, Y = np.meshgrid(lons[::3], lats[::3])


for i in range(nrows*ncols):
    ax = fig.add_subplot(nrows, ncols, i+1, projection=ccrs.PlateCarree(central_longitude=180))
    # 在ax上画地图
    ax = make_map(ax, projection, resolution, box, xnum, ynum)
    # 显著性
    # p = ax.contourf(lons, lats, prob, levels_prob, colors=('g', 'r'), transform=projection)
    # 绘制矢量 
    '''units=inches 指定箭头尺寸单位，inches调整坐标轴长宽不影响箭头大小；width调整坐标轴宽度时，箭头大小也随之变化'''
    '''scale=50., Number of data units per arrow length unit. eg.scale=30. 每英寸代表30m/s的风速大小'''
    '''scale_units= ; 如果不指定scale，则由scale——units指定箭头长度'''
    '''width控制箭杆宽度(shaft width in arrow units)，通常从0.005开始'''
    '''headwidth控制箭头宽度，以箭杆宽度为标准，默认值为箭杆宽度的三倍'''
    '''headlength控制箭头长度，以箭杆宽度为标准，默认值为箭杆宽度的5倍'''
    '''minshaft 长度低于scale的值的箭头，尖端长度设置为，默认值1'''
    '''minlength 长度低于该值（箭杆宽度为标准），的箭头不被绘制，只绘制一个点'''
    q  = ax.quiver(X, Y, u_mask[::3,::3], v_mask[::3,::3], units='inches', 
        scale=25., width=0.02, color='b')
    ax.set_title(subtitles[i], loc='left')
    # 绘制矢量图例
    qk = ax.quiverkey(q, 0.9, 1.05, 10, '10 m/s', labelpos='N', color='r')
    # ax 传递给axes
    axes.append(ax)
#==============================================================================
#调整布局
fig.subplots_adjust(left=None, bottom=None, right=None, top=0.9, hspace=0.3, wspace=None)
# 添加主标题
figtitle = 'Vector plot'
t = fig.text(0.5, 0.95, figtitle, horizontalalignment='center')

# 保存图片
# adjust spacing between subplots so ax and ax1 title and ticks labels don't overlay
#plt.show()
fig.savefig('./fig/quiver.pdf')
