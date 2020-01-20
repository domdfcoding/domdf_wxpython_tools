#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  constants.py
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


import webcolors
import wx

# Default text settings
text_defaults = {
		"color": webcolors.name_to_hex("black"),
		"font-size": "11pt",
		"font-family": "default",
		"font-style": "normal",
		"font-weight": "normal",
		"text-decoration": "none",
		"font-face-name": ''
		}

if wx.Platform == "__WXMSW__":
	text_defaults["font-size"] = "9pt"
elif wx.Platform == "__WXGTK__":
	text_defaults["font-size"] = "11pt"
	import lsb_release
	
	if "Ubuntu" in lsb_release.get_distro_information().values():
		text_defaults["font-face-name"] = "Ubuntu"

sys_colour_lookup = {
		"SYS_COLOUR_SCROLLBAR": wx.SYS_COLOUR_SCROLLBAR,
		"SYS_COLOUR_DESKTOP": wx.SYS_COLOUR_DESKTOP,
		"SYS_COLOUR_BACKGROUND": wx.SYS_COLOUR_DESKTOP,
		"SYS_COLOUR_ACTIVECAPTION": wx.SYS_COLOUR_ACTIVECAPTION,
		"SYS_COLOUR_INACTIVECAPTION": wx.SYS_COLOUR_INACTIVECAPTION,
		"SYS_COLOUR_MENU": wx.SYS_COLOUR_MENU,
		"SYS_COLOUR_WINDOW": wx.SYS_COLOUR_WINDOW,
		"SYS_COLOUR_WINDOWFRAME": wx.SYS_COLOUR_WINDOWFRAME,
		"SYS_COLOUR_MENUTEXT": wx.SYS_COLOUR_MENUTEXT,
		"SYS_COLOUR_WINDOWTEXT": wx.SYS_COLOUR_WINDOWTEXT,
		"SYS_COLOUR_CAPTIONTEXT": wx.SYS_COLOUR_CAPTIONTEXT,
		"SYS_COLOUR_ACTIVEBORDER": wx.SYS_COLOUR_ACTIVEBORDER,
		"SYS_COLOUR_INACTIVEBORDER": wx.SYS_COLOUR_INACTIVEBORDER,
		"SYS_COLOUR_APPWORKSPACE": wx.SYS_COLOUR_APPWORKSPACE,
		"SYS_COLOUR_HIGHLIGHT": wx.SYS_COLOUR_HIGHLIGHT,
		"SYS_COLOUR_HIGHLIGHTTEXT": wx.SYS_COLOUR_HIGHLIGHTTEXT,
		"SYS_COLOUR_BTNFACE": wx.SYS_COLOUR_BTNFACE,
		"SYS_COLOUR_3DFACE": wx.SYS_COLOUR_BTNFACE,
		"SYS_COLOUR_FRAMEBK": wx.SYS_COLOUR_BTNFACE,
		"SYS_COLOUR_BTNSHADOW": wx.SYS_COLOUR_BTNSHADOW,
		"SYS_COLOUR_3DSHADOW": wx.SYS_COLOUR_BTNSHADOW,
		"SYS_COLOUR_GRAYTEXT": wx.SYS_COLOUR_GRAYTEXT,
		"SYS_COLOUR_BTNTEXT": wx.SYS_COLOUR_BTNTEXT,
		"SYS_COLOUR_INACTIVECAPTIONTEXT": wx.SYS_COLOUR_INACTIVECAPTIONTEXT,
		"SYS_COLOUR_BTNHIGHLIGHT": wx.SYS_COLOUR_BTNHIGHLIGHT,
		"SYS_COLOUR_BTNHILIGHT": wx.SYS_COLOUR_BTNHIGHLIGHT,
		"SYS_COLOUR_3DHIGHLIGHT": wx.SYS_COLOUR_BTNHIGHLIGHT,
		"SYS_COLOUR_3DHILIGHT": wx.SYS_COLOUR_BTNHIGHLIGHT,
		"SYS_COLOUR_3DDKSHADOW": wx.SYS_COLOUR_3DDKSHADOW,
		"SYS_COLOUR_3DLIGHT": wx.SYS_COLOUR_3DLIGHT,
		"SYS_COLOUR_INFOTEXT": wx.SYS_COLOUR_INFOTEXT,
		"SYS_COLOUR_INFOBK": wx.SYS_COLOUR_INFOBK,
		"SYS_COLOUR_LISTBOX": wx.SYS_COLOUR_LISTBOX,
		"SYS_COLOUR_HOTLIGHT": wx.SYS_COLOUR_HOTLIGHT,
		"SYS_COLOUR_GRADIENTACTIVECAPTION": wx.SYS_COLOUR_GRADIENTACTIVECAPTION,
		"SYS_COLOUR_GRADIENTINACTIVECAPTION": wx.SYS_COLOUR_GRADIENTINACTIVECAPTION,
		"SYS_COLOUR_MENUHILIGHT": wx.SYS_COLOUR_MENUHILIGHT,
		"SYS_COLOUR_MENUBAR": wx.SYS_COLOUR_MENUBAR,
		"SYS_COLOUR_LISTBOXTEXT": wx.SYS_COLOUR_LISTBOXTEXT,
		"SYS_COLOUR_LISTBOXHIGHLIGHTTEXT": wx.SYS_COLOUR_LISTBOXHIGHLIGHTTEXT,
		}