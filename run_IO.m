% Program to read INOUT files and run the IO scheme
yr_bp=7;
lenx = 20; % Correlation length in x direction
leny = 20; % Correlation length in y direction
m = 50; % Number of influential points

year = [12000, 11000, 10000, 9000, 8000, 7000, 6000, 5000, 4000, 3000, 2000, 1000,  100];
name = strcat('INPUT_', num2str(year(yr_bp)),'.csv')
system(strcat('cp /home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/TEMP/',name,' ./'))
system('cp /home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/TEMP/LON.out ./')
system('cp /home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/TEMP/LAT.out ./')
DIR='./'
INPUT=load(strcat(DIR,name));
LON=load(strcat(DIR,'LON.out'));
LAT=load(strcat(DIR,'LAT.out'));
[fi,vari] = optiminterp2(INPUT(:,1),INPUT(:,2),INPUT(:,3),INPUT(:,4),lenx,leny,m,LON,LAT);
system('rm *csv')
csvwrite(strcat('/home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/optiminterp/inst/fi_',num2str(year(yr_bp)),'.csv'),reshape(fi',size(fi)(2),size(fi)(1)))
csvwrite(strcat('/home/fallah/Documents/paper_cubasch/CCLM_OI_HOLOCENE/optiminterp/inst/vari_',num2str(year(yr_bp)),'.csv'),reshape(vari',size(fi)(2),size(fi)(1)))


