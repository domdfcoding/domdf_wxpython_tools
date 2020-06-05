#!/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  FileBrowseCtrl.py
#
#  Copyright (c) 2019-2020  Dominic Davis-Foster <dominic@davis-foster.co.uk>
#  Adapted from wx.lib.filebrowsebutton.FileBrowseButton.
#  Original header below:
# ----------------------------------------------------------------------
# Name:        FileBrowseCtrl
# Purpose:     Composite controls that provide a Browse button next to
#              either a ClearableTextCtrl or a wxComboBox.  The Browse button
#              launches a wxFileDialog and loads the result into the
#              other control.
#
# Author:      Mike Fletcher, Dominic Davis-Foster
#
# Copyright:   (c) 2000-2018 by Total Control Software
# Licence:     wxWindows license
# Tags:        phoenix-port
# ----------------------------------------------------------------------
# 12/02/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o 2.5 Compatibility changes
#
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import sys
import wx  # type: ignore

sys.path.append("..")
from domdf_wxpython_tools import ClearableTextCtrl, FileBrowseCtrlWithHistory, FileBrowseCtrl, DirBrowseCtrl


class SimpleCallback:
	def __init__(self, tag):
		self.tag = tag
	
	def __call__(self, event):
		print(self.tag, event.GetString())


class DemoFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, -1, "File entry with browse", size=(500, 260))
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
		panel = wx.Panel(self, -1)
		innerbox = wx.BoxSizer(wx.VERTICAL)
		control = ClearableTextCtrl(panel, style=wx.TAB_TRAVERSAL)
		innerbox.Add(control, 0, wx.EXPAND)
		control = FileBrowseCtrl(
				panel,
				style=wx.TAB_TRAVERSAL | wx.FD_SAVE,
				fileMask="All files (*.*)|*.*|JPEG files (*.jpeg)|*.jpeg;*.jpg"
				)
		innerbox.Add(control, 0, wx.EXPAND)
		middlecontrol = FileBrowseCtrlWithHistory(
				panel,
				labelText="With History",
				history=["c:\\temp", "c:\\tmp", "r:\\temp", "z:\\temp"],
				changeCallback=SimpleCallback("With History"),
				)
		innerbox.Add(middlecontrol, 0, wx.EXPAND)
		middlecontrol = FileBrowseCtrlWithHistory(
				panel,
				labelText="History callback",
				history=self.historyCallBack,
				changeCallback=SimpleCallback("History callback"),
				)
		innerbox.Add(middlecontrol, 0, wx.EXPAND)
		self.bottomcontrol = control = FileBrowseCtrl(
				panel,
				labelText="With Callback",
				style=wx.SUNKEN_BORDER | wx.CLIP_CHILDREN,
				changeCallback=SimpleCallback("With Callback"),
				)
		innerbox.Add(control, 0, wx.EXPAND)
		self.bottommostcontrol = control = DirBrowseCtrl(
				panel,
				labelText="Simple dir browse button",
				style=wx.SUNKEN_BORDER | wx.CLIP_CHILDREN)
		innerbox.Add(control, 0, wx.EXPAND)
		ID = wx.NewIdRef()
		innerbox.Add(wx.Button(panel, ID, "Change Label", ), 1, wx.EXPAND)
		self.Bind(wx.EVT_BUTTON, self.OnChangeLabel, id=ID)
		ID = wx.NewIdRef()
		innerbox.Add(wx.Button(panel, ID, "Change Value", ), 1, wx.EXPAND)
		self.Bind(wx.EVT_BUTTON, self.OnChangeValue, id=ID)
		panel.SetAutoLayout(True)
		panel.SetSizer(innerbox)
		self.history = {"c:\\temp": 1, "c:\\tmp": 1, "r:\\temp": 1, "z:\\temp": 1}
	
	def historyCallBack(self):
		keys = self.history.keys()
		list(keys).sort()
		return keys
	
	def OnFileNameChangedHistory(self, event):
		self.history[event.GetString()] = 1
	
	def OnCloseMe(self, event):
		self.Close(True)
	
	def OnChangeLabel(self, event):
		self.bottomcontrol.SetLabel("Label Updated")
	
	def OnChangeValue(self, event):
		self.bottomcontrol.SetValue("r:\\somewhere\\over\\the\\rainbow.htm")
	
	def OnCloseWindow(self, event):
		self.Destroy()


class DemoApp(wx.App):
	def OnInit(self):
		wx.InitAllImageHandlers()
		frame = DemoFrame(None)
		frame.Show(True)
		self.SetTopWindow(frame)
		return True


print('Creating dialog')
app = DemoApp(0)
app.MainLoop()
