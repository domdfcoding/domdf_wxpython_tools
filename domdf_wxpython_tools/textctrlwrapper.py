#!/usr/bin/env python
#
#  textctrlwrapper.py
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

# TODO: Forward events

# stdlib
from typing import Tuple

# 3rd party
import wx  # type: ignore

__all__ = ["TextCtrlWrapper"]


class TextCtrlWrapper:
	"""
	Base class for wrappers around :class:`wx.TextCtrl`.

	Subclasses must set the value of :attr:`~.TextCtrlWrapper.textctrl`.
	"""

	#: The :class:`wx.TextCtrl` being wrapped.
	textctrl: wx.TextCtrl

	def AppendText(self, text: str):
		"""
		Appends the given text to the end of the text control.

		.. note::

			After the text is appended, the insertion point will be at the end of the text control.
			If this behaviour is not desired, the programmer should use GetInsertionPoint and SetInsertionPoint.

		:param text:
		"""

		return self.textctrl.AppendText(text)

	def CanCopy(self) -> bool:
		"""
		Returns :py:obj:`True` if the selection can be copied to the clipboard.
		"""

		return self.textctrl.CanCopy()

	def CanCut(self) -> bool:
		"""
		Returns :py:obj:`True` if the selection can be cut to the clipboard.
		"""

		return self.textctrl.CanCut()

	def CanPaste(self) -> bool:
		"""
		Returns :py:obj:`True` if the contents of the clipboard can be pasted into the text control.

		On some platforms (Motif, GTK) this is an approximation and
		returns :py:obj:`True` if the control is editable, :py:obj:`False` otherwise.
		"""

		return self.textctrl.CanPaste()

	def CanRedo(self) -> bool:
		"""
		Returns :py:obj:`True` if there is a redo facility available, and the last operation can be redone.
		"""

		return self.textctrl.CanRedo()

	def CanUndo(self) -> bool:
		"""
		Returns :py:obj:`True` if there is an undo facility available, and the last operation can be undone.
		"""

		return self.textctrl.CanUndo()

	def Clear(self) -> None:
		"""
		Clears the text in the control.

		Note that this function will generate a :py:obj:`wx.wxEVT_TEXT` event,
		i.e. its effect is identical to calling :meth:`SetValue('') <.TextCtrlWrapper.SetValue>`.
		"""

		self.textctrl.Clear()

	def Copy(self) -> None:
		"""
		Copies the selected text to the clipboard.
		"""

		return self.textctrl.Copy()

	def Cut(self) -> None:
		"""
		Copies the selected text to the clipboard and removes it from the control.
		"""

		return self.textctrl.Cut()

	def GetLastPosition(self):
		"""
		Returns the zero based index of the last position in the text control,
		which is equal to the number of characters in the control.

		:rtype: wx.TextPos
		"""

		return self.textctrl.GetLastPosition()

	def GetSelection(self) -> Tuple[int, int]:
		"""
		Gets the current selection span.

		If the returned values are equal, there was no selection.

		.. note::

			The indices returned may be used with the other :class:`wx.TextCtrl`
			methods but don't necessarily represent the correct indices into the string
			returned by GetValue for multiline controls under Windows (at least,)
			you should use GetStringSelection to get the selected text.
		"""

		return self.textctrl.GetSelection()

	def GetStringSelection(self) -> str:
		"""
		Returns the text currently selected in the control.

		If there is no selection, the returned string is empty.
		"""

		return self.textctrl.GetStringSelection()

	def GetValue(self) -> str:
		r"""
		Gets the contents of the control.

		.. note::

			For a multiline text control, the lines will be separated by (Unix-style) ``\n``
			characters, even under Windows where they are separated by a ``\r\n`` sequence
			in the native control.
		"""

		return self.textctrl.GetValue()

	def IsEditable(self) -> bool:
		"""
		Returns :py:obj:`True` if the controls contents may be edited by user
		(note that it always can be changed by the program).

		In other words, this functions returns :py:obj:`True` if the control
		hasn't been put in read-only mode by a previous call to :meth:`~.ClearableTextCtrl.SetEditable`.
		"""

		return self.textctrl.IsEditable()

	def IsEmpty(self) -> bool:
		"""
		Returns whether the control is currently empty.
		"""

		return self.textctrl.IsEmpty()

	def Paste(self) -> None:
		"""
		Pastes the clipboard contents into the control.
		"""

		return self.textctrl.Paste()

	def Redo(self) -> None:
		"""
		If there is a redo facility and the last operation can be redone, redoes the last operation.

		Does nothing if there is no redo facility.
		"""

		return self.textctrl.Redo()

	def Remove(self, from_: int, to_: int):
		r"""
		Removes the text starting at the first given position up to (but not including) the character at the last position.

		This function puts the current insertion point position at to as a side effect.

		:param from\_: The first position
		:param to\_: The last position
		"""

		return self.textctrl.Remove(from_, to_)

	def Replace(self, from_: int, to_: int, value) -> str:
		r"""
		Replaces the text starting at the first position up to (but not including) the character at the last position with the given text.

		This function puts the current insertion point position at to as a side effect.

		:param from\_: The first position
		:param to\_: The last position
		:param value: The value to replace the existing text with.
		"""

		return self.textctrl.Replace(from_, to_, value)

	def SelectAll(self) -> None:
		"""
		Selects all text in the control.
		"""

		return self.textctrl.SelectAll()

	def SelectNone(self) -> None:
		"""
		Deselects selected text in the control.
		"""

		return self.textctrl.SelectNone()

	def SetSelection(self, from_: int, to_: int):
		r"""
		Selects the text starting at the first position up to (but not including) the character at the last position.

		If both parameters are equal to -1 all text in the control is selected.

		Notice that the insertion point will be moved to from by this function.

		:param from\_: The first position
		:param to\_: The last position
		"""

		return self.textctrl.SetSelection(from_, to_)

	def SetValue(self, value: str):
		"""
		Sets the new text control value.

		It also marks the control as not-modified which means that :meth:`~.ClearableTextControl.IsModified`
		would return :py:obj:`False` immediately after the call to :meth:`~.ClearableTextControl.SetValue`.

		The insertion point is set to the start of the control (i.e. position 0) by this function
		unless the control value doesn't change at all, in which case the insertion point is left
		at its original position.

		.. note::

			Unlike most other functions changing the control's values, this function generates a
			:py:obj:`wx.wxEVT_TEXT` event. To avoid this you can use
			:meth:`~.ClearableTextControl.ChangeValue` instead.

		:param value: The new value to set. It may contain newline characters if the text control is multiline.
		"""

		return self.textctrl.SetValue(value)

	def Undo(self) -> None:
		"""
		If there is an undo facility, and the last operation can be undone, undoes the last operation.

		Does nothing if there is no undo facility.
		"""

		return self.textctrl.Undo()

	def WriteText(self, text: str):
		"""
		Writes the text into the text control at the current insertion position.

		:param text: Text to write to the text control
		"""

		return self.textctrl.WriteText(text)


# end of class TextCtrlWrapper
