#!/usr/bin/env python
#
#  validators.py
"""
Various validator classes
"""
#
#  Copyright (c) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
#  Based on the wxPython Demo.
#  Licenced under the wxWindows Library Licence, Version 3.1
#
#  CharValidator based on
#  http://wxpython-users.1045709.n5.nabble.com/best-way-to-restrict-input-to-integers-td2370605.html
#

# stdlib
import string

# 3rd party
import wx  # type: ignore

__all__ = ["ValidatorBase", "CharValidator", "FloatValidator"]


class ValidatorBase(wx.Validator):
	"""
	Base class for Validators.
	"""

	def Clone(self):
		"""
		Clones the :class:`wx.Validator`.
		"""

		return self.__class__()

	def TransferToWindow(self) -> bool:
		"""
		Transfer data from validator to window.

		The default implementation returns :py:obj:`False`, indicating that an error
		occurred. We simply return :py:obj:`True`, as we don't do any data transfer.
		"""

		return True  # Prevent wxDialog from complaining.

	def TransferFromWindow(self) -> bool:
		"""
		Transfer data from window to validator.

		The default implementation returns :py:obj:`False`, indicating that an error
		occurred.  We simply return :py:obj:`True`, as we don't do any data transfer.
		"""

		return True  # Prevent wxDialog from complaining.

	def set_warning(self) -> bool:
		"""
		Set the control's background colour to pink.
		"""

		self.GetWindow().SetBackgroundColour("pink")
		self.GetWindow().SetFocus()
		self.GetWindow().Refresh()
		return False

	def reset_ctrl(self) -> bool:
		"""
		Resets the control's background colour.
		"""

		self.GetWindow().SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
		self.GetWindow().Refresh()
		return True


class CharValidator(ValidatorBase):
	"""
	A Validator that only allows the type of characters selected to be entered.

	The possible flags are:

	* int-only - only the numbers ``0123456789`` can be entered.
	* float-only - only numbers and decimal points can be entered.
	"""

	def __init__(self, flag):
		wx.Validator.__init__(self)
		self.flag = flag
		self.Bind(wx.EVT_CHAR, self.OnChar)

		# Special allowed keys, including del, Ctrl+C, Ctrl+X and Ctrl+V
		self.special_keys = {
				wx.WXK_BACK,
				wx.WXK_TAB,
				wx.WXK_RETURN,
				wx.WXK_SHIFT,
				wx.WXK_CONTROL,
				wx.WXK_ALT,
				wx.WXK_CONTROL_C,
				wx.WXK_CONTROL_V,
				wx.WXK_CONTROL_X,
				wx.WXK_DELETE,
				}

	def Clone(self):
		"""
		Clones the :class:`~.CharValidator`.
		"""

		return self.__class__(self.flag)

	def Validate(self, win) -> bool:
		"""
		Validate the control.

		:param win:
		"""

		return True

	def OnChar(self, event) -> None:
		"""
		Event handler for text being entered in the control.

		:param event: The wxPython event.
		"""

		keycode = int(event.GetKeyCode())
		if keycode < 256:
			key = chr(keycode)

			if keycode in self.special_keys:
				event.Skip()
			if self.flag == "int-only":
				if key not in "0123456789":
					return
			elif self.flag == "float-only":
				if key == '.' and '.' in event.GetEventObject().GetValue():
					return
				if key not in "0123456789.":
					return
			elif self.flag == "no-alpha" and key in string.ascii_letters:
				return
			elif self.flag == "no-digit" and key in string.digits:
				return

		event.Skip()


class FloatValidator(CharValidator):
	"""
	A Validator that only allows numbers and decimal points to be entered.
	If a decimal point has already been entered, a second one cannot be entered.
	The argument `flag` is used to limit the number of decimal places that can be entered.
	"""

	def OnChar(self, event) -> None:
		"""
		Event handler for text being entered in the control.

		:param event: The wxPython event.
		"""

		keycode = int(event.GetKeyCode())
		if keycode < 256:
			key = chr(keycode)
			if keycode in self.special_keys:
				event.Skip()

			current_value = event.GetEventObject().GetValue()

			if key not in "0123456789.":
				return

			if '.' in current_value:
				if key == '.':
					if '.' not in event.GetEventObject().GetStringSelection():
						return

				# Current decimal places
				current_dp = len(current_value.split('.')[1])

				if current_dp == self.flag:
					# Already at maximum decimal places
					return

		event.Skip()
