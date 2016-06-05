#!/usr/bin/env python
# -*- coding:utf-8 -*-

from optparse import OptionParser
from glob import glob
import sys
import numpy as np
import pyfits as pf
import jdcal

""" Adds information in MUSICOS observation FITS file to the OPERA reduction.
    New keywords: MJD-OBS, MODDATA, DEC_DEG, RA_DEG, INSTMODE, EXPTIME2, 
    OBSTYPE, READTIME
"""

__author__ = "Daniel Moser"
__email__ = "dmfaes@gmail.com"

parser = OptionParser()
parser.add_option("-d", "--dir", dest="dir", help="Dir. containing the files",
    type='string', default="./")
parser.add_option("-b", "--bias", dest="bias", help="Bias filename prefix",
    type='string', default="bias*")
parser.add_option("-f", "--flats", dest="flats", help="Flat filename prefix",
    type='string', default="flat*")
parser.add_option("-l", "--lamp", dest="lamp", help="Lamp filename prefix",
    type='string', default="lamp*")
parser.add_option("-o", "--objs", dest="objs", help="Obj filename prefix", 
    type='string', default="*")
parser.add_option("-B", "--blue", action="store_true", dest="bluemode",
    help="Are the files of BLUE mode? Otherwise, RED", default=False)
parser.add_option("-r", "--dry-run", action="store_true", dest="dryrun",
    help="Dry run?", default=False)
parser.add_option("-w", "--overwrite", action="store_true", dest="overwrite",
    help="Overwrite header info?", default=False)

try:
    option, args = parser.parse_args(sys.argv[1:])
except:
    parser.error("Check usage with '-h' ")
    sys.exit(1)


def hms2fracday(hms):
    """ Enter hour:min:sec (string) and return fraction of a day (float) """
    hms = np.array(hms.split(':'), dtype='float')
    return (hms[0] + hms[1]/60. + hms[2]/3600) / 24.


def longdate2MJD(ldate):
    """ FROM YYYY-MM-HHThh:mm:ss.sss to MJD (float). """
    ldate, hms = ldate.split('T')
    ldate = np.array(ldate.split('-'), dtype=int)
    mjd = jdcal.gcal2jd(*ldate)[1]
    return mjd + hms2fracday(hms)


def ra2degf(rastr):
    """ RA to degrees (decimal). Input is string. """
    rastr = rastr.replace('::', ':')
    rastr = rastr.replace(',', '.')
    vals = np.array(rastr.split(':')).astype(float)
    return (vals[0] + vals[1] / 60. + vals[2] / 3600.) * 360. / 24


def dec2degf(decstr, delimiter=":"):
    """ Sexagesimal to decimal. Input is string. """
    vals = np.array(decstr.split(delimiter)).astype(float)
    if vals[0] < 0:
        vals[1:] *= -1
    return vals[0] + vals[1] / 60. + vals[2] / 3600.


def header_additions(files, type, blue=False, overwrite=False, dry=False):
    """ Do the MUSICOS header modifications.

    ``files`` = vector of filenames.

    ``type`` = BIAS, FLAT, COMP or OBJECT (upper case)."""

    type = type.upper()
    # 
    instmode = 'RED'
    if blue:
        instmode = 'BLUE'
    # 
    for fn in files:
        f = pf.open(fn, mode='update')
        if ('MODDATA' not in f[0].header) or (overwrite):
            f[0].header['READTIME'] = '1.0E-06'
            f[0].header['INSTRUME'] = 'MUSICOS'
            # 
            expt = f[0].header['EXPTIME'].replace(',', '.')
            f[0].header['EXPTIME2'] = (float(expt),
                'Exposure time inserted by OPERA')
            #
            f[0].header['MJD-OBS'] = (longdate2MJD(f[0].header['DATE-OBS']),
                'MJD = JD - 2400000.5')
            #
            f[0].header['DEC_DEG'] = (dec2degf(f[0].header['DEC']),
                'Dec in degrees')
            f[0].header['RA_DEG'] = (ra2degf(f[0].header['RA']),
                'RA in degrees')
            #
            if type is not 'BIAS':
                f[0].header['INSTMODE'] = (instmode,
                    'prism configuration: RED or BLUE')
            f[0].header['OBSTYPE'] = type
            # 
            moddata = 'Header modified by OPERA pipeline'
            f[0].header['MODDATA'] = (True, moddata)
        # 
            if not dry:
                print('# {0} as {1} updated to OPERA!'.format(fn, type))
                f.flush()  # changes are written back to original fits
            else:
                print('# {0} as {1} will be updated!'.format(fn, type))
        f.close()  # closing the file will also flush any changes and prevent
        # being updated
    return

if __name__ == '__main__':

    overwrite = option.overwrite
    # BIAS
    bias = glob(option.dir+'/'+option.bias+'*.fit*')
    header_additions(bias, 'BIAS', blue=option.bluemode, overwrite=overwrite, 
        dry=option.dryrun)
    # FLAT
    flat = glob(option.dir+'/'+option.flats+'*.fit*')
    header_additions(flat, 'FLAT', blue=option.bluemode, overwrite=overwrite, 
        dry=option.dryrun)
    # LAMP
    lamp = glob(option.dir+'/'+option.lamp+'*.fit*')
    header_additions(lamp, 'COMP', blue=option.bluemode, overwrite=overwrite, 
        dry=option.dryrun)
    # Other
    objs = glob(option.dir+'/'+option.objs+'*.fit*')
    other = np.array(bias+flat+lamp)
    objs = np.array(objs)
    objs = objs[~np.in1d(objs, other)]
    header_additions(objs, 'OBJECT', blue=option.bluemode, overwrite=overwrite, 
        dry=option.dryrun)
