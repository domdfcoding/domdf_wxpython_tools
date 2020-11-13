#  !/usr/bin/env python
#
#  ImagePanel.py
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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

# stdlib
import os
import sys
import tempfile
import urllib.request

# 3rd party
import wx  # type: ignore

sys.path.append("..")

# this package
from domdf_wxpython_tools import ImagePanel

with tempfile.TemporaryDirectory() as tmp:
	# Get splash image from GitHub
	urllib.request.urlretrieve(
			"https://github.com/wxWidgets/Phoenix/raw/master/demo/bitmaps/splash.png",
			os.path.join(tmp, "wxsplash.png")
			)

	class DemoFrame(wx.Frame):

		def __init__(self, parent: wx.Window, id, title, position, size):
			wx.Frame.__init__(self, parent, id, title, position, size)

			panel = ImagePanel(self, os.path.join(tmp, "wxsplash.png"))

			MainSizer = wx.BoxSizer(wx.VERTICAL)
			MainSizer.Add(panel, 4, wx.EXPAND)

			self.SetSizer(MainSizer)
			self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

		def OnCloseWindow(self, _) -> None:
			self.Destroy()

	class DemoApp(wx.App):

		def __init__(self, *args, **kwargs):
			wx.App.__init__(self, *args, **kwargs)

		def OnInit(self):
			wx.InitAllImageHandlers()
			frame = DemoFrame(None, -1, "ImagePanel Demo App", wx.DefaultPosition, (700, 700))

			self.SetTopWindow(frame)
			frame.Show()
			return True

	app = DemoApp(False)
	app.MainLoop()
