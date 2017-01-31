# run octave from python (IO code )
from oct2py import octave
import numpy as np
import csv
import os
import numpy
from netCDF4 import Dataset as NetCDFFile
from Read_CCLM import Plot_CCLM as pltcc
year = np.array([12000, 11000, 10000, 9000, 8000, 7000, 6000, 5000, 4000, 3000, 2000, 1000,  100])# years in proxy Data
# ===================================== Namelist =======================================================================
DIR='/home/fallah/Documents/DATA_ASSIMILATION/Bijan/CODES/Optimal_Interpolation/optiminterp/inst/'
yr_bp=6
vari_cclm     = 'T_2M'
SEAS_cclm     = 'DJF'
#if vari_cclm == 'T_2M':
pref_cclm     = 'eu_merge_seas_mm_'
#else:
#pref_cclm     = 'eu_merge_seas_mm_rr'



# ======================================================================================================================
octave.run(DIR+"run_IO.m")
fil_fi=DIR + 'fi_' + str(year[yr_bp]) + '.csv'
fil_vari=DIR + 'vari_' + str(year[yr_bp]) + '.csv'
lon=DIR + 'LON.out'
lat=DIR + 'LAT.out'
result_fi=numpy.array(list(csv.reader(open(fil_fi,"rb"),delimiter=','))).astype('float')
result_vari=numpy.array(list(csv.reader(open(fil_vari,"rb"),delimiter=','))).astype('float')

import numpy as np
from netCDF4 import Dataset
name='/scratch/users/fallah/CCLM_OI_HOLOCENE_DATA/Bijan/lffd7465122412.nc' # read the rlat and rlon from cclm netcdf file
nc = NetCDFFile(name)
rlats = nc.variables['rlat'][9:118]
rlons = nc.variables['rlon'][9:121]


nrows = len(rlats)
ncols = len(rlons)
# ======================================== Writing the Netcdef file of Values ==========================================
name_fi=DIR + 'FI_'+ str(year[yr_bp])+'.nc'
volcgrp = Dataset(name_fi, 'w', format='NETCDF3_64BIT')
volcgrp.createDimension('lat', nrows)
volcgrp.createDimension('lon', ncols)
rlon = volcgrp.createVariable('lon', 'f4', ('lon',))
rlat = volcgrp.createVariable('lat', 'f4', ('lat',))
FI  = volcgrp.createVariable('FI', 'f4', ('lat', 'lon'))
rlon[:] = rlons
rlat[:] = rlats
FI[:,:] = result_fi
volcgrp.close()
# ======================================================================================================================

# ======================================== Writing the Netcdef file of Variances =======================================
name_vari=DIR + 'VARI_'+ str(year[yr_bp])+'.nc'
volcgrp = Dataset(name_vari, 'w', format='NETCDF3_64BIT')
volcgrp.createDimension('lat', nrows)
volcgrp.createDimension('lon', ncols)
rlon = volcgrp.createVariable('lon', 'f4', ('lon',))
rlat = volcgrp.createVariable('lat', 'f4', ('lat',))
VARI  = volcgrp.createVariable('VARI', 'f4', ('lat', 'lon'))
rlon[:] = rlons
rlat[:] = rlats
VARI[:,:] = result_vari
volcgrp.close()
# ======================================================================================================================

lons_cclm, lats_cclm, t_cclm ,shapes_cclm = pltcc(dir_mistral='./', prefix='temp', seas='', expr='',
                                              plus_min='TRUE',var= vari_cclm, timming='TRUE', plotting='FALSE',
                                              grid='FALSE',all_times ='TRUE')
name_fi=DIR + 'DA_OUT_' + vari_cclm + '_' + SEAS_cclm + '_' + str(year[yr_bp])+'.nc'
volcgrp = Dataset(name_fi, 'w', format='NETCDF3_64BIT')
volcgrp.createDimension('rlat', nrows)
volcgrp.createDimension('rlon', ncols)
rlon = volcgrp.createVariable('rlon', 'f4', ('rlon',))
rlat = volcgrp.createVariable('rlat', 'f4', ('rlat',))
FI  = volcgrp.createVariable(vari_cclm, 'f4', ('rlat', 'rlon'))
rlon[:] = rlons
rlat[:] = rlats
FI[:,:] = result_fi + np.median(t_cclm,axis=0).squeeze()
volcgrp.close()
#order = 'cdo ncatted -a coordinates,' + vari_cclm + ',c,c,"lon lat"' + name_fi
#os.system(order)
#order = 'ncks -A -v lat,lon' + '/home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/TEMP/temp.nc ' + name_fi
#os.system(order)
print os.getcwd()
print 'run_octave.py'