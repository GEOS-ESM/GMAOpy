#! /usr/bin/env python
#

import numpy as np
import matplotlib.pyplot as plt
from numpy import *

def var_info(var):
    
    # Define regionclass
    class variable(object):
        def _init_(self, name=None):
            self.name      = name
            self.datarange = datarange

        
        
        
    T=variable()
    T.name      = 'T'
    T.datarange = np.arange(0, 32, 1)
    T.contours  = np.arange(-10, 40, 1)
    T.units     = 'T $[^oC]$'
    T.lev_var   = 'TEMP'
    T.clab      = [8,10,12,16,20,24,28]
    T.clabfat   = [2,1,1,1,1,2,1,1,1,1,2,1,1,1,1,2,1,1,1,1,2,1,1,1,1,2,1,1,1,1,2,1,1,1,1,2,1,1,1,1,2,1,1,1,1,2,1,1,1,1,2]
        
    S=variable()
    S.name      = 'S'
    S.datarange = np.arange(33,36,.1)
    S.contours  = np.arange(30,40,.1)
    S.units     = 'S $[psu]$'
    S.lev_var   = 'SALT'
    S.clab      = np.arange(33,36,.2)
    S.clabfat   = [2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2]
    
    SLA=variable()
    SLA.name      = 'SSH'
    SLA.datarange = np.arange(-.1,0.01,.1)
    SLA.contours  = np.arange(-.1,0.01,.1)
    SLA.units     = 'SSH $[m]$'
    SLA.lev_var   = 'SSH'
    SLA.clab      = np.arange(-.1,0.02,.1)
    SLA.clabfat   = [2,1,2,1,2,1,2,1,2,1,2]
    
    for variable in [eval(var)]:
        var_info.datarange = variable.datarange
        var_info.units     = variable.units
        var_info.lev_var   = variable.lev_var
        var_info.clab      = variable.clab
        var_info.clabfat   = variable.clabfat
        var_info.contours  = variable.contours
        var_info.name      = variable.name

    return var_info
