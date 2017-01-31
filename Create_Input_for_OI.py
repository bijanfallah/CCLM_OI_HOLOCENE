'''
Program to create the Input file for the Optimal Interpolation code
Step 1 :  create the f (difference between background and the observation):
d=y^o - Hx^b
Step 2 : calculate the error variance of the observations divided by the
error variance of the background field
Created by Bijan fallah
info@bijan-fallah.com
'''
# ============================================== Importing the packages ================================================
import pandas as pd
import numpy as np
import os
import csv
from itertools import izip
from netCDF4 import Dataset as NetCDFFile

def to_number(s):
    if "]" in s:
        try:
            s1 = s.replace("]", "")
            s1 = s1.replace("[", "")
            s1 = np.float(s1)
            return s1
        except ValueError:
            return s

def f1(x):
    return to_number(x)
f2 = np.vectorize(f1)
#f2 = f1
# ======================================================================================================================

# ================================================== Namelist variables ================================================
yr_bp=6
OBS_path = '/home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/TEMP/'
vari = 'T_2M'
SEAS= 'DJF'
pref = 'eu_merge_seas_mm_'
# ======================================================================================================================

# ====================================================Step 1 ===========================================================

# ----------- OBS------------------------------>
year        = np.array([12000, 11000, 10000, 9000, 8000, 7000, 6000, 5000, 4000, 3000, 2000, 1000,  100]) # years in proxy Data
name        = OBS_path + 'Stations_' + str(year[yr_bp]) + '.csv'
Obs         = pd.read_csv(name)
Obs.columns =   ['lon','lat','Vals','Variance']

# ---------- FG-------------------------------->
name        = OBS_path + 'First_Guess_DATA_' + vari + '_'+ SEAS + '_'+ str(year[yr_bp]) + '.csv'
FG          = pd.read_csv(name)
FG.columns  = ['lon','lat','Vals','Variance']
#Obs.Vals = f2(Obs.Vals)
#Obs.Variance = f2(Obs.Variance)

f = FG
f.Vals = Obs.Vals - FG.Vals
f.lon = Obs.lon
f.lat = Obs.lat
# ======================================================================================================================
# ====================================================== step 2 ========================================================
Vari = Obs.Variance/FG.Variance

# ======================================================================================================================
# ================================================== Write INPUT file ==================================================
name = OBS_path +'INPUT_'+ str(year[yr_bp]) + '.csv'
print
print name
print name
print name
print
with open(name, 'wb') as ff:
    writer = csv.writer(ff)
    writer.writerows(izip(f.lon,f.lat,f.Vals,list(Vari)))

# ======================================================================================================================
# ======================================= Writing the coordinates of the model grids ===================================
name='/scratch/users/fallah/CCLM_OI_HOLOCENE_DATA/Bijan/lffd7465122412.nc' # read the rlat and rlon from cclm netcdf file
nc = NetCDFFile(name)
rlats = nc.variables['rlat'][9:118]
rlons = nc.variables['rlon'][9:121]
xv, yv = np.meshgrid(rlons, rlats, sparse=False, indexing='ij')
np.savetxt('/home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/TEMP/LON.out', xv, delimiter=',')
np.savetxt('/home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/TEMP/LAT.out', yv, delimiter=',')
leng=rlons.__len__()*rlats.__len__()
lons=xv.reshape(leng,1)
lats=yv.reshape(leng,1)
print
print OBS_path
print OBS_path


with open(OBS_path + 'GRIDS.csv', 'wb') as gr:
    writer = csv.writer(gr)
    for i in range(0,leng):
        writer.writerows(izip(lons[i],lats[i]))
print 'ALL FILES CREATED SUCCESSFULLY'
print os.getcwd()
print os.getcwd()
print
# ======================================================================================================================

print os.getcwd()
print 'Create_Input_for_OI.py'
