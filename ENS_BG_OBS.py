'''
Program to create Background - OBS values
and the variances
save the out for OI input
make the ensemble from each time-slice simulation
'''
# ==================================================  importing ========================================================
from scipy.interpolate import RegularGridInterpolator as RegInt
import os
import numpy as np
from Read_CCLM import Plot_CCLM as pltcc
from rotgrid import Rotgrid
from itertools import izip
import time
import csv
from netCDF4 import Dataset as NetCDFFile
def f(x):
    return np.float(x)
f2 = np.vectorize(f)
# ======================================================================================================================
proxy_gridded = "FALSE" # if TRUE it reads the gridded netcdf file, else, it reads the scatter files (using the programm:
# scatter_proxies.py )
year = np.array([12000, 11000, 10000, 9000, 8000, 7000, 6000, 5000, 4000, 3000, 2000, 1000,  100])# years in proxy Data
model_path = '/scratch/users/fallah/CCLM_OI_HOLOCENE_DATA/Bijan'
#model_path='/home/bijan/Documents/DATA/Bijan'
path_to_proxy="/scratch/users/fallah/trash/EPOCH-2_Mauri_etal_QSR"

yr_bp=6 # time slice of Holocene
scratch       = "/scratch/users/fallah/trash"
path_to_proxy_scattered = 'path_to_prox_scatter'
name_lffd     = '/scratch/users/fallah/CCLM_OI_HOLOCENE_DATA/Bijan/lffd7465122412.nc'# read the rlat and rlon
                                                                                     # from cclm netcdf file
pref_prox_val = 'EPOCH-2_new_1'
vari_prox_val = 'tanom_djf'
pref_prox_un = 'EPOCH-2_uncertainties_new_1'
vari_prox_un = 'tanom_djf_se'
vari_cclm     = 'T_2M'
SEAS_cclm     = 'DJF'
#if vari_cclm == 'T_2M':
pref_cclm     = 'eu_merge_seas_mm_'
#else:
#    pref_cclm     = 'eu_merge_seas_mm_rr'

# ================================================ Read observation ====================================================
if not os.path.exists(path_to_proxy):# Check if the Proxy files exist
    print("file exists")
    wrk=os.getcwd()
    os.chdir(scratch)
    os.system("curl -sS  http://arve.unil.ch/pub/EPOCH-2_Mauri_etal_QSR.tar.gz> file.gz")
    os.system("tar -zxvf file.gz")
    os.system("rm file.gz")
# ---------------- read the proxy value------------------------
if proxy_gridded == "TRUE":

    lons_obs, lats_obs, t_obs , bef= pltcc(dir_mistral=path_to_proxy, prefix=pref_prox_val, seas='', expr='',
                                           plus_min='TRUE', var= vari_prox_val, timming='TRUE',plotting='FALSE',flag='FALSE',
                                           time=yr_bp, grid='TRUE')
    mapping = Rotgrid(-162.0, 39.25, 0, 0)
    #-------------read the corresponding uncertainty file----------
    lons_obs_un, lats_obs_un, t_obs_un , bef = pltcc(dir_mistral=path_to_proxy, prefix=pref_prox_un, seas='',
                                                     expr='', plus_min='TRUE', var= vari_prox_un, timming='TRUE',
                                                     plotting='FALSE',flag='FALSE',time=yr_bp, grid='TRUE')
    # -------------reshaping-----------------------------------------
    idx = np.where(t_obs > -900)  # capture the values without NaN
    s = lats_obs[idx]
    m = s.shape
    len = m[0]
    lons_obs_reshape = lons_obs[idx].reshape(len, 1)
    lats_obs_reshape = lats_obs[idx].reshape(len, 1)
    t_obs_reshape = t_obs[idx].reshape(len, 1)
    t_obs_un_reshape = t_obs_un[idx].reshape(len, 1)
    lats_obs_reshape_rot = lats_obs_reshape - lats_obs_reshape
    lons_obs_reshape_rot = lons_obs_reshape - lons_obs_reshape
    mapping = Rotgrid(-162.0, 39.25, 0, 0)
    for i in range(0, len):
        (lons_obs_reshape_rot[i], lats_obs_reshape_rot[i]) = mapping.transform(lons_obs_reshape[i], lats_obs_reshape[i])

        # ======================================================================================================================

else:
    file_name = path_to_proxy_scattered + 'Ta_' + str(year[yr_bp]) + "_" + SEAS_cclm.lower() + "_" + str(999999) + "_" + '_point.csv'
    with open(file_name, "rb") as csvfile:
        csvreader = csv.reader(csvfile)
        TA = np.array(list(csvreader), dtype=float)
    lons_obs_reshape_rot = TA[:,0]
    lats_obs_reshape_rot = TA[:,1]
    t_obs_reshape    = TA[:,2]
    t_obs_un_reshape = TA[:,3]


# ========================================== Write First Guess from CCLM ===============================================
# =========================================== Read the CCLM time-slice =================================================
name1 = model_path + '/' +pref_cclm + vari_cclm+ '_' + SEAS_cclm + '_' + str(year[yr_bp]) + 'bp.nc'
name2 = model_path + '/' +pref_cclm + vari_cclm+ '_' + SEAS_cclm + '_' + '200bp.nc'


CMD = 'cdo sub ' + name1 + ' ' + '-timmean ' + name2 +' ./temp.nc'
os.system(CMD)
time.sleep(2)                                                                                                      # +
lons_cclm, lats_cclm, t_cclm ,shapes = pltcc(dir_mistral='./', prefix='temp', seas='', expr='',
                                              plus_min='TRUE',var= vari_cclm, timming='TRUE', plotting='FALSE',
                                              grid='FALSE',all_times ='TRUE')

nums = shapes[0]
z=range(0,nums)
nc = NetCDFFile(name_lffd)
rlats = nc.variables['rlat'][9:118]
rlons = nc.variables['rlon'][9:121]
my_interpolating_function = RegInt((z,rlats, rlons), t_cclm, method='nearest')
NN = lons_obs_reshape_rot.shape[0]
points=np.zeros((NN,3))
points[:, 2] = lons_obs_reshape_rot.squeeze()
points[:, 1] = lats_obs_reshape_rot.squeeze()
points_in_indx=np.where(points[:,2] < max(rlons[:])) # use the observatins within the CCLM domain
points_in = points[points_in_indx]

# ================================ Writing the Observation and its uncertainty in a csv file ===========================
import csv
name = '/home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/TEMP/Stations_' + str(year[yr_bp]) + '.csv'
with open(name, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(izip(f2(points_in[:, 2]),f2(points_in[:, 1]),
                          t_obs_reshape[points_in_indx],t_obs_un_reshape[points_in_indx]))
# ======================================================================================================================

NN = points_in.shape[0]
Interp_Vals=np.zeros((NN,z.__len__()))

for i in z:
        points_in[:, 0] = np.zeros(NN)+i
        Interp_Vals[:,i] = my_interpolating_function(points_in)                        # interpolate model on observations

Interp_Vals = np.concatenate((Interp_Vals, Interp_Vals.var(axis=1)[...,None]),axis=1)
#Interp_Vals = np.concatenate((Interp_Vals, Interp_Vals.mean(axis=1)[...,None]),axis=1)      # getting the mean

Interp_Vals = np.concatenate((Interp_Vals, np.median(Interp_Vals, axis=1)[...,None]),axis=1) # getting the mdeian

name = '/home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/TEMP/First_Guess_DATA_' + vari_cclm + '_'+ SEAS_cclm + '_'+ str(year[yr_bp]) + '.csv'

with open(name, 'wb') as f:                                #write the First Guess files for the time-slice and all years
        writer = csv.writer(f)
        writer.writerows(izip(f2(points_in[:, 2]),f2(points_in[:, 1]),f2(Interp_Vals[:,-1]), f2(Interp_Vals[:,-2])))
        # lon, lat, value, variance
print
print 'FILES CREATED SUCCESSFULLY'
print os.getcwd()
print 'ENS_BG_OBS.py'

# ======================================================================================================================

