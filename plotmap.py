#==============================================================================

#JOJO, IAP, Beiing, Email:mtjsummer@163.com
#2018-02-09
' plot cartopy map module '
__author__ = 'JOJO'
#==============================================================================

import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.util import add_cyclic_point
from netCDF4 import Dataset 
import numpy as np
#==============================================================================

#绘制区域地图函数
def make_map(ax, projection, resolution, mapextent, xnum, ynum):
    ax.set_extent(mapextent, crs=projection)
    ax.coastlines(resolution, linewidth=0.5)
    '''标注坐标轴 注意lon的取值范围为-180:180；lat取值范围为-90：90'''
    '''设置坐标轴刻度'''
    ax.set_xticks(np.linspace(mapextent[0], mapextent[1], num=xnum, endpoint=True), crs=projection)
    ax.set_yticks(np.linspace(mapextent[2], mapextent[3], num=ynum, endpoint=True), crs=projection)
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    return ax

'''注意画经圈360的设置：projection=ccrs.PlateCarree(central_longitude=180),
lonstart=60, lonstop=360(即代表0E), xnum=6'''
if __name__=='__main__':
    make_map()
#==============================================================================
