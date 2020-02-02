#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Description: Model components for Python SDK sample.
"""
from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("macOSX")
