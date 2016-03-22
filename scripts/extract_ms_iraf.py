#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Program to normalize spectra from IRAF Echelle format based on derivative 
variations.
"""

import os
from glob import glob
import numpy as np
# import pyhdust.spectools as spt
# import pyhdust.phc as phc
from scipy import interpolate
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import specutils.io as sio
import pyfits
import datetime as dt


def dtflag():
    """ Return a "datetime" flag, i.e., a string the the current date and time
    formated as yyyymmdd-hhMM."""
    now = dt.datetime.now()
    return '{0}{1:02d}{2:02d}-{3:02d}{4:02d}{5:02d}'.format(now.year, 
        now.month, now.day, now.hour, now.minute, now.second)


def sum_ec(fwl, fflx):
    dmin = np.inf
    wlmin = np.inf
    wlmax = 0
    for f in fwl:
        if np.min(np.diff(f)) < dmin:
            dmin = np.min(np.diff(f))
        if np.min(f) < wlmin:
            wlmin = np.min(f)
        if np.max(f) > wlmax:
            wlmax = np.max(f)
    swl = np.arange(wlmin, wlmax, dmin)
    sflx = np.zeros(len(swl))
    for i in range(len(fwl)):
        idx = np.where( (swl > np.min(fwl[i])) & (swl < np.max(fwl[i])) )
        sflx[idx] += np.interp(swl[idx], fwl[i], fflx[i])
    return swl, sflx


def plot_orders(ax, fwl, fflx, mode='o'):
    for i in range(len(fwl)):
        ax.plot(fwl[i], fflx[i], mode, ms=1)
    return ax


def splitequal(n, N):
    """ Split `N` in approx. `n` igual parts 

    `N` must be integer.

    Suggestion: *phc.splitequal(N/8., N)* split N into sequences of 
    approx. 8 itens.
    """
    n = int(round(n))
    idx = []
    for i in range(n):
        idx.append([i * N / n, (i + 1) * N / n])
    if n == 0:
        idx = [[0, N]]
    return idx


def max_func_pts(x, y, ws=0.01, avgbox=3):
    """ `ws` window size where the maximum will be evaluated. Example: `ws=0.02`
    corresponds to 2% of the length of the input. """
    x, y = (np.array(x), np.array(y))
    N = len(x)
    parts = splitequal(N*ws, N)
    n = len(parts)
    xout, yout = (np.zeros(n), np.zeros(n))
    for i in range(n):
        p = parts[i]
        Y = y[p[0]:p[1]]
        X = x[p[0]:p[1]]
        idx = np.argsort(Y)
        xout[i] = np.average(X[idx][-avgbox:])
        yout[i] = np.average(Y[idx][-avgbox:])
    return xout, yout


def do_norm(wl, flx):
    xout, yout = max_func_pts(wl, flx, ws=0.01, avgbox=5)
    tck = interpolate.splrep(xout, yout)
    ynew = interpolate.splev(xout, tck, der=1)
    dmed = np.median( np.abs(ynew) )
    l = len(wl)
    # ConditionA: small derivative 
    conda = ( np.abs(ynew) < dmed )  
    # ConditionB: in the limits
    condb = ( wl[int(l*0.15)] > xout ) | ( xout > wl[int(l*(1-.15))] )
    # xmax = phc.find_nearest(yout, np.max(yout), idx=True)
    # xmax = xout[xmax]
    # xmax = wl[l/2]
    # ConditionC: xout < max(flx) AND ynew > 0
    # condc = ( xout <= xmax ) & ( ynew >= 0 )
    # ConditionD: xout > max(flx) AND ynew < 0
    # condd = ( xout >= xmax ) & ( ynew <= 0 )
    conde = ( ( xout > 6584.5 ) | ( xout < 6541. ) )
    # idx = np.where( (( conda & (condd | condc) ) | condb) & (conde) )  
    idx = np.where( (conda | condb) & (conde) )  
    # & (condd | condc))
    xout = xout[idx]
    yout = yout[idx]
    tck = interpolate.splrep(xout, yout, k=3)
    wl = wl[2:-2]
    flx = flx[2:-2]
    ynew = interpolate.splev(wl, tck, der=0)
    return wl, flx, ynew


def writeFits(flx, lbd, extrahead=None, savename=None, quiet=False, path=None,
    lbdc=None, externhd=None):
    """ Write a 1D spectra FITS.

    | INPUT: flux array, lbd array, extrahead flag+info, save name.
    | - lbd array: if len(lbd)==2: lbd = [CRVAL1, CDELT1]
    |              else: CDELT1 = (lbd[-1]-lbd[0])/(len(lbd)-1)
    |                    CRVAL1 = lbd[0]
    |   WARNING: lbd must be in ANGSTROMS (FITS default). It can also be 
    |   velocities. In this case, it must be in km/s and lbdc is given in 
    | ANGSTROM.
    | - extrahead: matrix (n,2). Example: [['OBJECT','Achernar'], ['COMMENT',
    | 'value']]

    `externhd` = copy the header from an external file.

    OUTPUT: write FITS file.
    """
    if path is None or path == '':
        path = os.getcwd()
    if path[-1] != ['/']:
        path += '/'
    if lbdc is not None:
        lbd = (lbd / 2.99792458e10 * 1e5 + 1) * lbdc
    hdu = pyfits.PrimaryHDU(flx)
    hdulist = pyfits.HDUList([hdu])
    if externhd is not None:
        extf = pyfits.open(externhd)
        hdulist[0].header = extf[0].header
        hdulist[0].header['BZERO'] = 0.
    hdulist[0].header['CRVAL1'] = lbd[0]
    if len(lbd) == 2:
        hdulist[0].header['CDELT1'] = lbd[1]
    else:
        hdulist[0].header['CDELT1'] = (lbd[-1] - lbd[0]) / (len(lbd) - 1)
    if extrahead is not None:
        for e in extrahead:
            hdulist[0].header[e[0]] = e[1]
    if savename is None:
        savename = 'spec_{0}'.format(dtflag())
    if savename.find('.fit') == -1:
        savename += '.fits'
    hdu.writeto(path + savename, clobber=True)
    if not quiet:
        print('# FITS file {0}{1} saved!'.format(path, savename))
    return


if __name__ == '__main__':
    path = '.'
    opsps = glob('*.ms.cal.fits')
    print opsps

    # avgspecs = []
    for sp in opsps:
        # os.system('gunzip -c {0} > tmp.txt'.format(sp))
        # spec = np.loadtxt('tmp.txt', skiprows=11)
        spec = sio.read_fits.read_fits_spectrum1d(sp)

        # fig, ax = plt.subplots()
        # ax.plot(spec[:, 5], spec[:, 10], label='Leg.')
        # # ax.set_title('Title')
        # # ax.legend()
        # phc.savefig(fig, figname=sp.replace('.spc.gz', '_ori'))

        # i = 0
        onorm = []
        fwl = []
        oflx = []
        ocont = []
        # orders = np.unique(spec[:, 0])
        for i in range(len(spec)):
            wl = np.array(spec[i].wavelength)
            flx = np.array(spec[i].flux)
            try:
                wl, flx, ynew = do_norm(wl, flx)
                fwl.append(wl)
                onorm.append(flx/ynew)
                ocont.append(ynew)
                oflx.append(flx)        
            except:
                print('# Error in order {0}'.format(i))

        fig, ax = plt.subplots()
        ax = plot_orders(ax, fwl, oflx, 'o')
        ax = plot_orders(ax, fwl, ocont, '-')
        plt.savefig(sp.replace('.fits', '.orders'))

        swl, sflx = sum_ec(fwl, oflx)
        swl, scont = sum_ec(fwl, ocont)
        swl, snorm = sum_ec(fwl, onorm)

        # avgspecs.append(sp.replace('.spc.gz', '.rv.fits'))
        nans, x = (np.isnan(scont), lambda z: z.nonzero()[0])
        sflx[nans] = 1.
        scont[nans] = 1.
        idx = np.where(scont <= 1e-3)
        scont[idx] = 1.
        sflx[idx] = 1.
        final = sflx/scont
        idx = np.where((final > 0.986) & (final < 1.014))
        pflx = final[idx]
        pwl = swl[idx]
        pflx = np.interp(swl, pwl, savgol_filter(pflx, 3, 1, mode='nearest'))
        final = final/pflx
        writeFits( final, swl, savename=sp.replace('.fits', '.ext.fits'), 
            quiet=False, externhd=sp )

        fig, ax = plt.subplots()
        ax.plot(swl, final)
        ax.set_ylim([0, 3])
        plt.savefig(sp.replace('.fits', ''))
        plt.close(fig)

    # if os.path.exists('tmp.txt'):
    #     os.system('rm tmp.txt')

    # spt.averagespecs(avgspecs)
