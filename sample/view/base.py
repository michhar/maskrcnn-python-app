#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: base.py
Description: Base components for Python sample.
"""
import time
import os
import sys

import wx

import util
from maskrcnn_detect.custom import CustomConfig
import maskrcnn_detect.model as modellib

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLASS_NAME = "balloon"
WEIGHTS_PATH = "mask_rcnn_balloon.h5"

sys.path.insert(0, ROOT_DIR)


class MyPanel(wx.Panel):
    """Base Panel."""

    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)
        colour_window = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        self.SetBackgroundColour(colour_window)


class MyStaticBitmap(MyPanel):
    """Base StaticBitmap."""

    def __init__(self, parent, bitmap=wx.NullBitmap, size=util.MAX_IMAGE_SIZE):
        super(MyStaticBitmap, self).__init__(parent)
        self.bmp = bitmap
        self.scale = 1.0
        self.bitmap = wx.StaticBitmap(self, bitmap=bitmap)
        self.size = size
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.AddStretchSpacer()
        self.sizer.Add(self.bitmap, 0, wx.EXPAND)
        self.sizer.AddStretchSpacer()
        self.SetMinSize((size, size))
        self.SetSizer(self.sizer)
        self.sizer.Layout()

    def set_path(self, path):
        """Set the image path."""
        img = util.rotate_image(path)
        width = img.GetWidth()
        img = util.scale_image(img, size=self.size)
        new_width = img.GetWidth()
        self.scale = 1.0 * new_width / width
        self.bmp = img.ConvertToBitmap()
        self.bitmap.SetBitmap(self.bmp)
        self.sizer.Layout()


class MyGridStaticBitmap(wx.Panel):
    """Base Grid StaticBitmap."""

    def __init__(self,
                 parent,
                 rows=1,
                 cols=0,
                 vgap=0,
                 hgap=0,
                 size=util.MAX_THUMBNAIL_SIZE):
        super(MyGridStaticBitmap, self).__init__(parent)
        self.sizer = wx.GridSizer(rows, cols, vgap, hgap)
        self.SetSizer(self.sizer)
        self.size = size

    def set_paths(self, paths):
        """Set the paths for the images."""
        self.sizer.Clear(True)
        for path in paths:
            bitmap = MyStaticBitmap(self, size=self.size)
            bitmap.set_path(path)
            self.sizer.Add(bitmap)
        self.SetSizerAndFit(self.sizer)
        self.sizer.Layout()


class DetectionModel:
    def __init__(self, weights_path, class_name):
        self.weights_path = weights_path
        self.class_name = class_name
        self.config = None
        self.model = None

        ## Config
        self.load_inference_config()

        ## Initialize model
        self.initialize_model()

        ## Load weights
        self.load_model_weights()

    def load_inference_config(self):
        class InferenceConfig(CustomConfig):

            # Set batch size to 1 since we'll be running inference on
            # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
            GPU_COUNT = 1
            IMAGES_PER_GPU = 1

            def __init__(self, class_name):
                super(InferenceConfig, self).__init__(class_name=class_name)

        self.config = InferenceConfig(class_name=self.class_name)

    def initialize_model(self):
        self.model = modellib.MaskRCNN(mode="inference", config=self.config,
                            model_dir=ROOT_DIR)

    def load_model_weights(self):
        self.model.load_weights(os.path.join(ROOT_DIR, self.weights_path), 
            by_name=True)


class MyLog(wx.TextCtrl):
    """The window for each scenario."""

    def __init__(self, parent):
        style = wx.TE_MULTILINE | wx.TE_READONLY
        super(MyLog, self).__init__(parent, style=style)
        colour_menu = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU)
        self.SetBackgroundColour(colour_menu)

    def log(self, msg):
        """Add log."""
        log_time = time.strftime("%H:%M:%S", time.localtime())
        msg = '[{}]: {}\n'.format(log_time, msg)
        self.WriteText(msg)


