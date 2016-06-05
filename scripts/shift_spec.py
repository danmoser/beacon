#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" Program that shifts a FITS spectrum based on an Halpha Gaussian fit.
"""

from glob import glob
import numpy as np
import sys
import pyfits as pf
import pyhdust.spectools as spt
import pyhdust.phc as phc
from scipy.optimize import curve_fit
from argparse import ArgumentParser

__version__ = "0.9"
__author__ = "Daniel Moser"
__email__ = "dmfaes@gmail.com"


class MyParser(ArgumentParser): 
    def error(self, message):
        sys.stderr.write('# Error: %s\n' % message)
        self.print_help()
        sys.exit(2)


parser = MyParser(description=__doc__)
parser.add_argument('--version', action='version', 
    version='%(prog)s {0}'.format(__version__))
parser.add_argument("INPUT", help=("String to retrive the spectrum(a) "
    "filename(s) (wildcards accepted)"))
parser.add_argument("-l", "--line", action="store", dest="line", 
    help=("Wavelength of the reference line [default: %(default)s]"), 
    type=float, default=6562.79)

args = parser.parse_args()


def gauss(x, a, x0, sigma, y0=1.):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))+y0


def find_max_peak(vl, nflx, idx=-1):
    """ Based on max flux. 
    """
    if idx == -1:
        idx = np.where(nflx == np.max(nflx))
        return nflx[idx], vl[idx]
    else:
        idx_ = np.where(nflx[:idx] == np.max(nflx[:idx]))
        nfV, vlV = nflx[idx_], vl[idx_]
        idx_ = np.where(nflx[idx:] == np.max(nflx[idx:]))
        nfR, vlR = nflx[idx_], vl[idx_]
    return nfV, vlV, nfR, vlR


def has_central_absorp(nf0, vlV, vlR):
    """ Return ``True`` or ``False`` if the line has a central absorption 
    (i.e., it is an absorption line or it is an double peak emission line).
    """
    if nf0 < 1:
        # print('# F(lb=0) < 1: A double-peak emission line was found!')
        return True
    if vlR-vlV > 100:
        return True
    else:
        return False


def gauss_fit(x, y, a0=None, x0=None, sig0=None, y0=None, emission=True):
    """ Return ``curve_fit``, i.e., ``popt, pcov``.
    """
    if a0 is None:
        a0 = np.percentile(y, 95) - np.mean(y)
        if not emission:
            a0 *= -1
    if x0 is None:
        x0 = np.sum(x*y)/len(x)
    if sig0 is None:
        sig0 = (x[-1]-x[0])/10.
    if y0 is None:
        q = 5
        if not emission:
            q = 95
        y0 = np.percentile(y, q)
    return curve_fit(gauss, x, y, p0=[a0, x0, sig0, y0])

lbc = args.line
linput = args.INPUT

for fitsfile in glob(linput):

    imfits = pf.open(fitsfile, mode='update')
    flux = imfits[0].data
    wl = np.arange(len(flux)) * imfits[0].header['CDELT1'] + \
        imfits[0].header['CRVAL1']

    vl, nflx = spt.lineProf(wl, flux, lbc=lbc)
    idx0 = phc.find_nearest(vl, 0., idx=True)
    nf0 = nflx[idx0]
    nfV, vlV, nfR, vlR = find_max_peak(vl, nflx, idx=idx0)

    if has_central_absorp(nf0, vlV, vlR):
        idxV = phc.find_nearest(vl, vlV, idx=True)
        idxR = phc.find_nearest(vl, vlR, idx=True)+idx0
        popt, pcov = gauss_fit(vl[idxV:idxR], nflx[idxV:idxR], emission=False)
    else:
        popt, pcov = gauss_fit(vl, nflx)

    vshift = -popt[1]
    new_wl = wl*(1 + vshift/phc.c.cgs*1e5)

    imfits[0].header['CDELT1'] = (new_wl[-1]-new_wl[0])/(len(new_wl)-1)
    imfits[0].header['CRVAL1'] = new_wl[0]
    # imfits[0].data = np.interp(new_wl, wl, flux)

    old_sh = 0
    if 'VELSHIFT' in imfits[0].header:
        old_sh = imfits[0].header['VELSHIFT'] 
    imfits[0].header['VELSHIFT'] = (vshift + old_sh, 'Lambda shift in km/s')

    print('# {0} updated with {1:.1f} km/s shift (accum. {2:.0f} km/s)'.format(
        fitsfile, vshift, vshift+old_sh))
    imfits.close()

if len(glob(linput)) == 0:
    print('# ERROR! {0} files were not found!'.format(linput))
