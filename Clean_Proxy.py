'''
Project to read and unpack the zip file regarding the Mauri et al. (2015) paper
doi:10.1016/j.quascirev.2015.01.013
01/11/2016

'''
import numpy as np
from Read_CCLM import Plot_CCLM as pltcc
#from netCDF4 import Dataset as NetCDFFile
#from Read_CCLM import nanargmax
import os
import matplotlib.pyplot as plt
#path="/home/bijan/Documents/DATA"
path="/scratch/users/fallah/trash/EPOCH-2_Mauri_etal_QSR"
year = np.array([12000, 11000, 10000, 9000, 8000, 7000, 6000, 5000, 4000, 3000, 2000, 1000,  100])

if not os.path.exists(path):# Check if the Proxy files exist
    print("file exists")
    #scratch="/scratch/users/fallah/trash"
    scratch="/home/bijan/DATA"
    wrk=os.getcwd()
    os.chdir(scratch)
    os.system("curl -sS  http://arve.unil.ch/pub/EPOCH-2_Mauri_etal_QSR.tar.gz> file.gz")
    os.system("tar -zxvf file.gz")
    os.system("rm -f file.gz")
    os.chdir(wrk)
else: # test plot of RECONSTRUCTIONS for 6000-200 BP and T_2M
    pref = 'EPOCH-2_new_1'
    vari = 'tanom_djf'
    name = pref + '.pdf'
    fig = plt.figure('1')
    fig.set_size_inches(14, 10)
    pltcc(dir_mistral=path, prefix=pref, seas='', expr='', plus_min='TRUE', var= vari, timming='TRUE',
          plotting='TRUE', time=7)
    plt.savefig(name)
    plt.close()

# Now find the same time slice in model outs(anomaly w.r.t 200BP) and plot:


model_path = '/scratch/users/fallah/CCLM_OI_HOLOCENE_DATA/Bijan'
#model_path='/home/bijan/Documents/DATA/Bijan'
pref = 'eu_merge_seas_mm_'
vari = 'T_2M'
SEAS= 'DJF'
yr_bp=6
yr_model=7
name1 = model_path + '/' +pref + vari+ '_' + SEAS + '_' + str(year[yr_bp]) + 'bp.nc'
name2 = model_path + '/' +pref + vari+ '_' + SEAS + '_' + '200bp.nc'
CMD = 'cdo sub ' + name1 + ' ' + '-timmean ' + name2 +' ./temp.nc'
os.system(CMD)
name = pref + vari + '_' + str(year[yr_bp]) + 'bp.pdf'
fig = plt.figure('1')
fig.set_size_inches(14, 10)

# Plot the contour of model output:
pltcc(dir_mistral='./', prefix='temp', seas='', expr='', plus_min='TRUE', var= vari, timming='TRUE',
      plotting='TRUE', time=yr_model, grid='FALSE')

# Plot the proxy grids:

pref = 'EPOCH-2_new_1'
vari = 'tanom_djf'
pltcc(dir_mistral=path, prefix=pref, seas='', expr='', plus_min='TRUE', var= vari, timming='TRUE',plotting='TRUE',flag='FALSE',
      time=7, grid='TRUE')
plt.savefig(name)
plt.close()

#TODO: Now create the input files for the OI scheme
#TODO: conduct OI for all years of each time-slice and create netcdf files (DJF, JJA, Yearly, T_2M and PRECIP)
#
