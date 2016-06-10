#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pyhdust.phc as phc

print("# This will change the filters F# to [u,b,v,r,i] letters.")
roots = ['_F0', '_F1', '_F2', '_F3', '_F4']
newrs = ['_u', '_b', '_v', '_r', '_i']

for i in range(len(roots)):
    phc.renlist(roots[i], newrs[i])
