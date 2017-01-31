'''
Program to read the CLM data
and start analysis



'''
import os
from netCDF4 import Dataset as NetCDFFile
import numpy as np
import matplotlib.pyplot as plt

#if not os.path.exists('TEMP'):
#    os.makedirs('TEMP')
#os.chdir('TEMP')
def nanargmax(a):
    idx = np.argmax(a, axis=None)
    multi_idx = np.unravel_index(idx, a.shape)
    if np.isnan(a[multi_idx]):
        nan_count = np.sum(np.isnan(a))
        idx = np.argpartition(a, -nan_count-1, axis=None)[-nan_count-1]
        multi_idx = np.unravel_index(idx, a.shape)
    return multi_idx
def nanargmin(a):
    idx = np.argmin(a, axis=None)
    multi_idx = np.unravel_index(idx, a.shape)
    if np.isnan(a[multi_idx]):
        nan_count = np.sum(np.isnan(a))
        idx = np.argpartition(a, -nan_count-1, axis=None)[-nan_count-1]
        multi_idx = np.unravel_index(idx, a.shape)
    return multi_idx
def Plot_CCLM(dir_mistral='/scratch/users/fallah/CCLM_OI_HOLOCENE_DATA/Bijan',prefix='anom',seas='JJA', expr='200bp',
              var='T_2M',flag='TRUE',color_map='TRUE', plus_min='TRUE', plotting='TRUE', timming='TRUE', time= '1', grid='TRUE',
              all_times ='FALSE'):
    import cartopy.crs as ccrs
    import cartopy.feature
    if seas and expr:
        name = dir_mistral + '/' + prefix + '_' + seas + '_' + expr +'.nc'
    else:
        name = dir_mistral + '/' + prefix + '.nc'
    print name
    print name
    print name

    nc = NetCDFFile(name)
    #os.remove(name)
    #lats_1 = nc.variables['lat'][:]
    #lons_1 = nc.variables['lon'][:]
    lats = nc.variables['lat'][:]
    lons = nc.variables['lon'][:]
    if len(lats.shape) == 1:
        lons, lats = np.meshgrid(lons,lats)
        print "lon and lat have been meshgridded"
    shapes = nc.variables[var][:].shape
    if timming == "TRUE":
        if all_times == "TRUE":
            t = nc.variables[var][:].squeeze()
        else:
            t = nc.variables[var][time,:,:].squeeze()

    else:
        t = nc.variables[var][:,:].squeeze()
    nc.close()
    if plotting == 'TRUE':

        rp = ccrs.RotatedPole(pole_longitude=-162.0,
                              pole_latitude=39.25,
                              globe=ccrs.Globe(semimajor_axis=6370000,
                                               semiminor_axis=6370000))
        pc = ccrs.PlateCarree()
        ax = plt.axes(projection=rp)
        ax.coastlines('50m', linewidth=0.8)
        ax.add_feature(cartopy.feature.OCEAN,
                       edgecolor='black', zorder=0,facecolor='lightgray',
                       linewidth=0.8, alpha=.7)
        ax.add_feature(cartopy.feature.LAND, zorder=0,facecolor='lightgray',
                       linewidth=0.8, alpha=.7)
        if flag=='TRUE':
            if plus_min=='TRUE':
                v = np.linspace(-6, 6, 21, endpoint=True)
                cs = plt.contourf(lons, lats, t, v, transform=ccrs.PlateCarree(), cmap=plt.cm.bwr)
                #cs = plt.pcolormesh(lons, lats, t, transform=ccrs.PlateCarree(), cmap=plt.cm.bwr,vmin=-6, vmax=6)
                #cs.set_edgecolor('face')
            else:
                v = np.linspace(np.nanmin(t),np.nanmax(t) , 21, endpoint=True)
                cs = plt.contourf(lons, lats, t, v, transform=ccrs.PlateCarree(), cmap=plt.cm.BuGn)
                #cs = plt.pcolormesh(lons, lats, t, transform=ccrs.PlateCarree(), cmap=plt.cm.BuGn,vmin=-6, vmax=6)
                #cs.set_edgecolor('face')
            if color_map=='TRUE':
                cb = plt.colorbar(cs)
                cb.set_label(var, fontsize=20)
                cb.ax.tick_params(labelsize=20)
        idx=np.where(t > -900)
        if grid=='TRUE':
          #  name_lffd     = '/scratch/users/fallah/CCLM_OI_HOLOCENE_DATA/Bijan/lffd7465122412.nc'
          #  nc = NetCDFFile(name_lffd)
          #  rlons = nc.variables['rlon'][9:121]
          #  LO = lons[idx]
          #  LA = lats[idx]
          #  points_in_indx=np.where(LO < max(rlons[:])) # use the observatins within the CCLM domain
            plt.scatter(lons[idx], lats[idx], marker='.', transform=ccrs.PlateCarree(), c='gray', s=10, zorder=10)
          #  plt.scatter(LO[points_in_indx], LA[points_in_indx], marker='.', transform=ccrs.PlateCarree(), c='red', s=20, zorder=10)
        ax.gridlines()
        ax.text(-41.14, 4.24, r'$45\degree N$',
                fontsize=15)
        ax.text(-41.14, -10.73, r'$30\degree N$',
                fontsize=15)
        ax.text(-19.83, -32.69, r'$0\degree $',
                fontsize=15)
        ax.text(0.106, -32.69, r'$20\degree E$',
                fontsize=15)
        ax.text(23.106, -32.69, r'$40\degree E$',
                fontsize=15)
        ax.text(-35.83, -27.69, r'$info@Bijan-Fallah.com$',
                fontsize=5, color='green')

        xs, ys, zs = rp.transform_points(pc,
                                         np.array([-14, 96.0]),
                                         np.array([13, 64])).T
        ax.set_xlim(xs)
        ax.set_ylim(ys)


    else:

        return lons, lats, t, shapes



