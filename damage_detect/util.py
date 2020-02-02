#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: util.py
Description: Shared utilities project.
"""
from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("macOSX")

import os.path
import time
import matplotlib.pyplot as plt

import requests

import damage_detect as DD


TIME_SLEEP = 1


def get_ax(rows=1, cols=1, size=16):
    """Return a Matplotlib Axes array to be used in
    all visualizations in the notebook. Provide a
    central point to control graph sizes.
    
    Adjust the size attribute to control how big to render images
    """
    _, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
    return ax

def parse_image(image):
    """Parse the image smartly and return metadata for request.

    First check whether the image is a URL or a file path or a file-like object
    and return corresponding metadata.

    Args:
        image: A URL or a file path or a file-like object represents an image.

    Returns:
        a three-item tuple consist of HTTP headers, binary data and json data
        for POST.
    """
    if hasattr(image, 'read'):  # When image is a file-like object.
        headers = {'Content-Type': 'application/octet-stream'}
        data = image.read()
        return headers, data, None
    elif os.path.isfile(image):  # When image is a file path.
        headers = {'Content-Type': 'application/octet-stream'}
        data = open(image, 'rb').read()
        return headers, data, None
    else:  # Default treat it as a URL (string).
        headers = {'Content-Type': 'application/json'}
        json = {'url': image}
        return headers, None, json