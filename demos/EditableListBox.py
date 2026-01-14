#  !/usr/bin/env python
#
#  EditableListBox.py
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
import wx.adv  # type: ignore[import-untyped]

sys.path.append("..")

# this package
from domdf_wxpython_tools import EditableListBox


class DemoFrame(wx.Frame):

	def __init__(self):
		wx.Frame.__init__(
				self,
				None,
				-1,
				"Vanilla EditableListBox",
				size=(350, 350),
				style=wx.DEFAULT_FRAME_STYLE,
				)

		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self, -1)

		# Put the label above the buttons
		self.elb = EditableListBox(
				self.panel,
				-1,
				'',
				(50, 50),
				(152, 250),
				style=wx.adv.EL_DEFAULT_STYLE |
				# wx.adv.EL_NO_REORDER |
				wx.adv.EL_ALLOW_NEW | wx.adv.EL_ALLOW_EDIT | wx.adv.EL_ALLOW_DELETE,
				)

		self.elb.SetStrings([
				"Apples",
				"Pears",
				"Bananas",
				"Cherries",
				])
		self.SetFocus()

	def OnClose(self, event: wx.Event) -> None:
		"""

		:param event: The wxPython event.
		"""
		print(self.elb.GetStrings())
		event.Skip()


class DemoApp(wx.App):

	def OnInit(self) -> bool:
		self.frame = DemoFrame()
		self.frame.Show(True)

		return True


app = DemoApp(False)
app.MainLoop()
