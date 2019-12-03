#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  utils.py
#
#  Copyright 2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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

import wx


def toggle(object):
	if object.IsEnabled():
		object.SetValue(not object.GetValue())
		return True
	return False


def coming_soon(msg="This feature has not been implemented yet"):
	wx.MessageBox(msg, "Coming Soon", wx.ICON_INFORMATION | wx.OK)


def collapse_label(text, collapsed=True):
	import sys
	if sys.platform == "win32":
		return f"{text} {'>>' if collapsed else '<<'}"
	else:
		return f"{'⯈' if collapsed else '⯆'} {text}"


def generate_faces():
	FACES = {'backcol': '#FFFFFF',
			 'calltipbg': '#FFFFB8',
			 'calltipfg': '#404040',
			 'size': 12,
			 'lnsize': 10,
			 'other': 'new century schoolbook',
			 'times': 'Times',
			 'mono': 'Courier',
			 'helv': 'Helvetica',
			 }
	
	if 'wxMSW' in wx.PlatformInfo:
		FACES = {**FACES,
				 'times': 'Times New Roman',
				 'mono': 'Courier New',
				 'helv': 'Arial',
				 'lucida': 'Lucida Console',
				 'other': 'Comic Sans MS',
				 'size': 10,
				 'lnsize': 8,
				 }
	
	elif 'wxGTK' in wx.PlatformInfo and ('gtk2' in wx.PlatformInfo or
										 'gtk3' in wx.PlatformInfo):
		FACES = {**FACES,
				 'times': 'Serif',
				 'mono': 'Monospace',
				 'helv': 'Sans',
				 'size': 10,
				 'lnsize': 9,
				 }
	
	elif 'wxMac' in wx.PlatformInfo:
		FACES = {**FACES,
				 'times': 'Lucida Grande',
				 'mono': 'Monaco',
				 'helv': 'Geneva',
				 }
	
	return FACES


