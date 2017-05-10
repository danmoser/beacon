#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" Program to rename the IAGPOL filters id from "_Fn" to "_f", where f is one
of the filters (u, b, v, r, i).
"""
from glob import glob
import os

__version__ = "0.9"
__author__ = "Daniel Moser"
__email__ = "dmfaes@gmail.com"


def renlist(root, newr):
    """ The routine changes each A_STR_B to A_NEW_B inside the running folder.
    """
    files = glob('*{0}*'.format(root))
    files.sort()
    for i in range(len(files)):
        os.system(
            'mv "' + files[i] + '" "' + files[i].replace(root, newr) + '"' )
        print("# " + files[i] + " renamed to: " +
              files[i].replace(root, newr) )
    return


if __name__ == '__main__':
    print("# This will change the filters F# to [u,b,v,r,i] letters.")
    roots = ['_F0', '_F1', '_F2', '_F3', '_F4']
    newrs = ['_u', '_b', '_v', '_r', '_i']

    for i in range(len(roots)):
        renlist(roots[i], newrs[i])
