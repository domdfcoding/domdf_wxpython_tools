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
import sys

# 3rd party
import wx  # type: ignore[import-not-found]

sys.path.append("..")

# this package
from domdf_wxpython_tools import LogCtrl


class DemoFrame(wx.Frame):
	"""
	Frame containing all the PyCrust components.
	"""

	name = "LogCtrl Demo"

	def __init__(
			self,
			parent=None,
			id=-1,
			title="LogCtrl Demo",
			pos=wx.DefaultPosition,
			size=wx.DefaultSize,
			style=wx.DEFAULT_FRAME_STYLE,
			*args,
			**kwds,
			):

		wx.Frame.__init__(self, parent, id, title, pos, size, style)

		self.log = LogCtrl(parent=self, *args, **kwds)

		self.Bind(wx.EVT_CLOSE, self.OnClose)

	def OnClose(self, _) -> None:
		"""
		Event handler for closing.
		"""

		self.log.Destroy()
		self.Destroy()


class App(wx.App):
	"""
	LogCtrl Demo application.
	"""

	def OnInit(self) -> bool:
		self.frame = DemoFrame()
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True


if __name__ == "__main__":
	app = App(0)
	app.MainLoop()
