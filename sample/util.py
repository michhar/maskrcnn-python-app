#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: util.py
Description: util module for Python sample.
"""
from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("macOSX")

from threading import Thread
import io
import operator
import os.path

from PIL import Image
import wx

try:
    import maskrcnn_detect as DD
except ImportError:
    import sys
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, ROOT_DIR)
    import maskrcnn_detect as DD

IMAGE_WILDCARD = 'Image files (*.jpg, *.png)|*.jpg; *.png'
INNER_PANEL_WIDTH = 710
MAX_IMAGE_SIZE = 1000
MAX_THUMBNAIL_SIZE = 75
STYLE = wx.SIMPLE_BORDER
ORIENTATION_TAG = 274

def scale_image(img, size=MAX_IMAGE_SIZE):
    """Scale the wx.Image."""
    width = img.GetWidth()
    height = img.GetHeight()
    if width > height:
        new_width = size
        new_height = size * height / width
    else:
        new_height = size
        new_width = size * width / height
    img = img.Scale(new_width, new_height)
    return img


def rotate_image(path):
    """Rotate the image from path and return wx.Image."""
    img = Image.open(path)
    try:
        exif = img._getexif()
        if exif[ORIENTATION_TAG] == 3:
            img = img.rotate(180, expand=True)
        elif exif[ORIENTATION_TAG] == 6:
            img = img.rotate(270, expand=True)
        elif exif[ORIENTATION_TAG] == 8:
            img = img.rotate(90, expand=True)
    except:
        pass
    return pil_image_to_wx_image(img)


def draw_bitmap_rectangle(bitmap):
    """Draw rectangle on bitmap."""
    dc = wx.MemoryDC(bitmap.bmp)
    dc.SetPen(wx.BLUE_PEN)
    dc.SetBrush(wx.TRANSPARENT_BRUSH)
    dc.SetTextBackground('black')
    dc.SetTextForeground('white')
    dc.SetBackgroundMode(wx.SOLID)
    dc.SetFont(
        wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD))
    dc.SelectObject(wx.NullBitmap)
    bitmap.bitmap.SetBitmap(bitmap.bmp)


def PIL2wx(image):
    width, height = image.size
    return wx.Bitmap.FromBuffer(width, height, image.tobytes())

def wx2PIL(bitmap):
    size = tuple(bitmap.GetSize())
    try:
        buf = size[0]*size[1]*3*"\x00"
        bitmap.CopyToBuffer(buf)
    except:
        del buf
        buf = bitmap.ConvertToImage().GetData()
    return Image.frombuffer("RGB", size, buf, "raw", "RGB", 0, 1)

def pil_image_to_wx_image(pil_image):
    """Convert from PIL image to wx image."""
    wx_image = wx.Image(pil_image.width, pil_image.height)
    wx_image.SetData(pil_image.convert("RGB").tobytes())
    return wx_image


def key_with_max_value(item):
    """Get the key with maximum value in a dict."""
    return max(item.items(), key=operator.itemgetter(1))[0]


def async_dec(func):
    """Async wrapper."""

    def wrapper(*args, **kwargs):
        """Async wrapper."""
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()

    return wrapper
