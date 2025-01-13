#!/bin/csh

setenv MODULEPATH /discover/nobackup/ebsmith2/gpy/releases/modules:$MODULEPATH
module load gpy/1.93

# YYYYMMDDHH
set bdate = $1
set edate = $2
set exp = $3

#if ( "$exp" == "e5131_fp" ) then
#    setenv SEMPERPY_CONFIG /discover/nobackup/ebsmith2/gpy/releases/config/1.90.ops.e5131_fp/config
#endif
setenv SEMPERPY_CONFIG /discover/nobackup/ebsmith2/o2h/o2h/config
#if ( "$exp" == "f516_fp" ) then
#    setenv SEMPERPY_CONFIG /discover/nobackup/ebsmith2/gpy/releases/config/1.90.ops.f516_fp/config
#endif
#if ( "$exp" == "f515_fpp" ) then
#    setenv SEMPERPY_CONFIG /discover/nobackup/ebsmith2/gpy/releases/config/1.90.ops.f515_fpp/config
#endif
#if ( "$exp" == "d5124_m2_jan10" ) then
#    setenv SEMPERPY_CONFIG /discover/nobackup/projects/gmao/share/dao_ops/lib/python/gmaopy/1.90.ops.merra2/gmaopy/config
#endif
#if ( "$exp" == "d5124_rpit_jan00" ) then
#    setenv SEMPERPY_CONFIG /discover/nobackup/ebsmith2/gpy/releases/config/1.90.ops.rpit/config
#endif
#if ( "$exp" == "d5124_rpit_jan04" ) then
#    setenv SEMPERPY_CONFIG /discover/nobackup/ebsmith2/gpy/releases/config/1.90.ops.rpit/config
#endif
#if ( "$exp" == "d5124_rpit_jan12" ) then
#    setenv SEMPERPY_CONFIG /discover/nobackup/ebsmith2/gpy/releases/config/1.90.ops.rpit/config
#endif
echo "SEMPERPY_CONFIG set to $SEMPERPY_CONFIG"

cd /discover/nobackup/ebsmith2/gpy/releases/1.93/scripts/o2h
echo "Working directory is `pwd`"

echo "Performing $exp database conventional statistics."
python compute_ozone.py $bdate $edate $exp &
python compute_conv.py $bdate $edate $exp &
python compute_iasi.py $bdate $edate $exp &
python compute_airs.py $bdate $edate $exp &
python compute_cris.py $bdate $edate $exp &
python compute_tovs_etc_radiance.py $bdate $edate $exp &

wait
