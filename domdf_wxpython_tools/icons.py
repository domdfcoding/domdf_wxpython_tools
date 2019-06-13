#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  icons.py
#
#  Copyright 2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  GetStockBitmap and GetStockToolbarBitmap from
#  		https://sourceforge.net/p/wxglade/mailman/message/6475744/
#		Copyright (C) 2005 Antoine Pitrou
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

def get_toolbar_icon(icon_name, size=24):
	return wx.Bitmap(wx.ArtProvider.GetBitmap(f"wx{icon_name}", "wxART_TOOLBAR_C", wx.Size(size, size)))

def get_button_icon(icon_name, size=24):
	return wx.Bitmap(wx.ArtProvider.GetBitmap(f"wx{icon_name}", "wxART_BUTTON_C", wx.Size(size, size)))

# The following code (C) 2005 Antoine Pitrou
# https://sourceforge.net/p/wxglade/mailman/message/6475744/
_art_provider = None


def GetStockBitmap(art_id, art_client=None):
	"""
	Get a stock bitmap from its wx.ART_xxx ID
	"""
	global _art_provider
	if _art_provider is None:
		_art_provider = wx.ArtProvider()
	return _art_provider.GetBitmap(id=art_id,
								   client=art_client or wx.ART_OTHER)


def GetStockToolbarBitmap(art_id):
	return GetStockBitmap(art_id, wx.ART_TOOLBAR)


TB = GetStockToolbarBitmap
