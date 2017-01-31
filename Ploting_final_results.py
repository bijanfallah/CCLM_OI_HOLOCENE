'''
Program to plot the final results
after the assimilation is done!

'''
## TODO: it shoupd be adopted for the automatic coding
# =================================================== Importing  =======================================================
import matplotlib.pyplot as plt
from Read_CCLM import Plot_CCLM as pltcc
import os
import time
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature
import matplotlib.patches as patches
from rotgrid import Rotgrid
# ======================================================================================================================
# ==================================================== Namelist ========================================================
model_path   = '/scratch/users/fallah/CCLM_OI_HOLOCENE_DATA/Bijan'
path_to_FI   = '/scratch/users/fallah/HOLOCENE_RUN_3/optiminterp/inst/'
year = np.array([12000, 11000, 10000, 9000, 8000, 7000, 6000, 5000, 4000, 3000, 2000, 1000,  100])# years in proxy Data
yr_bp=7 # time slice of Holocene
pref_prox_val = 'EPOCH-2_new_1'
vari_cclm     = 'T_2M'
SEAS_cclm     = 'DJF'
vari_prox_val = 'tanom_' + SEAS_cclm.lower()
flag=1
#if vari_cclm == 'T_2M':
pref_cclm     = 'eu_merge_seas_mm_'
#else:
#    pref_cclm     = 'eu_merge_seas_mm_rr'

print os.getcwd()
print 'Ploting_final_results.py'
name1 = model_path + '/' +pref_cclm + vari_cclm+ '_' + SEAS_cclm + '_' + str(year[yr_bp]) + 'bp.nc'
name2 = model_path + '/' +pref_cclm + vari_cclm+ '_' + SEAS_cclm + '_' + '200bp.nc'
CMD = 'cdo sub ' + name1 + ' ' + '-timmean ' + name2 +' ./temp.nc'
os.system(CMD)
time.sleep(2)


name = 'RESULT_' + vari_cclm + '_' + SEAS_cclm + '_' + str(year[yr_bp]) + '.pdf'
# ======================================================================================================================

fig = plt.figure('1')
fig.set_size_inches(14, 10)

lons_cclm, lats_cclm, t_cclm ,shapes_cclm = pltcc(dir_mistral='./', prefix='temp', seas='', expr='',plus_min='TRUE',
                                                  var= vari_cclm, timming='TRUE', plotting='FALSE',
                                                  grid='FALSE',all_times ='TRUE')
pref = 'FI_' + str(year[yr_bp])
print pref
print path_to_FI
lons_fi, lats_fi, t_fi ,shapes_fi = pltcc(dir_mistral=path_to_FI , prefix= pref, seas='', expr='',
                                          plus_min='TRUE',var= 'FI', timming='TRUE', plotting='FALSE',
                                          grid='FALSE',all_times ='TRUE')
FINAL = np.median(t_cclm,axis=0).squeeze() + t_fi
print FINAL.shape
# ============================================= PLOTING BLOCK ==========================================================
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
               linewidth=0.1, alpha=.7)
#FINAL[FINAL>6]=6
#FINAL = np.ma.masked_where(np.logical_and(FINAL> - 0.5, FINAL < 0.5), FINAL)
#FINAL[np.logical_and(FINAL> - 0.5, FINAL < 0.5) ] = np.nan
v = np.linspace(-6, 6, 21, endpoint=True)
#cs = plt.contourf(lons_cclm, lats_cclm, FINAL, v, transform=ccrs.PlateCarree(), cmap=plt.cm.bwr)
cmap = plt.cm.get_cmap('bwr', 21)
#cmap.set_bad(color='lightgray',alpha=1)

cs = plt.pcolormesh(lons_cclm, lats_cclm, FINAL, transform=ccrs.PlateCarree(), cmap=cmap,vmin=-6, vmax=6)

cs.set_edgecolor('face')

ax.add_feature(cartopy.feature.OCEAN,
               edgecolor='black', zorder=1,facecolor='gray',
               linewidth=0.1, alpha=1)


# putting the patches for two regions
mapping = Rotgrid(-162.0, 39.25, 0, 0)
lon_box=np.zeros([1,2])
lat_box=np.zeros([1,2])
(lon_box[0,0], lat_box[0,0]) = mapping.transform(9,44.5)
(lon_box[0,1], lat_box[0,1]) = mapping.transform(17,44)
#
# for p in [
#     patches.Rectangle(
#         (lon_box[0,0],lat_box[0,0]), 5, 3,
#         hatch='/',
#         fill=False
#     ),
#     patches.Rectangle(
#         (lon_box[0,1],lat_box[0,1]), 5, 3,
#         hatch='\\',
#         fill=False
#     ),
# ]:
#     ax.add_patch(p)
# END putting the patches for two regions
cb = plt.colorbar(cs)

cb.set_label(vari_cclm, fontsize=20)
cb.ax.tick_params(labelsize=20)
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
        fontsize=5, color='black')

xs, ys, zs = rp.transform_points(pc,
                                 np.array([-14, 96.0]),
                                 np.array([13, 64])).T
import csv
import numpy as np
from rotgrid import Rotgrid
name3 = '/home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/'
fil_name = name3 + "Ta_" + str(year[yr_bp]) + "_" + SEAS_cclm.lower() + "_" + str(flag) + "_" + "_point.csv"
name3 = np.array(list(csv.reader(open(fil_name, "rb"), delimiter=','))).astype('float')
plt.scatter(name3[:,0], name3[:,1], marker='o', c='green', s=25, zorder=10, lw=0, alpha=.7)
ax.text(-27.83, -24.50, str(len(name3[:,1])),
        fontsize=25, color='green')
ax.set_xlim(xs)
ax.set_ylim(ys)
plt.savefig(name)
plt.close()
#plt.show()
# ======================================================================================================================
print os.getcwd()
print 'Ploting_final_results.py'

