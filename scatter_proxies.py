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
# ===================================  Variables ========================================
ye = np.array([12000, 11000, 10000, 9000, 8000, 7000, 6000, 5000, 4000, 3000, 2000, 1000,  100]) # years in proxy Data
yr_bp=7
DIR = '/home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/Mauri_point_data/'
month='jja'
plotting ="TRUE"
year = ye[yr_bp]
OUT_DIR='path'
# =====================================   Functions    =======================================

def weighted_Arithmetic_Mean(Var, Ster):# https://en.wikipedia.org/wiki/Weighted_arithmetic_mean
    for i in range(len(Ster)):
        if Ster[i] == 0:
            Ster[i] +=100000000
    W = 1 / ((Ster) ** 2)
    #W = [float(i)/sum(W) for i in W]
    Mean_Var = sum(W[g] * Var[g] / sum(W) for g in range(len(W)))
    Vari_Var = 1 / sum((Ster[g]**-2) for g in range(len(Ster)))

    return Mean_Var, Vari_Var

file_name= DIR + 'tanom_' + month + '.csv'

def find_point(lon,Var):
    Var = np.array(Var)
    VAR_L = Var[Var[:,0]==lon]
    #VAR_Len = len(VAR_L[:,1])
    return VAR_L
    #return Var[np.logical_and(Var[:,0] == lon, Var[:,1] == lat)]

def find_time(time1,time2,Var):
    Var = np.array(Var)
    return Var[np.logical_and(Var[:,3] >= time1 , Var[:,3] <= time2)]

# =====================================  Main  ===========================================
with open(file_name,"rb") as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader) # Skip the first row!
    TA_var = np.array(list(csvreader),dtype=float)
TA_var[:,0]=np.round(TA_var[:,0],7)
TA_var[:,1]=np.round(TA_var[:,1],7)

#Lat = np.unique (np.round(TA_var[:,1],7))

#print len(Lat)
#print Lon[1]
for i in range(year,year+1000,1000):
    time1 = i-500
    time2 = i+500
    #print time1
    #print time2
    Ta = find_time(time1, time2, TA_var)
    Lon = np.unique(Ta[:, 0])
    #print len(Lon)
    #print Lon

    Ta_point = np.ones([len(Lon)*100,4])*-999.9
    #Ta_point = -999.0
    for j in range(len(Lon)):
        #print j
        #print m
        #print Lon[j],Ta
        #print find_point(Lon[j], Ta)
       # print Lon[j]
        TT = find_point(Lon[j],Ta)
        if len(TT)>0:

           # for k in range(len(TT[:,0])):

            Lat = np.unique(TT[:, 1])
            for g in range(len(Lat)):
                TTT = TT[TT[:,1] == Lat[g]]
                if len(TTT[:,1]) > 0:
                    tz= np.array(weighted_Arithmetic_Mean(TTT[:, 4], TTT[:, 5]))

                    Ta_point[j+g, 0] = TTT[0, 0]
                    Ta_point[j+g, 1] = TTT[0, 1]
                    Ta_point[j+g, 2] = tz[0]
                    Ta_point[j+g, 3] = tz[1]
                    #print len(TT[:,0])

        #print weighted_Arithmetic_Mean(TT[:,4], TT[:,5])
        #Ta_point[j,2:3] = np.array(weighted_Arithmetic_Mean(TT[:,4], TT[:,5]))
    Ta_final = Ta_point[Ta_point[:,0] != -999.9]
    fil_name = OUT_DIR + "Ta_" + str(i) + "_" + month + "_point.csv"
    np.savetxt(fil_name,Ta_final, delimiter=",")


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
                   edgecolor='black', zorder=0,facecolor='lightblue',
                   linewidth=0.00, alpha=1)
    ax.add_feature(cartopy.feature.LAND, zorder=0,facecolor='lightgray',
                   linewidth=0.00, alpha=1)

    #v = np.linspace(-6, 6, 21, endpoint=True)
    #cs = plt.contourf(lons_cclm, lats_cclm, FINAL, v, transform=ccrs.PlateCarree(), cmap=plt.cm.bwr)
    cmap = plt.cm.get_cmap('bwr', 21)

    mapping = Rotgrid(-162.0, 39.25, 0, 0)
    for ww in range(len(Ta_final[:,0])):
        (Ta_final[ww,0], Ta_final[ww,1]) = mapping.transform(Ta_final[ww,0], Ta_final[ww,1])
    Ta_final[Ta_final[:,3]>.5]=float('nan')
    cs = plt.scatter(Ta_final[:,0],Ta_final[:,1],vmin=-6, vmax=6, marker = 'o',c=Ta_final[:,2], cmap=cmap, s = 50, alpha=0.7)
    cb = plt.colorbar(cs)

    #v = np.linspace(-6, 6, 21, endpoint=True)
    #cs = plt.contourf(lons_cclm, lats_cclm, FINAL, v, transform=ccrs.PlateCarree(), cmap=plt.cm.bwr)
    cmap = plt.cm.get_cmap('bwr', 21)

    plt.show()



