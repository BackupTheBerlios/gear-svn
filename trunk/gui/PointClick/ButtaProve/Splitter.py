#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.4 on Fri Jul 21 14:06:50 2006

import wx

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.window_1 = wx.SplitterWindow(self, -1, style=wx.SP_3D|wx.SP_BORDER)
        self.window_1_pane_2 = wx.Panel(self.window_1, -1)
        self.window_2 = wx.SplitterWindow(self.window_1_pane_2, -1, style=wx.SP_3D|wx.SP_BORDER)
        self.window_1_pane_1 = wx.Panel(self.window_1, -1)
        self.window_2_pane_1 = wx.Panel(self.window_2, -1)
        self.window_2_pane_2 = wx.Panel(self.window_2, -1)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("frame_1")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        grid_sizer_1 = wx.GridSizer(1, 1, 0, 0)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.window_2.SplitVertically(self.window_2_pane_1, self.window_2_pane_2)
        sizer_1.Add(self.window_2, 1, wx.EXPAND, 0)
        self.window_1_pane_2.SetAutoLayout(True)
        self.window_1_pane_2.SetSizer(sizer_1)
        sizer_1.Fit(self.window_1_pane_2)
        sizer_1.SetSizeHints(self.window_1_pane_2)
        self.window_1.SplitHorizontally(self.window_1_pane_1, self.window_1_pane_2)
        grid_sizer_1.Add(self.window_1, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(grid_sizer_1)
        grid_sizer_1.Fit(self)
        grid_sizer_1.SetSizeHints(self)
        self.Layout()
        # end wxGlade

# end of class MyFrame


