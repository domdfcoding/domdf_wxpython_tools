#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  imagepanel.py
"""
Multiline wx.TextCtrl that allows tabbing to the next or previous control.
"""
#
#  Copyright 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#  With help from http://wxpython-users.1045709.n5.nabble.com/Text-control-and-TAB-td2306159.html
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import wx


class TabbableTextCtrl(wx.TextCtrl):
	"""
	Multiline wx.TextCtrl that allows tabbing to the next or previous control.
	"""
	
	def __init__(
			self, parent, id=wx.ID_ANY, value='',
			pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
			validator=wx.DefaultValidator, name=wx.TextCtrlNameStr):
		"""
		:param parent: Parent window. Should not be None.
		:type parent: wx.Window
		:param id: Control identifier. A value of -1 denotes a default value.
		:type id: wx.WindowID
		:param value: Default text value.
		:type value: str
		:param pos: Text control position.
		:type pos: wx.Point
		:param size:  Text control size.
		:type size: wx.Size
		:param style: Window style. See wx.TextCtrl.
		:type style: int
		:param validator: Window validator.
		:type validator: wx.Validator
		:param name: Window name.
		:type name: str
		"""
		
		wx.TextCtrl.__init__(
				self, parent, id, value=value, pos=pos, size=size,
				style=style | wx.TE_MULTILINE | wx.TE_PROCESS_ENTER,
				validator=validator, name=name)
		
		self.Bind(wx.EVT_CHAR, self.on_char)
	
	@staticmethod
	def on_char(event):
		"""
		Event handler for key being pressed, to allow for navigating between controls with TAB
		"""
		if event.GetKeyCode() == wx.WXK_TAB:
			flags = wx.NavigationKeyEvent.IsForward
			if event.ShiftDown():
				flags = wx.NavigationKeyEvent.IsBackward
			# if event.ControlDown():
			# 	flags = wx.NavigationKeyEvent.WinChange
			event.GetEventObject().GetParent().Navigate(flags)
		else:
			event.Skip()
