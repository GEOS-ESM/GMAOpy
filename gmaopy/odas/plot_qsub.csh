#!/bin/csh -vx
##PBS -S /bin/csh 
#PBS -W group_list=g0609
#PBS -l walltime=02:00:00
#PBS -l select=1:ncpus=4
#PBS -N plot_all
#PBS -q pproc

umask 022

##!/bin/csh
#
# USAGE:
# qsub plot_all_qsub.csh -v EXPNAME=${expname},YEAR=${year},MONTH=${mon}

setenv prod /discover/nobackup/projects/gmao/ssd/g5odas/production/GEOS5odas-3.2/

module purge
module load comp/intel-11.1.038
 
# Start: User Defined Parameters
  set expname   = $EXPNAME         #'mvoi_1980'
  set startyear = $YEAR        #{1979}
  set endyear   = $YEAR        #{1979}
  set startmon  = $MONTH       #{01}
  set endmon    = $MONTH        #{12}
  set grp       = fcst        #'fcst'
  set lev1      = 0        #min depth
  set lev2      = 500        #max depth
  set ilat      = 0         # latitude for glb region
# End: User Defined Parameters

set plot_xz = 1
set plot_yz = 1
set plot_xy = 1

set codes = /discover/nobackup/projects/gmao/ssd/g5odas/production/GEOS5odas-3.2/rc/pproc_utils/

#############################
# PLOT_XZ_SLICE
#############################
if ($plot_xz == 1) then
set regions   = {eqpac,eqind,eqatl,glb}
set variables = {S,T}

mkdir ${prod}/${expname}/pics/
mkdir ${prod}/${expname}/pics/Vertical_Fields/
mkdir ${prod}/${expname}/pics/Vertical_Fields/xz_slice

set year = $startyear
while ($year <= $endyear) 
  set mon = $startmon
  while ($mon <= $endmon) 
    #if ($mon <= 9) then
    #  set mon = '0'$mon
    #endif 

    echo $year$mon

    foreach reg ($regions)
      foreach var ($variables)

        ${codes}/plot_ocean_state/plot_xz_slice.py $grp $var $reg $lev1 $lev2 $ilat $expname $year $mon 
        ${codes}/plot_ocean_state/plot_xz_slice.py $grp $var $reg 0 2000 $ilat $expname $year $mon 

      end
    end

    set mon = `expr $mon + 1`

  end # months
  set year = `expr $year + 1`
end # years

endif #plot_xz


#############################
# PLOT_YZ_SLICE
#############################
if ($plot_yz == 1) then

set regions   = {i60E,i75E,i90E,p165E,p180E,p155W,p140W,p125W,p110W,a30W,a15W}
set variables = {T,S}

mkdir ${prod}/${expname}/pics/Vertical_Fields/yz_slice

set year = $startyear
while ($year <= $endyear) 
  set mon = $startmon
  while ($mon <= $endmon) 
    #if ($mon <= 9) then
    #  set mon = '0'$mon
    #endif 

    echo $year$mon

    foreach reg ($regions)
      foreach var ($variables)

        ${codes}/plot_ocean_state/plot_yz_slice.py $grp $var $reg $lev1 $lev2 $expname $year $mon 
        ${codes}/plot_ocean_state/plot_yz_slice.py $grp $var $reg 0 2000 $expname $year $mon 

      end
    end

    set mon = `expr $mon + 1`

  end # months
  set year = `expr $year + 1`
end # years
endif

#############################
# PLOT_XY_SLICE
#############################
if ($plot_xy == 1) then

mkdir /gpfsm/dnb42/projects/p17/production/GEOS5odas-3.2/${expname}/pics/Horizontal_Fields/

set year = $startyear
while ($year <= $endyear) 
  set mon = $startmon
  while ($mon <= $endmon) 
    #if ($mon <= 9) then
    #  set mon = '0'$mon
    #endif 

    ${codes}/plot_ocean_state/plot_xy_slice.py T $expname -5 30 1   0  $year $mon Horizontal_Fields 
    ${codes}/plot_ocean_state/plot_xy_slice.py S $expname 30 37 0.3 0  $year $mon Horizontal_Fields 
    ${codes}/plot_ocean_state/plot_xy_slice.py T $expname -5 30 1   10 $year $mon Horizontal_Fields 
    ${codes}/plot_ocean_state/plot_xy_slice.py S $expname 30 37 0.3 10 $year $mon Horizontal_Fields 
    ${codes}/plot_ocean_state/plot_xy_slice.py SSH $expname -.1 .1 0.01 0 $year $mon Horizontal_Fields 

    set mon = `expr $mon + 1`

  end # months
  set year = `expr $year + 1`
end # years
endif

exit
