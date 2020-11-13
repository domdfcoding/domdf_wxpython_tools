#  !/usr/bin/env python
#
#  ColourPickerDialog.py
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
import wx  # type: ignore

sys.path.append("..")

# this package
from domdf_wxpython_tools import ColourPickerDialog

app = wx.App(False)

dlg = ColourPickerDialog(None)
res = dlg.ShowModal()
if res == wx.ID_OK:
	print(dlg.colour_list)
	dlg.Destroy()
