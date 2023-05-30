#  !/usr/bin/env python
#
#  tabbable_textctrl.py
"""
Multiline wx.TextCtrl that allows tabbing to the next or previous control.
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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

# stdlib
from typing import AnyStr

# 3rd party
import wx  # type: ignore

__all__ = ["TabbableTextCtrl"]


class TabbableTextCtrl(wx.TextCtrl):
	"""
	Multiline :class:`wx.TextCtrl` that allows tabbing to the next or previous control.

	:param parent: Parent window. Should not be :py:obj:`None`.
	:param id: Control identifier. A value of ``-1`` denotes a default value.
	:param value: Default text value.
	:param pos: Text control position.
	:param size: Text control size.
	:param style: Window style. See :class:`wx.TextCtrl`.
	:param validator: Window validator.
	:default validator: :py:obj:`wx.DefaultValidator`
	:param name: Window name.
	"""

	def __init__(
			self,
			parent: wx.Window,
			id: int = wx.ID_ANY,  # noqa: A002  # pylint: disable=redefined-builtin
			value: str = '',
			pos: wx.Point = wx.DefaultPosition,
			size: wx.Size = wx.DefaultSize,
			style: int = 0,
			validator: wx.Validator = wx.DefaultValidator,
			name: AnyStr = wx.TextCtrlNameStr
			):
		wx.TextCtrl.__init__(
				self,
				parent,
				id,
				value=value,
				pos=pos,
				size=size,
				style=style | wx.TE_MULTILINE | wx.TE_PROCESS_ENTER,
				validator=validator,
				name=name
				)

		self.Bind(wx.EVT_CHAR, self.on_char)

	@staticmethod
	def on_char(event) -> None:
		"""
		Event handler for key being pressed, to allow for navigating between controls with :kbd:`TAB`.
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
