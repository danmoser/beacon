#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" Program to add the *UT* entry the in fits header. It requires the 
*DATE-OBS* entry. """

import pyfits as pf
from glob import glob
import numpy as np
import jdcal


def hms2fracday(hms):
    """ Enter hour:min:sec (string) and return fraction of a day (float) """
    hms = np.array(hms.split(':'), dtype='float')
    return (hms[0] + hms[1]/60. + hms[2]/3600.) / 24.


def longdate2MJD(ldate):
    """ FROM YYYY-MM-HHThh:mm:ss.sss to MJD (float). """
    ldate, hms = ldate.split('T')
    ldate = np.array(ldate.split('-'), dtype=int)
    mjd = jdcal.gcal2jd(*ldate)[1]
    return mjd + hms2fracday(hms)


if __name__ == '__main__':
    lfits = glob('*.fit*')
    for fn in lfits:
        f = pf.open(fn, mode='update')
        if 'DATE-OBS' in f[0].header and 'UT' not in f[0].header:
            ldate, hms = f[0].header['DATE-OBS'].split('T')
            f[0].header['UT'] = hms
            f.flush()
            print('# {0} updated with UT!'.format(fn))
        elif 'DATE-OBS' not in f[0].header:
            print('# ERROR! DATE-OBS not in header of {0}'.format(fn))
        else:
            print('# {0} already contains UT info.'.format(fn))
        f.close()
