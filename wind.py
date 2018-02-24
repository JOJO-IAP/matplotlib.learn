#==============================================================================

#JOJO, IAP, Beiing, Email:mtjsummer@163.com

#==============================================================================

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.font_manager import FontProperties

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

from netCDF4 import Dataset 
import numpy as np

#==============================================================================

# 读入数据
fu = Dataset('uwnd850.nc')
fv = Dataset('vwnd850.nc')
# print(f)
'''levels= [ 1000.   925.   850.   700.   600.   500.   400.   300.   250.   850.
   150.   100.    70.    50.    30.    20.    10.]'''
missing_value = -10**36

uwnd      = np.array(fu.variables['reg'][:,0,:,:])
uwnd_mask = np.ma.masked_where(uwnd < missing_value, uwnd)
uprob     = np.array(fu.variables['reg'][:,1,:,:])
uprob_mask = np.ma.masked_where(uprob < missing_value, uprob)

vwnd      = np.array(fv.variables['reg'][:,0,:,:])
vwnd_mask = np.ma.masked_where(vwnd < missing_value, vwnd)
vprob     = np.array(fu.variables['reg'][:,1,:,:])
vprob_mask = np.ma.masked_where(vprob < missing_value, uprob)

lats      = np.array(fu.variables['lat'][:])
lons      = np.array(fu.variables['lon'][:])

#mask较小的vector
speed = np.sqrt(np.square(uwnd_mask)+np.square(vwnd_mask))
threshold = 0.2
u_mask = np.ma.masked_where(speed < threshold, uwnd_mask)
v_mask = np.ma.masked_where(speed < threshold, vwnd_mask)

#计算显著性检验
prob = np.fmax(np.absolute(uprob_mask), np.absolute(vprob_mask))

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
lonstop    = 360
latstart   = -30
latstop    = 90
box        = np.array([lonstart, lonstop, latstart, latstop])
# x，y轴标签个数
xnum       = 6
ynum       = 5 
#
nrows      = 2
ncols      = 1
# prob_level
levels_prob = [0., 0.95, 1.0]
subtitles = ['a) EAWIM','b) EAWMIres']
figtitle = 'Reg_wind 850hPa'

#quiver 参数设置
scl = 3.
#quiverkey 参数设置
U = 1
Ulabel = '1 m/s'
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
    q  = ax.quiver(X, Y, u_mask[i,::3,::3], v_mask[i,::3,::3], units='inches', scale=scl, width=0.015, color='b',transform=projection)
    ax.set_title(subtitles[i], loc='left')
    # 绘制矢量图例
    qk = ax.quiverkey(q, 0.9, 1.05, U, Ulabel, labelpos='N', color='r')
    # ax 传递给axes
    axes.append(ax)
#==============================================================================
#调整布局
fig.subplots_adjust(left=None, bottom=None, right=None, top=0.9, hspace=0.3, wspace=None)
# 添加主标题
t = fig.text(0.5, 0.95, figtitle, horizontalalignment='center', fontproperties=FontProperties(size=16))

# 保存图片
# adjust spacing between subplots so ax and ax1 title and ticks labels don't overlay
#plt.show()
fig.savefig('../fig/reg.wind850.eps')
