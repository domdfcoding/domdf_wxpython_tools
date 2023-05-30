#!/usr/bin/env python
#
#  ClearableTextCtrl.py
"""
A TextCtrl with a button to clear its contents
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Adapted from src/generic/srchctlg.cpp
#  Part of wxWidgets, https://github.com/wxWidgets/wxWidgets
#  Copyright (c) 2006 Vince Harron.
#  Licenced under the wxWindows licence
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
from typing import List, Tuple

# 3rd party
import wx  # type: ignore

# this package
from domdf_wxpython_tools.textctrlwrapper import TextCtrlWrapper

__all__ = ["CTCWidget", "ClearButton", "ClearableTextCtrl", "clear_btn"]

# the margin between the text control and the clear button
MARGIN = 3

# arguments to wxColour::ChangeLightness() for making the search/clear
# bitmaps foreground colour, respectively
CANCEL_BITMAP_LIGHTNESS = 16  # a bit more lighter

ClearableTextCtrlNameStr = "ClearableTextCtrl"


class CTCWidget(wx.TextCtrl):
	"""
	Text control used by :class:`~.ClearableTextCtrl`.

	:param parent: The parent window.
	:param value: The initial value of the text control
	:param style: The style of the text control
	:param validator:
	"""

	def __init__(self, parent: "ClearableTextCtrl", value: str, style: int, validator):
		wx.TextCtrl.__init__(self, parent, value=value, style=style, validator=validator)
		self.parent = parent

		# Ensure that our best size is recomputed using our overridden DoGetBestSize()
		self.InvalidateBestSize()

		self.Bind(wx.EVT_TEXT, self.OnText, id=wx.ID_ANY)
		self.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnter, id=wx.ID_ANY)
		self.Bind(wx.EVT_TEXT_MAXLEN, self.OnText, id=wx.ID_ANY)

	def GetMainWindowOfCompositeControl(self) -> "ClearableTextCtrl":
		"""
		Returns the parent object.
		"""

		return self.parent

	def OnText(self, event) -> None:
		"""
		Event handler for text being entered in the control.

		:param event: The wxPython event.
		"""

		event = wx.CommandEvent(event)
		event.SetEventObject(self.parent)
		event.SetId(self.parent.GetId())

		self.parent.GetEventHandler().ProcessEvent(event)

	def OnTextEnter(self, _) -> None:
		"""
		Event handler for the :kbd:`enter` / :kbd:`return ⏎` key being pressed

		:param event: The wxPython event.
		"""

		if not self.IsEmpty():
			event = wx.CommandEvent(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.parent.GetId)
			event.SetEventObject(self.parent)
			event.SetString(self.parent.GetValue())

			self.parent.ProcessWindowEvent(event)

	"""

#ifdef __WXMSW__
	# We increase the text control height to be the same as for the controls
	# with border as this is what we actually need here because even though
	# this control itself is borderless, it's inside wxClearableTextCtrl which does
	# have the border and so should have the same height as the normal text
	# entries with border.
	#
	# This is a bit ugly and it would arguably be better to use whatever size
	# the base class version return and just centre the text vertically in
	# the search control but I failed to modify the code in LayoutControls()
	# to do this easily and as there is much in that code I don't understand
	# (notably what is the logic for buttons sizing?) I prefer to not touch it
	# at all.
	virtual wxSize DoGetBestSize() const wxOVERRIDE
	{
		const long flags = GetWindowStyleFlag()
		wxCTCWidget* const self = const_cast<wxCTCWidget*>(this)

		self.SetWindowStyleFlag((flags & ~wxBORDER_MASK) | wxBORDER_DEFAULT)
		wxSize size = wxTextCtrl::DoGetBestSize()

		# The calculation for no external borders in wxTextCtrl::DoGetSizeFromTextSize also
		# removes any padding around the value, which is wrong for this situation. So we
		# can't use wxBORDER_NONE to calculate a good height, in which case we just have to
		# assume a border in the code above and then subtract the space that would be taken up
		# by a themed border (the thin blue border and the white internal border).
		# Don't use FromDIP(4), this seems not needed.
		size.y -= 4

		self.SetWindowStyleFlag(flags)

		return size
	}
#endif # __WXMSW__"""


#: XPM button icon for clearing the text control.
clear_btn: List[bytes] = [
		b"25 19 2 1",
		b"   c None",
		b"+  c #000000",
		b"                         ",
		b"                         ",
		b"                         ",
		b"                         ",
		b"                         ",
		b"                         ",
		b"         +++++++++++++   ",
		b"        ++           +   ",
		b"       ++    +   +   +   ",
		b"      ++      + +    +   ",
		b"     ++        +     +   ",
		b"      ++      + +    +   ",
		b"       ++    +   +   +   ",
		b"        ++           +   ",
		b"         +++++++++++++   ",
		b"                         ",
		b"                         ",
		b"                         ",
		b"                         ",
		b"                         ",
		]


class ClearButton(wx.Control):
	"""
	Clear button for the :class:`~.ClearableTextCtrl`.

	:param parent: The parent window.
	:param eventType:
	:param bmp:
	"""

	def __init__(self, parent: "ClearableTextCtrl", eventType: wx.PyEventBinder, bmp: wx.Bitmap):

		wx.Control.__init__(self, parent, id=wx.ID_ANY, style=wx.NO_BORDER)
		self.parent = parent
		self.m_eventType = eventType.typeId
		self.m_bmp = bmp

		self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

		self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
		self.Bind(wx.EVT_PAINT, self.OnPaint)

	def SetBitmapLabel(self, label: wx.Bitmap) -> None:
		"""
		Set bitmap for the button.

		:param label: Bitmap to set for the button.
		"""

		self.m_bmp = label
		self.InvalidateBestSize()

	# The buttons in ClearableTextCtrl shouldn't accept focus from keyboard because
	# this would interfere with the usual TAB processing: the user expects
	# that pressing TAB in the search control should switch focus to the next
	# control and not give it to the button inside the same control.
	def AcceptsFocusFromKeyboard(self) -> bool:
		"""
		Always returns :py:obj:`False`.
		"""

		return False

	def GetMainWindowOfCompositeControl(self) -> "ClearableTextCtrl":
		"""
		Returns the parent object.
		"""

		return self.parent

	def GetBestSize(self) -> wx.Size:
		"""
		Returns the best size for the control.
		"""

		return wx.Size(self.m_bmp.GetWidth(), self.m_bmp.GetHeight())

	def OnLeftUp(self, _) -> None:
		"""
		Event Handler for left mouse button being released.
		"""

		event = wx.CommandEvent(self.m_eventType, self.parent.GetId())
		event.SetEventObject(self.parent)

		if self.m_eventType == wx.EVT_SEARCHCTRL_SEARCH_BTN.typeId:
			# it's convenient to have the string to search for directly in the
			# event instead of having to retrieve it from the control in the
			# event handler code later, so provide it here
			event.SetString(self.parent.GetValue())

		self.GetEventHandler().ProcessEvent(event)

		self.parent.SetFocus()

	def OnPaint(self, _) -> None:
		"""
		Event Handler for widget being painted.
		"""

		dc = wx.PaintDC(self)

		# Clear the background in case of a user bitmap with alpha channel
		dc.GetBrush().SetColour(self.parent.GetBackgroundColour())
		# dc.SetBrush(self.parent.GetBackgroundColour())
		dc.Clear()

		# Draw the bitmap
		dc.DrawBitmap(self.m_bmp, 0, 0, True)


class ClearableTextCtrl(TextCtrlWrapper, wx.Panel):
	"""
	TextCtrl with a button to clear its contents.

	:param parent: The parent window.
	:param id: An identifier for the control. :py:obj:`wx.ID_ANY` is taken to mean a default.
	:param value: Default text value.
	:param pos: The control position. The value :py:obj:`wx.DefaultPosition` indicates a default position,
		chosen by either the windowing system or wxWidgets, depending on platform.
	:param size: The control size. The value wx.DefaultSize indicates a default size,
		chosen by either the windowing system or wxWidgets, depending on platform.
	:param style: The window style. See :class:`wx.TextCtrl`.
	:param validator: Window validator.
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
			name: str = ClearableTextCtrlNameStr
			):

		wx.Panel.__init__(self, parent, id, pos, size, style | wx.BORDER_SUNKEN, name)

		textctrl_style = style | wx.TAB_TRAVERSAL | wx.BORDER_NONE | wx.TE_RICH2

		if wx.Platform == "__WXGTK__":
			# wx.BORDER_NONE doesn't work unless its a multiline textctrl
			textctrl_style |= wx.TE_MULTILINE | wx.TE_DONTWRAP

		self.textctrl = self.m_text = CTCWidget(self, value, textctrl_style, validator=validator)
		self.m_clearBitmap = self.default_clear_bitmap
		self.m_clearButton = ClearButton(self, wx.EVT_SEARCHCTRL_CANCEL_BTN, self.m_clearBitmap)
		self.m_clearButton.SetSize((16, 16))
		self.LayoutControls()

		self.SetBackgroundColour(self.m_text.GetBackgroundColour())
		# self.m_text.SetBackgroundColour(wx.Colour())

		self.SetInitialSize(size)
		self.SetMinSize((-1, 29))
		self.Move(pos)

		self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnClearButton, id=wx.ID_ANY)
		self.Bind(wx.EVT_SIZE, self.OnSize)

	# def Destroy(self):
	# 	self.m_text.Destroy()
	# 	self.m_clearButton.Destroy()
	# 	wx.Control.Destroy(self)

	@property
	def default_clear_bitmap(self) -> wx.Bitmap:
		"""
		Returns the default clear button bitmap for the control.
		"""

		# return Clear_Button_16.GetBitmap()
		return wx.Bitmap(clear_btn)

	def SetFont(self, font: wx.Font) -> bool:
		"""
		Sets the font for the control.

		:param font: Font to associate with this control.
			Pass ``wx.NullFont`` to reset to the default font.

		:return: :py:obj:`True` if the operation completes successfully,
			:py:obj:`False` otherwise.
		"""

		if not self.m_text.SetFont(font):
			return False

		# TODO: Recreate the bitmaps as their size may have changed.

		return True

	def SetBackgroundColour(self, colour: wx.Colour) -> bool:
		"""
		Sets the background colour of the control

		:param colour: The colour to be used as the background colour; pass :py:obj:`wx.NullColour`.
			to reset to the default colour.

		.. note::

			You may want to use ``wx.SystemSettings.GetColour`` to retrieve a
			suitable colour to use rather than setting an hard-coded one.

		:return: :py:obj:`True` if the operation completes successfully,
			:py:obj:`False` otherwise.
		"""

		if not all([self.m_text.SetBackgroundColour(colour), wx.Window.SetBackgroundColour(self, colour)]):
			return False

		# TODO: When the background changes, re-render the bitmaps so that the correct
		#  colour shows in their "transparent" area.

		return True

	def AutoComplete(self, completer: wx.TextCompleter) -> bool:
		"""
		Enable auto-completion using the provided completer object.

		The specified completer object will be used to retrieve the list of possible
		completions for the already entered text and will be deleted by :class:`wx.TextEntry`
		itself when it's not needed any longer.

		:param completer: The object to be used for generating completions if not :py:obj:`None`.
			If it is :py:obj:`None`, auto-completion is disabled. The :class:`wx.TextEntry` object
			takes ownership of this pointer and will delete it in any case
			(i.e. even if this method return :py:obj:`False`).

		:return: :py:obj:`True` if the auto-completion was enabled or :py:obj:`False`
			if the operation failed, typically because auto-completion is not supported by the current platform.
		"""

		return self.m_text.AutoComplete(completer)

	def AutoCompleteDirectories(self) -> bool:
		"""
		Call this function to enable auto-completion of the text using the file system directories.

		Unlike :meth:`~.ClearableTextCtrl.AutoCompleteFileNames`, which completes both file names and directories,
		this function only completes the directory names.

		.. note:: This function is only implemented in wxMSW port and does nothing under the other platforms.

		:return: :py:obj:`True` if the auto-completion was enabled or :py:obj:`False` if the
			operation failed, typically because auto-completion is not supported by the current platform.
		"""

		return self.m_text.AutoCompleteDirectories()

	def AutoCompleteFileNames(self) -> bool:
		"""
		Call this function to enable auto-completion of the text typed in a single-line text control
		using all valid file system paths.

		.. note:: This function is only implemented in wxMSW port and does nothing under the other platforms.

		:return: :py:obj:`True` if the auto-completion was enabled or :py:obj:`False`
			if the operation failed, typically because auto-completion is not supported by the current platform.
		"""

		return self.m_text.AutoCompleteFileNames()

	def ChangeValue(self, value: str):
		"""
		Sets the new text control value.

		It also marks the control as not-modified which means that :meth:`~.ClearableTextCtrl.IsModified`
		would return :py:obj:`False` immediately after the call to :meth:`~.ClearableTextCtrl.ChangeValue`.

		The insertion point is set to the start of the control (i.e. position 0) by this function.

		This functions does not generate the :py:obj:`wx.wxEVT_TEXT` event but otherwise is identical to
		:meth:`~.ClearableTextCtrl.SetValue`.

		:param value: The new value to set. It may contain newline characters if the text control is multiline.
		"""

		self.m_text.ChangeValue(value)

	def DiscardEdits(self) -> None:
		"""
		Resets the internal modified flag as if the current changes had been saved.
		"""

		self.m_text.DiscardEdits()

	def EmulateKeyPress(self, event: wx.KeyEvent) -> bool:
		"""
		Inserts into the control the character which would have been inserted if the given
		key event had occurred in the text control.

		The event object should be the same as the one passed to :py:obj:`wx.EVT_KEY_DOWN` handler
		previously by wxWidgets.

		.. note:: This function doesn't currently work correctly for all keys under any platform but MSW.

		:param event:

		:return: :py:obj:`True` if the event resulted in a change to the control, :py:obj:`False` otherwise.
		"""

		return self.m_text.EmulateKeyPress(event)

	def GetBestClientSize(self) -> wx.Size:
		"""
		Returns the best size for the control.
		"""

		size = self.m_text.GetBestSize()

		if self.IsClearButtonVisible():
			size.x += self.m_clearButton.GetBestSize().x + self.FromDIP(MARGIN)

		# horizontalBorder = FromDIP(1) + (size.y - size.y * 14 / 21 ) / 2
		horizontalBorder = (size.y - size.y * 14 / 21) / 2
		size.x += 2 * horizontalBorder

		return size

	def GetCompositeWindowParts(self) -> List[wx.Window]:
		"""
		Returns a list of :class:`wx.Window` objects that make up this control.
		"""

		return [self.m_text, self.m_clearButton]

	def GetDefaultStyle(self) -> wx.TextAttr:
		"""
		Returns the style currently used for new text.
		"""

		return self.m_text.GetDefaultStyle()

	def GetInsertionPoint(self) -> int:
		"""
		Returns the insertion point, or cursor, position.

		This is defined as the zero based index of the character position
		to the right of the insertion point.
		For example, if the insertion point is at the end of the single-line text control,
		it is equal to :meth:`~.ClearableTextCtrl.GetLastPosition`.
		"""

		return self.m_text.GetInsertionPoint()

	def GetLineLength(self, lineNo: int) -> int:
		"""
		Gets the length of the specified line, not including any trailing newline character(s).

		:param lineNo: Line number (starting from zero).

		:return: The length of the line, or -1 if lineNo was invalid.
		"""

		return self.m_text.GetLineLength(lineNo)

	def GetLineText(self, lineNo: int) -> str:
		"""
		Returns the contents of a given line in the text control, not including any trailing newline character(s).

		:param lineNo: Line number (starting from zero).
		"""

		return self.m_text.GetLineText(lineNo)

	# GetMargins

	# @staticmethod
	# def GetMultiplier():
	# 	"""
	# 	Icons are rendered at 3-8 times larger than necessary and downscaled for antialiasing
	#
	# 	:return:
	# 	:rtype: int
	# 	"""
	#
	# 	depth = wx.DisplayDepth()
	#
	# 	if depth >= 24:
	# 		return 8
	# 	else:
	# 		return 6

	def GetNumberOfLines(self) -> int:
		"""
		Returns the number of lines in the text control buffer.
		"""

		return 1

	def GetRange(self, from_: int, to_: int) -> str:
		r"""
		Returns the string containing the text starting in the positions from and up to to in the control.

		The positions must have been returned by another :class:`wx.TextCtrl` method.

		.. note::

			The positions in a multiline :class:`wx.TextCtrl` do not correspond to the indices in the string
			returned by GetValue because of the different new line representations ( ``CR`` or ``CR LF`` )
			and so this method should be used to obtain the correct results instead of extracting parts
			of the entire value. It may also be more efficient, especially if the control contains a lot of data.

		:param from\_:
		:param to\_:
		"""

		return self.m_text.GetRange(from_, to_)

	def GetStyle(self, position: int, style: wx.TextAttr) -> bool:
		"""
		Returns the style at this position in the text control.

		Not all platforms support this function.

		:param position:
		:param style:

		:return: :py:obj:`True` on success, :py:obj:`False` if an error occurred (this may also mean that the styles are not supported under this platform).
		"""

		return self.m_text.GetStyle(position, style)

	def HitTestPos(self, pt) -> None:
		"""
		Finds the position of the character at the specified point.

		If the return code is not :py:obj:`wx.TE_HT_UNKNOWN` the position of the character
		closest to this position is returned, otherwise the output parameter is not modified.

		.. note::

			This function is currently only implemented in Univ, wxMSW and
			wxGTK ports and always returns :py:obj:`wx.TE_HT_UNKNOWN` in the other ports.

		:param pt:

		:rtype:	wxTextCtrlHitTestResult
		"""

		return self.m_text.HitTestPos(pt)

	def HitTest(self, pt) -> wx.TextCtrlHitTestResult:
		"""
		Finds the row and column of the character at the specified point.

		If the return code is not :py:obj:`wx.TE_HT_UNKNOWN` the row and column
		of the character closest to this position are returned, otherwise the
		output parameters are not modified.

		.. note::

			This function is currently only implemented in Univ, wxMSW and
			wxGTK ports and always returns :py:obj:`wx.TE_HT_UNKNOWN` in the other ports.

		NB: pt is in device coords (not adjusted for the client area origin nor scrolling).

		:param pt:
		"""

		return self.m_text.HitTest(pt)

	def IsClearButtonVisible(self) -> bool:
		"""
		Returns the clear button's visibility state.
		"""

		return self.m_clearButton and self.m_clearButton.IsShown()

	def IsModified(self) -> bool:
		"""
		Returns whether the text has been modified by user.

		.. note:: Calling :meth:`~.ClearableTextCtrl.SetValue` doesn't make the control modified.
		"""

		return self.m_text.IsModified()

	def IsMultiLine(self) -> bool:
		"""
		Returns whether this is a multi line control.
		"""

		return self.m_text.IsMultiLine()

	def IsSingleLine(self) -> bool:
		"""
		Returns whether this is a single line control.
		"""

		return self.m_text.IsSingleLine()

	def LayoutControls(self) -> None:
		"""
		Lays out the child controls.
		"""

		if not self.m_text:
			return

		total_size = self.GetClientSize()
		overall_width = total_size.x
		overall_height = total_size.y

		text_size = self.m_text.GetBestSize()
		clear_size = self.m_clearButton.GetBestSize()
		clear_margin = MARGIN

		# make room for the clear button
		horizontalBorder = 1 + (text_size.y - text_size.y * 14 / 21) / 2

		x = 0
		textWidth = overall_width

		textWidth -= horizontalBorder

		textWidth -= +clear_size.x + clear_margin + 1
		if textWidth < 0:
			textWidth = 0

		# position the subcontrols inside the client area

		if wx.Platform == "__WXMSW__":
			# The text control is too high up on Windows; normally a text control looks OK because
			# of the white border that's part of the theme border. We can also remove a pixel from
			# the height to fit the text control in, because the padding in EDIT_HEIGHT_FROM_CHAR_HEIGHT
			# is already generous.
			textY = 1
		else:
			textY = 0

		self.m_text.SetSize(x, textY, textWidth, overall_height - textY - 10)

		text_pos = self.m_text.GetPosition()
		self.m_text.SetPosition((text_pos.x + 3, text_pos.y + 5))

		x += textWidth

		x += clear_margin
		self.m_clearButton.SetSize(x, (overall_height - clear_size.y) / 2, clear_size.x, clear_size.y)

		clear_pos = self.m_clearButton.GetPosition()
		self.m_clearButton.SetPosition((clear_pos.x, clear_pos.y))

	def MarkDirty(self) -> None:
		"""
		Mark the control as modified (dirty).
		"""

		self.m_text.MarkDirty()

	def OnClearButton(self, event: wx.CommandEvent) -> None:
		"""
		Event handler for clear button being pressed

		:param event:
		"""

		self.m_text.Clear()
		event.Skip()

	def OnSize(self, event: wx.SizeEvent) -> None:
		"""
		Event handler for the size of the control being changed.

		:param event:
		"""

		# pass
		self.LayoutControls()

	def PositionToXY(self, pos: int) -> Tuple[int, int]:
		"""
		Converts given position to a zero-based column, line number pair.

		:param pos: Position
		"""

		return self.m_text.PositionToXY(pos)

	# def RenderClearBitmap(self, x: int, y: int):
	# 	"""
	#
	# 	:param x:
	# 	:param y:
	# 	:param renderDrop:
	# 	:type renderDrop:	bool
	# 	"""
	#
	# 	bg = self.GetBackgroundColour()
	# 	fg = self.GetForegroundColour().ChangeLightness(CANCEL_BITMAP_LIGHTNESS)
	#
	# 	# begin drawing code
	# 	# image starts
	#
	# 	# total size 14x14
	# 	# force 1:1 ratio
	# 	if x > y:
	# 		# x is too big
	# 		x = y
	# 	else:
	# 		# y is too big
	# 		y = x
	#
	# 	# 14x14 circle
	# 	# cross line starts (4,4)-(10,10)
	# 	# drop (13,16)-(19,6)-(16,9)
	#
	# 	multiplier = self.GetMultiplier()
	#
	# 	multiplier = 1
	#
	# 	penWidth = multiplier * x / 14
	#
	# 	bitmap = wx.Bitmap(multiplier * x, multiplier * y)
	# 	mem = wx.MemoryDC()
	# 	mem.SelectObject(bitmap)
	#
	# 	# clear background
	# 	mem.SetBrush(wx.Brush(bg))
	# 	mem.SetPen(wx.Pen(bg))
	# 	mem.DrawRectangle(0, 0, bitmap.GetWidth(), bitmap.GetHeight())
	#
	# 	# draw drop glass
	# 	mem.SetBrush(wx.Brush(fg))
	# 	mem.SetPen(wx.Pen(fg))
	# 	radius = multiplier * x / 2
	# 	mem.DrawCircle(radius, radius, radius)
	#
	# 	# draw cross
	# 	lineStartBase = 4 * x / 14
	# 	lineLength = x - 2 * lineStartBase
	#
	# 	mem.SetPen(wx.Pen(bg))
	# 	mem.SetBrush(wx.Brush(bg))
	# 	handleCornerShift = penWidth / 2
	# 	handleCornerShift = max(handleCornerShift, 1)
	# 	handlePolygon = [
	# 			wx.Point(-handleCornerShift, +handleCornerShift),
	# 			wx.Point(+handleCornerShift, -handleCornerShift),
	# 			wx.Point(multiplier * lineLength + handleCornerShift, multiplier * lineLength - handleCornerShift),
	# 			wx.Point(multiplier * lineLength - handleCornerShift, multiplier * lineLength + handleCornerShift),
	# 			]
	# 	mem.DrawPolygon(handlePolygon, multiplier * lineStartBase, multiplier * lineStartBase)
	#
	# 	handlePolygon2 = [
	# 			wx.Point(+handleCornerShift, +handleCornerShift),
	# 			wx.Point(-handleCornerShift, -handleCornerShift),
	# 			wx.Point(multiplier * lineLength - handleCornerShift, -multiplier * lineLength - handleCornerShift),
	# 			wx.Point(multiplier * lineLength + handleCornerShift, -multiplier * lineLength + handleCornerShift),
	# 			]
	# 	mem.DrawPolygon(handlePolygon2, multiplier * lineStartBase,
	# 					multiplier * (x - lineStartBase))
	#
	# 	# Stop drawing on the bitmap before possibly calling RescaleBitmap()
	# 	# below.
	# 	mem.SelectObject(wx.NullBitmap)
	#
	# 	# ===============================================================================
	# 	# end drawing code
	# 	# ===============================================================================
	#
	# 	#if multiplier != 1:
	# 	self.RescaleBitmap(bitmap, wx.Size(x, y))
	#
	# 	return bitmap

	# @staticmethod
	# def RescaleBitmap(bmp: wx.Bitmap, sizeNeeded: wx.Size):
	# 	"""
	#
	# 	:param bmp:
	# 	:param sizeNeeded:
	# 	"""
	#
	# 	if not sizeNeeded.IsFullySpecified():
	# 		raise ValueError("New size must be given")
	#
	# 	img = bmp.ConvertToImage()
	# 	img.Rescale(sizeNeeded.x, sizeNeeded.y)
	# 	bmp = wx.Bitmap(img)

	#
	# if wx.Platform in {"__WXMSW__", "__WXOSX__"}:
	# 	newBmp.UseAlpha(bmp.HasAlpha())
	#
	# dc(newBmp)
	# scX = sizeNeeded.GetWidth() / bmp.GetWidth()
	# scY = sizeNeeded.GetHeight() / bmp.GetHeight()
	# dc.SetUserScale(scX, scY)
	# dc.DrawBitmap(bmp, 0, 0)
	#
	# bmp = newBmp

	def SetClearBitmap(self, bitmap: wx.Bitmap):
		"""
		Sets the bitmap for the clear button.

		:param bitmap:
		"""

		if bitmap.IsOk:
			self.m_clearBitmap = bitmap
			if self.m_clearButton:
				self.m_clearButton.SetBitmapLabel(self.m_clearBitmap)

	def SetDefaultStyle(self, style: wx.TextAttr) -> bool:
		"""
		Changes the default style to use for the new text which is going to be added to the control.

		This applies both to the text added programmatically using :meth:`~.ClearableTextCtrl.WriteText` or
		:meth:`~.ClearableTextCtrl.AppendText` and to the text entered by the user interactively.

		If either of the font, foreground, or background colour is not set in style,
		the values of the previous default style are used for them.
		If the previous default style didn't set them either then the global font or colours
		of the text control itself are used as fall back.

		However, if the style parameter is the default :class:`wx.TextAttr`,
		then the default style is just reset (instead of being combined with
		the new style which wouldn't change it at all).

		:param style: The style for the new text

		:return: :py:obj:`True` on success, :py:obj:`False` if an error occurred
			(this may also mean that the styles are not supported under this platform).
		"""

		return self.m_text.SetDefaultStyle(style)

	def SetEditable(self, editable: bool):
		"""
		Makes the text item editable or read-only, overriding the :py:obj:`wx.TE_READONLY` flag.

		:param editable: If :py:obj:`True`, the control should be editable.
			If :py:obj:`False`, the control should be read-only.
		"""

		self.m_text.SetEditable(editable)

	def SetInsertionPoint(self, pos: int):
		"""
		Sets the insertion point at the given position.

		:param pos: Position to set, in the range from 0 to :meth:`~.ClearableTextCtrl.GetLastPosition` inclusive.
		"""

		self.m_text.SetInsertionPoint(pos)

	def SetInsertionPointEnd(self):
		"""
		Sets the insertion point at the end of the text control.

		This is equivalent to calling :meth:`~.ClearableTextCtrl.SetInsertionPoint`
		with :meth:`~.ClearableTextCtrl.GetLastPosition` as the argument.
		"""

		self.m_text.SetInsertionPointEnd()

	# SetMargins

	def SetMaxLength(self, length: int):
		"""
		This function sets the maximum number of characters the user can enter into the control.

		In other words, it allows limiting the text value length to len not counting the terminating ``NUL`` character.

		If len is 0, the previously set max length limit, if any, is discarded,
		and the user may enter as much text as the underlying native text control widget supports
		(typically at least 32Kb).

		If the user tries to enter more characters into the text control when it is already
		filled up to the maximal length, a :py:obj:`wx.wxEVT_TEXT_MAXLEN` event is sent to
		notify the program about it (giving it the possibility to show an explanatory message, for example)
		and the extra input is discarded.

		Note that in wxGTK this function may only be used with single line text controls.

		:param length:
		"""

		self.m_text.SetMaxLength(length)

	def SetModified(self, modified: bool):
		"""
		Marks the control as being modified by the user or not.

		:param modified:
		"""

		self.m_text.SetModified(modified)

	def SetStyle(self, start: int, end: int, style: wx.TextAttr) -> bool:
		"""
		Changes the style of the given range.

		If any attribute within style is not set, the corresponding attribute from GetDefaultStyle is used.

		:param start: The start of the range to change.
		:param end: The end of the range to change.
		:param style: The new style for the range.

		:return: :py:obj:`True` on success, :py:obj:`False` if an error occurred
			(this may also mean the styles are not supported under this platform).
		"""

		return self.m_text.SetStyle(start, end, style)

	def ShowPosition(self, pos: int):
		"""
		Makes the line containing the given position visible.

		:param pos: The position that should be visible.
		"""

		self.m_text.ShowPosition(pos)

	def ShouldInheritColours(self) -> bool:
		"""
		"""

		return True

	def XYToPosition(self, x: int, y: int) -> int:
		"""
		Converts the given zero-based column and line number to a position.

		:param x: The column number
		:param y: The line number
		"""

		return self.m_text.XYToPosition(x, y)
