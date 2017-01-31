#!/bin/bash
# ======================================================================================================================
# Here is the heart of the system:
# created by:
#
# .______    __         __       ___      .__   __.     _______    ___       __       __          ___       __    __
# |   _  \  |  |       |  |     /   \     |  \ |  |    |   ____|  /   \     |  |     |  |        /   \     |  |  |  |
# |  |_)  | |  |       |  |    /  ^  \    |   \|  |    |  |__    /  ^  \    |  |     |  |       /  ^  \    |  |__|  |
# |   _  <  |  | .--.  |  |   /  /_\  \   |  . `  |    |   __|  /  /_\  \   |  |     |  |      /  /_\  \   |   __   |
# |  |_)  | |  | |  `--'  |  /  _____  \  |  |\   |    |  |    /  _____  \  |  `----.|  `----./  _____  \  |  |  |  |
# |______/  |__|  \______/  /__/     \__\ |__| \__|    |__|   /__/     \__\ |_______||_______/__/     \__\ |__|  |__|
#
#                                               info@bijan-fallah.com
#
#
#
#
#  Just edit the "NAMELIST PART" and the "PATH to DIRs" please:
#
#
#
# ======================================================================================================================

set -ex
# ======================================== NAMELIST =========================================
#[12000, 11000, 10000, 9000, 8000, 7000, 6000, 5000, 4000, 3000, 2000, 1000,  100]
# 0        1      2      3    4     5     6     7     8     9     10    11     12
yr_bp=6              # Time slice's year
#M=30                     # Number of influential observations
SEAS_cclm='DJF'           # Season of time slice
vari_cclm='T_2M'          # Variable of interest to be processed
# vari_cclm='TOT_PREC'
M=10000                #Number of influential points
flag=2 # 1 = thinning, 2 = super-obing
NAME='HOLOCENE_Gesund_Br_250_yrs_window_so'
# ===========================================================================================
SEAS_cclm_l=$(echo "${SEAS_cclm,,}")
echo $SEAS_cclm_l
# =================================== Corelation length adjustment ==========================
# The adjustment is based on the experiment done with shifted and not shifted cclm simulations
# The experiment codes and set-up are in /home/fallah/Documents/DATA_ASSIMILATION/Bijan/CODES/CCLM/Python_Codes/historical_runs_yearly

if [ ${SEAS_cclm} = 'DJF' ];
 then
  COR_LEN=12                 # Correlation Length
fi
if [ ${SEAS_cclm} = 'JJA' ];
 then
  COR_LEN=3                 # Correlation Length
fi
# ===========================================================================================

# ====================================== PATH to DIRs =======================================
DIR_python='/home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/'                  # DIR to python codes
DIR_OI='/home/fallah/Documents/DATA_ASSIMILATION/Bijan/CODES/Optimal_Interpolation/' # DIR to Optimal Interpolation exe files
DIR_WORK='/scratch/users/fallah/'                                                    # DIR to work space
# ===========================================================================================

pref_prox_val='EPOCH-2_new_1'
if [ ${vari_cclm} = 'T_2M' ];
  then
   vari_prox_val=tanom_${SEAS_cclm_l}

fi
if [ ${vari_cclm} = 'TOT_PREC' ];
  then
   vari_prox_val=panom_${SEAS_cclm_l}

fi

pref_prox_un='EPOCH-2_uncertainties_new_1'


if [ ${vari_cclm} = 'T_2M' ];
  then
   vari_prox_un=tanom_${SEAS_cclm_l}_se
fi
if [ ${vari_cclm} = 'TOT_PREC' ];
  then
   vari_prox_un=panom_${SEAS_cclm_l}_se
fi

pref_cclm='eu_merge_seas_mm_'




NAME=${NAME}_${COR_LEN}
if [ ! -d ${DIR_WORK}$NAME ];
 then
  mkdir ${DIR_WORK}${NAME}
fi
if [ ! -d ${DIR_WORK}$NAME/PLOTS ];
 then
 mkdir ${DIR_WORK}${NAME}/PLOTS
fi
cd ${DIR_WORK}${NAME}/PLOTS

if [ ! -d ${DIR_WORK}${NAME}/TEMP ]; then
  mkdir ${DIR_WORK}${NAME}/TEMP
fi

cp ${DIR_python}/*py ${DIR_WORK}${NAME}/
cp -rf ${DIR_OI}optiminterp ${DIR_WORK}${NAME}/
cp  /home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/run_IO.m   ${DIR_WORK}${NAME}/optiminterp/inst/



XX="$DIR_WORK$NAME/Stations$NAME"

#================================= ENS_BG_OBS.py ====================================
sed -i "s/yr_bp=6/yr_bp=$yr_bp/g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py



or='EPOCH-2_new_1'
var1=$(echo ${or})
var2=$(echo ${pref_prox_val})
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py

or='tanom_djf'
var1=$(echo ${or})
var2=$(echo ${vari_prox_val})
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py


or='path_to_prox_scatter'
var1=$(echo ${or})
var2=$(echo ${DIR_WORK}${NAME}/)
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py


or='EPOCH-2_uncertainties_new_1'
var1=$(echo ${or})
var2=$(echo ${pref_prox_un})
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py

or='tanom_djf_se'
var1=$(echo ${or})
var2=$(echo ${vari_prox_un})
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py

or='T_2M'
var1=$(echo ${or})
var2=$(echo ${vari_cclm})
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py

or='DJF'
var1=$(echo ${or})
var2=$(echo ${SEAS_cclm})
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py

or='eu_merge_seas_mm_'
var1=$(echo ${or})
var2=$(echo ${pref_cclm})
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py

sed -i "s/yr_bp=6/yr_bp=$yr_bp/g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py
sed -i "s/999999/$flag/g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py
sed -i "s/yr_bp=6/yr_bp=$yr_bp/g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py
sed -i "s/yr_bp=6/yr_bp=$yr_bp/g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py
sed -i "s/yr_bp=6/yr_bp=$yr_bp/g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py
sed -i "s/yr_bp=6/yr_bp=$yr_bp/g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py

or='/home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/TEMP/First_Guess_DATA_'
var1=$(echo ${or})
var2=$(echo ${DIR_WORK}${NAME}/TEMP/First_Guess_DATA_)
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py

or='/home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/TEMP/Stations_'
var1=$(echo ${or})
var2=$(echo ${DIR_WORK}${NAME}/TEMP/Stations_)
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/ENS_BG_OBS.py

#====================================================================================

#===================================== run_IO.m =====================================
sed -i "s/lenx = 20;/lenx = $COR_LEN/g" ${DIR_WORK}${NAME}/optiminterp/inst/run_IO.m
sed -i "s/leny = 20;/leny = $COR_LEN/g" ${DIR_WORK}${NAME}/optiminterp/inst/run_IO.m
sed -i "s/m = 50;/m= $M/g" ${DIR_WORK}${NAME}/optiminterp/inst/run_IO.m
yr_bp=`expr $yr_bp + 1` # +1 because of the difference between python and octave codes
sed -i "s/yr_bp=7;/yr_bp=$yr_bp/g" ${DIR_WORK}${NAME}/optiminterp/inst/run_IO.m
var1=$(echo ${DIR_python})
var2=$(echo ${DIR_WORK}${NAME}/)
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/optiminterp/inst/run_IO.m
#=====================================================================================

#===================================== run_cotave.py =================================
DIR='/home/fallah/Documents/DATA_ASSIMILATION/Bijan/CODES/Optimal_Interpolation/optiminterp/inst/'
var1=$(echo ${DIR})
var2=$(echo ${DIR_WORK}${NAME}/optiminterp/inst/)
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/run_octave.py
yr_bp=`expr $yr_bp - 1` # -1 because of the difference between python and octave codes
sed -i "s/yr_bp=6/yr_bp=$yr_bp/g" ${DIR_WORK}${NAME}/run_octave.py

or='DJF'
var1=$(echo ${or})
var2=$(echo ${SEAS_cclm})
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/run_octave.py

or='T_2M'
var1=$(echo ${or})
var2=$(echo ${vari_cclm})
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/run_octave.py
#=====================================================================================

#================================== Create_Input_for_IO.py ===========================
## TODO: fill this part please!
DIR='/home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/TEMP/'
var1=$(echo ${DIR})
var2=$(echo ${DIR_WORK}${NAME}/TEMP/)
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/Create_Input_for_OI.py
sed -i "s/yr_bp=6/yr_bp=$yr_bp/g" ${DIR_WORK}${NAME}/Create_Input_for_OI.py

or='T_2M'
var1=$(echo ${or})
var2=$(echo ${vari_cclm})
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/Create_Input_for_OI.py

or='DJF'
var1=$(echo ${or})
var2=$(echo ${SEAS_cclm})
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/Create_Input_for_OI.py

or='eu_merge_seas_mm_'
var1=$(echo ${or})
var2=$(echo ${pref_cclm})
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/Create_Input_for_OI.py
#=====================================================================================
#======================== Ploting_final_results.py ===================================


sed -i "s/yr_bp=7/yr_bp=$yr_bp/g" ${DIR_WORK}${NAME}/Ploting_final_results.py
or='T_2M'
var1=$(echo ${or})
var2=$(echo ${vari_cclm})
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/Ploting_final_results.py

or='DJF'
var1=$(echo ${or})
var2=$(echo ${SEAS_cclm})
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/Ploting_final_results.py



or='/home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/'
var1=$(echo ${or})
var2=$(echo ${DIR_WORK}${NAME}/)
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/Ploting_final_results.py






or='HOLOCENE_RUN_3'
var1=$(echo ${or})
var2=$(echo ${NAME})
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/Ploting_final_results.py


if [ ${vari_cclm} = 'TOT_PREC' ];
then
 or='vmin=-6'
 var1=$(echo ${or})
 var2='vmin=-2.5'
 sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/Ploting_final_results.py
fi

if [ ${vari_cclm} = 'TOT_PREC' ];
then
 or='vmax=6'
 var1=$(echo ${or})
 var2='vmax=2.5'
 sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/Ploting_final_results.py
fi
sed -i "s/flag=1/flag=$flag/g" ${DIR_WORK}${NAME}/Ploting_final_results.py



#=====================================================================================
#======================== scatter_proxies_obing_thinning.py =========================================
var2=$(echo ${SEAS_cclm_l})
var1='jja'
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/scatter_proxies_obing_thinning.py

sed -i "s/yr_bp=7/yr_bp=$yr_bp/g" ${DIR_WORK}${NAME}/scatter_proxies_obing_thinning.py
sed -i "s/flag=1/flag=$flag/g" ${DIR_WORK}${NAME}/scatter_proxies_obing_thinning.py
or='path'
var1=$(echo ${or})
orr=${DIR_WORK}${NAME}/
var2=$(echo $orr)
echo $var1
echo $var2
sed -i "s%$var1%$var2%g" ${DIR_WORK}${NAME}/scatter_proxies_obing_thinning.py
#=====================================================================================
#==================================== Python calls ===================================
#python ${DIR_WORK}${NAME}/scatter_proxies.py
python ${DIR_WORK}${NAME}/scatter_proxies_obing_thinning.py
python ${DIR_WORK}${NAME}/ENS_BG_OBS.py
python ${DIR_WORK}${NAME}/Create_Input_for_OI.py
python ${DIR_WORK}${NAME}/run_octave.py
python ${DIR_WORK}${NAME}/Ploting_final_results.py
#=====================================================================================

#cp ${DIR_WORK}${NAME}/optiminterp/inst/*nc ./


