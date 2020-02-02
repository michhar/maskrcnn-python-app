#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Description: View components for Python SDK sample.
"""

import wx
import wx.lib.agw.labelbook as LB

from wx.lib.agw.fmresources import INB_FIT_LABELTEXT
from wx.lib.agw.fmresources import INB_LEFT
from wx.lib.agw.fmresources import INB_NO_RESIZE

from view.panel_detection import DetectionPanel

TITLE = u"Image Instance Segmentation for Detecting and Masking Objects"


class MyLabelBook(LB.LabelBook):
    """LabelBook part in Main Frame."""

    def __init__(self, parent):
        agw_style = INB_LEFT | INB_FIT_LABELTEXT | INB_NO_RESIZE
        super(MyLabelBook, self).__init__(parent, agwStyle=agw_style)

        self.AddPage(wx.Panel(self), u"Select a scenario:")
        self.EnableTab(1, False)

        self.AddPage(DetectionPanel(self), u" - Detection and Masks")


class MyTitle(wx.Panel):
    """Title part in Main Frame."""

    def __init__(self, parent):
        super(MyTitle, self).__init__(parent)
        self.SetBackgroundColour('#00b294')
        self.SetMinSize((-1, 80))

        sizer = wx.BoxSizer()
        sizer.AddStretchSpacer()

        family = wx.FONTFAMILY_DEFAULT
        style = wx.FONTSTYLE_NORMAL
        weight = wx.FONTWEIGHT_NORMAL
        font = wx.Font(20, family, style, weight)
        self.text = wx.StaticText(self, label=TITLE, style=wx.ALIGN_CENTER)
        self.text.SetFont(font)
        sizer.Add(self.text, flag=wx.ALIGN_CENTER_VERTICAL)

        sizer.AddStretchSpacer()
        self.SetSizer(sizer)


class MyFrame(wx.Frame):
    """Main Frame."""

    def __init__(self, parent):
        super(MyFrame, self).__init__(parent, title=TITLE, size=(1280, 768))

        # icon_path = 'Assets/Microsoft-logo_rgb_c-gray.png'
        # self.SetIcon(wx.Icon(icon_path))

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.title = MyTitle(self)
        sizer.Add(self.title, flag=wx.EXPAND)

        self.book = MyLabelBook(self)
        sizer.Add(self.book, 1, flag=wx.EXPAND)

        status_text = (
            'This is not an official Microsoft product and images will not ' +
            'be used commercially.')
        self.status = wx.StatusBar(self)
        self.status.SetStatusText(status_text)
        sizer.Add(self.status, flag=wx.EXPAND)

        self.SetSizer(sizer)
        self.Layout()


class MyApp(wx.App):
    """The whole app."""

    def OnInit(self):
        """Show main frame."""
        frame = MyFrame(None)
        frame.Show()
        return True
