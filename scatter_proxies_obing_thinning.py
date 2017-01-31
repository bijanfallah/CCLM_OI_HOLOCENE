'''
Program to make millennial means from timely scattered Proxies of Mauri et al.

'''
# =================================== importing  ========================================
import numpy as np
import csv
import cartopy.crs as ccrs
import cartopy.feature
import matplotlib.pyplot as plt
from rotgrid import Rotgrid
from netCDF4 import Dataset as NetCDFFile

# ===================================  Variables ========================================
ye = np.array([12000, 11000, 10000, 9000, 8000, 7000, 6000, 5000, 4000, 3000, 2000, 1000, 100])  # years in proxy Data
yr_bp=7
DIR = '/home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/Mauri_point_data/'
month = 'jja'
plotting = "FALSE"
year = ye[yr_bp]
OUT_DIR = 'path'
flag=1  # data thinning


# flag=2 #super-obing
# =====================================   Functions    =======================================
# TODO: -----correction here:---
def weighted_Arithmetic_Mean(Var, Ster):  # https://en.wikipedia.org/wiki/Weighted_arithmetic_mean
    for i in range(len(Ster)):
        if Ster[i] == 0:
            Ster[i] += 10000
    #     if dist[i] == 0:
    #         dist[i] += 1

    #dist = [float(i) / sum(dist) for i in dist]
    # Ster = dist * Ster
    # Var = dist * Var
    W = 1 / (Ster ** 2)

    # W = [float(i)/sum(W) for i in W]
    Mean_Var = sum(W[g] * Var[g] / sum(W) for g in range(len(W)))
    Vari_Var = 1 / sum((Ster[g] ** -2) for g in range(len(Ster)))

    return Mean_Var, Vari_Var


def obs_grid_correcting(flag=1, VAR_PROXY=0):
    '''
    This function will do the observation data correction for each grid of the model.
    There may be grid cells with more than one observation inside.
    :param flag: =1  data thinning and =2 super-obing
    :return: the list of observations and their locations
    '''
    name = '/scratch/users/fallah/CCLM_OI_HOLOCENE_DATA/Bijan/lffd7465122412.nc'  # read the rlat and rlon from cclm netcdf file
    nc = NetCDFFile(name)
    rlats = nc.variables['rlat'][9:118]
    rlons = nc.variables['rlon'][9:121]
    # xv, yv = np.meshgrid(rlons, rlats, sparse=False, indexing='ij')
    # leng = rlons.__len__() * rlats.__len__()
    # lons = xv.reshape(leng, 1)
    # lats = yv.reshape(leng, 1)
    iii = 0
    mapping = Rotgrid(-162.0, 39.25, 0, 0)

    for ww in range(len(VAR_PROXY[:, 0])):
        (VAR_PROXY[ww, 0], VAR_PROXY[ww, 1]) = mapping.transform(VAR_PROXY[ww, 0], VAR_PROXY[ww, 1])

    VAR_PROXY_NE = np.ones([len(VAR_PROXY[:, 0]), 4]) * -999.9
    va = np.zeros([1, 2])
    for grd_x in range(len(rlons) - 1):

        for grd_y in range(len(rlats) - 1):
            Targ = VAR_PROXY[np.logical_and(VAR_PROXY[:, 0] >= rlons[grd_x], VAR_PROXY[:, 0] <= rlons[grd_x + 1])]
            Targ = Targ[np.logical_and(Targ[:, 1] >= rlats[grd_y], Targ[:, 1] <= rlats[grd_y + 1])]
            if len(Targ) >= 1:
                if flag == 1:
                    #print 'Targ is ', Targ
                    err_min = min(Targ[:, 3])
                    dumm = Targ[Targ[:, 3] == err_min]
                    print dumm
                    VAR_PROXY_NE[iii, 0] = np.mean(dumm[:, 0])
                    VAR_PROXY_NE[iii, 1] = np.mean(dumm[:, 1])
                    VAR_PROXY_NE[iii, 2] = np.mean(dumm[:, 2])
                    VAR_PROXY_NE[iii, 3] = np.mean(dumm[:, 3])

                    iii = iii + 1
                else:
                    if flag == 2:
                        va[0:1] = 0
                        va[0:1] = weighted_Arithmetic_Mean(Targ[:, 2], Targ[:, 3])
                        VAR_PROXY_NE[iii, 0] = np.mean(Targ[:, 0])
                        VAR_PROXY_NE[iii, 1] = np.mean(Targ[:, 1])
                        VAR_PROXY_NE[iii, 2] = va[0][0]
                        VAR_PROXY_NE[iii, 3] = va[0][1]
                        iii = iii + 1
    VAR_PROXY_NEW = VAR_PROXY_NE[VAR_PROXY_NE[:, 0] != -999.9]

    return VAR_PROXY_NEW


file_name = DIR + 'tanom_' + month + '.csv'


def find_point(lon, Var):
    Var = np.array(Var)
    VAR_L = Var[Var[:, 0] == lon]
    # VAR_Len = len(VAR_L[:,1])
    return VAR_L
    # return Var[np.logical_and(Var[:,0] == lon, Var[:,1] == lat)]


def find_time(time1, time2, Var):
    Var = np.array(Var)
    return Var[np.logical_and(Var[:, 3] >= time1, Var[:, 3] <= time2)]


# =====================================  Main  ===========================================
with open(file_name, "rb") as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the first row!
    TA_var = np.array(list(csvreader), dtype=float)
TA_var[:, 0] = np.round(TA_var[:, 0], 7)
TA_var[:, 1] = np.round(TA_var[:, 1], 7)

# Lat = np.unique (np.round(TA_var[:,1],7))

# print len(Lat)
# print Lon[1]
for i in range(year, year + 1000, 1000):
    time1 = i - 250
    time2 = i + 250
    # print time1
    # print time2
    Ta = find_time(time1, time2, TA_var)
    Lon = np.unique(Ta[:, 0])
    print len(Lon)
    # print Lon

    Ta_point = np.ones([len(Lon) * 500, 5]) * -999.9
    # Ta_point = -999.0
    for j in range(len(Lon)):
        # print j
        # print m
        # print Lon[j],Ta
        # print find_point(Lon[j], Ta)
        # print Lon[j]
        TT = find_point(Lon[j], Ta)
        if len(TT) > 0:

            # for k in range(len(TT[:,0])):

            Lat = np.unique(TT[:, 1])
            for g in range(len(Lat)):
                TTT = TT[TT[:, 1] == Lat[g]]
                if len(TTT[:, 1]) > 0:
                    tz = np.array(weighted_Arithmetic_Mean(TTT[:, 4], TTT[:, 5]))

                    Ta_point[j + g, 0] = TTT[0, 0]
                    Ta_point[j + g, 1] = TTT[0, 1]
                    Ta_point[j + g, 2] = tz[0]
                    Ta_point[j + g, 3] = tz[1]

                    # print len(TT[:,0])

                    # print weighted_Arithmetic_Mean(TT[:,4], TT[:,5])
                    # Ta_point[j,2:3] = np.array(weighted_Arithmetic_Mean(TT[:,4], TT[:,5]))
    Ta_fin = Ta_point[Ta_point[:, 0] != -999.9]
    Ta_final = obs_grid_correcting(flag=flag, VAR_PROXY=Ta_fin)
    fil_name = OUT_DIR + "Ta_" + str(i) + "_" + month + "_" + str(flag) + "_" + "_point.csv"
    np.savetxt(fil_name, Ta_final, delimiter=",")

# Now Data-thinning or the Super-obing: _______________________________________________


# _____________________________________________________________________________________

# some plotting here: _________________________________________________________________
if plotting == "TRUE":
    rp = ccrs.RotatedPole(pole_longitude=-162.0,
                          pole_latitude=39.25,
                          globe=ccrs.Globe(semimajor_axis=6370000,
                                           semiminor_axis=6370000))
    pc = ccrs.PlateCarree()
    ax = plt.axes(projection=rp)
    ax.coastlines('50m', linewidth=0.8)
    ax.add_feature(cartopy.feature.OCEAN,
                   edgecolor='black', zorder=0, facecolor='lightblue',
                   linewidth=0.00, alpha=1)
    ax.add_feature(cartopy.feature.LAND, zorder=0, facecolor='lightgray',
                   linewidth=0.00, alpha=1)

    # v = np.linspace(-6, 6, 21, endpoint=True)
    # cs = plt.contourf(lons_cclm, lats_cclm, FINAL, v, transform=ccrs.PlateCarree(), cmap=plt.cm.bwr)
    cmap = plt.cm.get_cmap('bwr', 21)

    # mapping = Rotgrid(-162.0, 39.25, 0, 0)
    # for ww in range(len(Ta_final[:,0])):
    #    (Ta_final[ww,0], Ta_final[ww,1]) = mapping.transform(Ta_final[ww,0], Ta_final[ww,1])
    # Ta_final[Ta_final[:,3]>.5]=float('nan')
    cs = plt.scatter(Ta_final[:, 0], Ta_final[:, 1], vmin=-6, vmax=6, marker='o', c=Ta_final[:, 2], cmap=cmap, s=50,
                     alpha=0.7)
    cb = plt.colorbar(cs)

    # v = np.linspace(-6, 6, 21, endpoint=True)
    # cs = plt.contourf(lons_cclm, lats_cclm, FINAL, v, transform=ccrs.PlateCarree(), cmap=plt.cm.bwr)
    cmap = plt.cm.get_cmap('bwr', 21)

    plt.show()
