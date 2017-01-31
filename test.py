import numpy as np
import csv
import cartopy.crs as ccrs
import cartopy.feature
import matplotlib.pyplot as plt
from rotgrid import Rotgrid
from netCDF4 import Dataset as NetCDFFile
with open('pathTa_5000_jja_1__point.csv',"rb") as csvfile:
    csvreader = csv.reader(csvfile)
    Ta_final = np.array(list(csvreader),dtype=float)
plotting="TRUE"
if plotting == "TRUE":

    rp = ccrs.RotatedPole(pole_longitude=-162.0,
                          pole_latitude=39.25,
                          globe=ccrs.Globe(semimajor_axis=6370000,
                                           semiminor_axis=6370000))
    pc = ccrs.PlateCarree()
    ax = plt.axes(projection=rp)
    ax.coastlines('50m', linewidth=0.8)
    ax.add_feature(cartopy.feature.OCEAN,
                   edgecolor='black', zorder=0,facecolor='lightblue',
                   linewidth=0.00, alpha=1)
    ax.add_feature(cartopy.feature.LAND, zorder=0,facecolor='lightgray',
                   linewidth=0.00, alpha=1)

    #v = np.linspace(-6, 6, 21, endpoint=True)
    #cs = plt.contourf(lons_cclm, lats_cclm, FINAL, v, transform=ccrs.PlateCarree(), cmap=plt.cm.bwr)
    cmap = plt.cm.get_cmap('bwr', 21)

    #mapping = Rotgrid(-162.0, 39.25, 0, 0)
    #for ww in range(len(Ta_final[:,0])):
    #    (Ta_final[ww,0], Ta_final[ww,1]) = mapping.transform(Ta_final[ww,0], Ta_final[ww,1])
    #Ta_final[Ta_final[:,3]>.5]=float('nan')
    cs = plt.scatter(Ta_final[:,0],Ta_final[:,1],vmin=-6, vmax=6, marker = 'o',c=Ta_final[:,2], cmap=cmap, s = 50, alpha=0.7)
    cb = plt.colorbar(cs)

    #v = np.linspace(-6, 6, 21, endpoint=True)
    #cs = plt.contourf(lons_cclm, lats_cclm, FINAL, v, transform=ccrs.PlateCarree(), cmap=plt.cm.bwr)
    cmap = plt.cm.get_cmap('bwr', 21)

    plt.show()
