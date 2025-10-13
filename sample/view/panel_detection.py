#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: panel_detection.py
Description: Detection Panel for Python sample.
"""

import wx
from wxasync import AsyncBind
import asyncio

import util
from view import base


class DetectionPanel(base.MyPanel):
    """Detection Panel."""

    def __init__(self, parent, weights_path):
        super(DetectionPanel, self).__init__(parent)

        self.detection_init = base.DetectionModel(weights_path, base.CLASS_NAME)

        self.vsizer = wx.BoxSizer(wx.VERTICAL)

        self.hsizer = wx.BoxSizer()
        self.hsizer.AddStretchSpacer()

        self.hvsizer = wx.BoxSizer(wx.VERTICAL)
        self.hvsizer.SetMinSize((util.INNER_PANEL_WIDTH, -1))

        label = ("To detect and mask objects in image, click the 'Choose Image' "
                 "button. You will see a shape and box surrounding every object location.")
        self.static_text = wx.StaticText(self, label=label)
        self.static_text.Wrap(util.INNER_PANEL_WIDTH)
        self.hvsizer.Add(self.static_text, 0, wx.ALL, 5)

        self.vhsizer = wx.BoxSizer()
        self.vhsizer.SetMinSize((util.INNER_PANEL_WIDTH, -1))

        self.lsizer = wx.BoxSizer(wx.VERTICAL)
        self.lsizer.SetMinSize((util.MAX_IMAGE_SIZE, -1))

        flag = wx.ALIGN_RIGHT
        self.btn = wx.Button(self, label='Choose Image')
        self.lsizer.Add(self.btn, 0, flag, 5)

        # Use AsyncBind for the asynchronous event handler
        # self.Bind(wx.EVT_BUTTON, self.OnChooseImage, self.btn)

        flag = wx.ALIGN_CENTRE_HORIZONTAL
        # Set up the place to place image element
        self.bitmap = base.MyStaticBitmap(self)
        self.lsizer.Add(self.bitmap, 0, flag, 5)

        self.vhsizer.Add(self.lsizer, 0, wx.ALIGN_LEFT)
        self.vhsizer.AddStretchSpacer()

        self.rsizer = wx.BoxSizer(wx.VERTICAL)
        self.rsizer.SetMinSize((util.MAX_IMAGE_SIZE, -1))

        style = wx.ALIGN_CENTER
        flag = wx.ALIGN_CENTRE_HORIZONTAL
        self.result = wx.StaticText(self, style=style)
        self.rsizer.Add(self.result, 0, flag, 5)

        flag = wx.ALIGN_LEFT | wx.EXPAND | wx.ALL

        self.vhsizer.Add(self.rsizer, 0, wx.EXPAND)

        self.hvsizer.Add(self.vhsizer)

        self.hsizer.Add(self.hvsizer, 0)
        self.hsizer.AddStretchSpacer()

        self.vsizer.Add(self.hsizer, 3, wx.EXPAND)

        self.log = base.MyLog(self)
        self.vsizer.Add(self.log, 1, wx.EXPAND)

        self.SetSizerAndFit(self.vsizer)

        # AsyncBind(wx.EVT_BUTTON, self.OnChooseImage, self.btn)
        AsyncBind(wx.EVT_BUTTON, self.async_detect, self.btn)

    async def OnChooseImage(self, event):
        """Choose Image."""
        dlg = wx.FileDialog(self, wildcard=util.IMAGE_WILDCARD)
        if dlg.ShowModal() != wx.ID_OK:
            return
        path = dlg.GetPath()
        await self.async_detect(path)

    def choose_image(self):
        dlg = wx.FileDialog(self, wildcard=util.IMAGE_WILDCARD)
        if dlg.ShowModal() != wx.ID_OK:
            return
        path = dlg.GetPath()
        return path

    async def async_test(self, event):
        """Test async w/ wx"""
        self.result.SetLabel("Button clicked")
        await asyncio.sleep(1)
        self.result.SetLabel("Working")
        await asyncio.sleep(1)
        self.result.SetLabel("Completed")

    async def async_detect(self, event):
        """Async detection."""
        path = self.choose_image()
        # self.log.log('Request: Detecting {}'.format(path))
        self.result.SetLabelText('Detecting ...')
        self.btn.Disable()
        self.rsizer.Layout()
        self.vhsizer.Layout()

        # try:
        # Use the ML algo on input image, give background (BG) as a class
        res = await util.DD.detect.async_detect(path, self.detection_init.model,
            class_names=['BG', base.CLASS_NAME])
        self.result.SetLabelText('Preparing result...')
        # Read in image
        self.bitmap.set_path(res['image_file'])
        # Set the image on the StaticBitmap object for display
        util.draw_bitmap_rectangle(self.bitmap)
        self.result.SetLabelText('Done.')
        res_text = f"{res['num_objects']} object location(s) detected."
        self.result.SetLabelText(res_text)

        # log_text = 'Response: Success. Detected {} object location(s)'.format(
        #     res['num_objects'], path)
        # self.log.log(log_text)
        # text = '{} object location(s) detected.'.format(res['num_objects'])
        # self.result.SetLabelText(text)
        # except Exception as exp:
        #     self.log.log('Response: {}'.format(exp))

        self.btn.Enable()
        self.rsizer.Layout()
        self.vhsizer.Layout()
