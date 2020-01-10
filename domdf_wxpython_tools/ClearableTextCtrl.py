#!/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  ClearableTextCtrl.py
#
#  Copyright (c) 2020  Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Adapted from srchctlg.cpp (part of wxWidgets, https://github.com/wxWidgets/wxWidgets)
#  Copyright (c) 2006 Vince Harron.
#  Original header below:
# ///////////////////////////////////////////////////////////////////////////////
# // Name:        src/generic/srchctlg.cpp
# // Purpose:     implements wxSearchCtrl as a composite control
# // Author:      Vince Harron
# // Created:     2006-02-19
# // Copyright:   Vince Harron
# // Licence:     wxWindows licence
# ///////////////////////////////////////////////////////////////////////////////#
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
from wx.lib.embeddedimage import PyEmbeddedImage

# the margin between the text control and the clear button
MARGIN = 3

# arguments to wxColour::ChangeLightness() for making the search/clear
# bitmaps foreground colour, respectively
CANCEL_BITMAP_LIGHTNESS = 16  # a bit more lighter


ClearableTextCtrlNameStr = "ClearableTextCtrl"


class CTCWidget(wx.TextCtrl):
	def __init__(self, parent, value, style, validator):
		"""
		CTCWidget: text control used by ClearableTextCtrl
		
		:param parent:
		:type parent:  ClearableTextCtrl
		:param value:
		:type value: 	str
		:param style:
		:type style: 	int
		"""
		
		wx.TextCtrl.__init__(self, parent, value=value, style=style, validator=validator)
		self.parent = parent
		
		# Ensure that our best size is recomputed using our overridden DoGetBestSize()
		self.InvalidateBestSize()
		
		self.Bind(wx.EVT_TEXT, self.OnText, id=wx.ID_ANY)
		self.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnter, id=wx.ID_ANY)
		self.Bind(wx.EVT_TEXT_MAXLEN, self.OnText, id=wx.ID_ANY)
		
	def GetMainWindowOfCompositeControl(self):
		return self.parent
	
	# protected:
	def OnText(self, eventText):
		"""
		
		:param eventText:
		:type eventText:	wxCommandEvent
		"""
		
		event = wx.CommandEvent(eventText)
		event.SetEventObject(self.parent)
		event.SetId(self.parent.GetId())
		
		self.parent.GetEventHandler().ProcessEvent(event)
	
	def OnTextEnter(self, event):
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


class ClearButton(wx.Control):
	def __init__(self, parent, eventType, bmp):
		"""
		ClearButton: clear button used by ClearableTextCtrl
		
		:param parent:
		:type parent: ClearableTextCtrl
		:param eventType:
		:type eventType:wx.PyEventBinder
		:param bmp:
		:type bmp: wx.Bitmap
		"""
		
		wx.Control.__init__(self, parent, id=wx.ID_ANY, style=wx.NO_BORDER)
		self.parent = parent
		self.m_eventType = eventType.typeId
		self.m_bmp = bmp
		
		self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
		
		self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		
	def SetBitmapLabel(self, label):
		"""
		
		:param label:
		:type label: wx.Bitmap
		"""
		
		self.m_bmp = label
		self.InvalidateBestSize()
	
	# The buttons in ClearableTextCtrl shouldn't accept focus from keyboard because
	# this would interfere with the usual TAB processing: the user expects
	# that pressing TAB in the search control should switch focus to the next
	# control and not give it to the button inside the same control.
	def AcceptsFocusFromKeyboard(self):
		return False
	
	def GetMainWindowOfCompositeControl(self):
		return self.parent
	
	# protected:
	def GetBestSize(self):
		return wx.Size(self.m_bmp.GetWidth(), self.m_bmp.GetHeight())
	
	def OnLeftUp(self, event):
		"""
		
		:param event:
		:type event:	wx.MouseEvent
		"""
		print(self.m_eventType)
		event = wx.CommandEvent(self.m_eventType, self.parent.GetId())
		event.SetEventObject(self.parent)
		
		if self.m_eventType == wx.EVT_SEARCHCTRL_SEARCH_BTN.typeId:
			# it's convenient to have the string to search for directly in the
			# event instead of having to retrieve it from the control in the
			# event handler code later, so provide it here
			event.SetString(self.parent.GetValue())
		
		self.GetEventHandler().ProcessEvent(event)
		
		self.parent.SetFocus()
		
	def OnPaint(self, event):
		"""
		
		:param event:
		:type event:	wx.PaintEvent
		"""
		
		dc = wx.PaintDC(self)
		
		# Clear the background in case of a user bitmap with alpha channel
		dc.GetBrush().SetColour(self.parent.GetBackgroundColour())
		#dc.SetBrush(self.parent.GetBackgroundColour())
		dc.Clear()
		
		# Draw the bitmap
		dc.DrawBitmap(self.m_bmp, 0, 0, True)
		

class ClearableTextCtrl(wx.Window):
	def __init__(
			self, parent, id=wx.ID_ANY, value="", pos=wx.DefaultPosition,
			size=wx.DefaultSize, style=0, validator=wx.DefaultValidator,
			name=ClearableTextCtrlNameStr
			):
		"""
		ClearableTextCtrl creation
		
		:param parent:
		:type parent:	wx.Window
		:param id:
		:type id:		wx.WindowID
		:param value:
		:type value:	str
		:param pos:
		:type pos:		wx.Point
		:param size:
		:type size:		wx.Size
		:param style:
		:type style:	int
		:param validator:
		:type validator:wx.Validator
		:param name:
		:type name:		str
		"""
		
		wx.Window.__init__(self, parent, id, pos, size, style, name)
		
		self.m_text = CTCWidget(self, value, style, validator=validator)
		self.m_clearBitmap = self.default_clear_bitmap
		self.m_clearButton = ClearButton(self, wx.EVT_SEARCHCTRL_CANCEL_BTN, self.m_clearBitmap)

		self.LayoutControls()
		
		self.SetBackgroundColour(self.m_text.GetBackgroundColour())
		self.m_text.SetBackgroundColour(wx.Colour())
		
		self.SetInitialSize(size)
		self.Move(pos)

		self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnClearButton, id=wx.ID_ANY)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		
	# def Destroy(self):
	# 	self.m_text.Destroy()
	# 	self.m_clearButton.Destroy()
	# 	wx.Control.Destroy(self)
	
	@property
	def default_clear_bitmap(self):
		return Clear_Button_16.GetBitmap()
	
	def SetFont(self, font):
		"""
		
		:param font:
		:type font: wx.Font
		
		:return:
		:rtype: bool
		"""
		
		if not self.m_text.SetFont(font):
			return False
	
		# Recreate the bitmaps as their size may have changed.
		# TODO

		return True
	
	def SetBackgroundColour(self, colour):
		"""
		
		:type colour: wx.Colour
		
		:rtype: bool
		"""
		
		if not self.m_text.SetBackgroundColour(colour):
			return False
	
		# When the background changes, re-render the bitmaps so that the correct
		# colour shows in their "transparent" area.
		# TODO

		return True
	
	def AppendText(self, text):
		"""
		Appends the text to the end of the text control.

		.. note::  After the text is appended, the insertion point will be at the end of the text control.
		If this behaviour is not desired, the programmer should use GetInsertionPoint and SetInsertionPoint.

		:param text: Text to write to the text control.
		:type text:	str
		"""

		self.m_text.AppendText(text)
	
	def AutoComplete(self, completer):
		"""
		Enable auto-completion using the provided completer object.

		The specified completer object will be used to retrieve the list of possible completions for the already entered text and will be deleted by wx.TextEntry itself when it’s not needed any longer.
		
		:param completer: The object to be used for generating completions if not None. If it is None, auto-completion is disabled. The wx.TextEntry object takes ownership of this pointer and will delete it in any case (i.e. even if this method return False).
		:type completer: wx.TextCompleter
		
		:return: True if the auto-completion was enabled or False if the operation failed, typically because auto-completion is not supported by the current platform.
		:rtype: bool
		"""

		return self.m_text.AutoComplete(completer)
		
	def AutoCompleteDirectories(self):
		"""
		Call this function to enable auto-completion of the text using the file system directories.

		Unlike AutoCompleteFileNames which completes both file names and directories, this function only completes the directory names.
		
		Notice that currently this function is only implemented in wxMSW port and does nothing under the other platforms.
		
		:return: True if the auto-completion was enabled or False if the operation failed, typically because auto-completion is not supported by the current platform.
		:rtype: bool
		"""
	
		return self.m_text.AutoCompleteDirectories()
		
	def AutoCompleteFileNames(self):
		"""
		Call this function to enable auto-completion of the text typed in a single-line text control using all valid file system paths.

		Notice that currently this function is only implemented in wxMSW port and does nothing under the other platforms.
		
		:return: True if the auto-completion was enabled or False if the operation failed, typically because auto-completion is not supported by the current platform.
		:rtype: bool
		"""
	
		return self.m_text.AutoCompleteFileNames()
	
	def CanCopy(self):
		"""
		:return: True if the selection can be copied to the clipboard.
		:rtype:	bool
		"""
		
		return self.m_text.CanCopy()
	
	def CanCut(self):
		"""
		:return: True if the selection can be cut to the clipboard.
		:rtype:	bool
		"""
		
		return self.m_text.CanCut()
	
	def CanPaste(self):
		"""
		:return: True if the contents of the clipboard can be pasted into the text control.
		:rtype:	bool
		
		On some platforms (Motif, GTK) this is an approximation and returns True if the control is editable, False otherwise.
		"""
		
		return self.m_text.CanPaste()
	
	def CanRedo(self):
		"""
		:return: True if there is a redo facility available and the last operation can be redone.
		:rtype: bool
		"""
		
		return self.m_text.CanRedo()
	
	def CanUndo(self):
		"""
		:return: True if there is an undo facility available and the last operation can be undone.
		:rtype: bool
		"""
		
		return self.m_text.CanUndo()
	
	def ChangeValue(self, value):
		"""
		Sets the new text control value.

		It also marks the control as not-modified which means that IsModified() would return False immediately after the call to ChangeValue .
		
		The insertion point is set to the start of the control (i.e. position 0) by this function.
		
		This functions does not generate the wxEVT_TEXT event but otherwise is identical to SetValue .
		
		See User Generated Events vs Programmatically Generated Events for more information.
		
		:param value: The new value to set. It may contain newline characters if the text control is multi-line
		:type value: str
		"""
		
		self.m_text.ChangeValue(value)
	
	def Clear(self):
		"""
		Clears the text in the control.

		Note that this function will generate a wxEVT_TEXT event, i.e. its effect is identical to calling SetValue (“”).
		"""
		
		self.m_text.Clear()
	
	def Copy(self):
		"""Copies the selected text to the clipboard."""
		
		self.m_text.Copy()
	
	def Cut(self):
		"""Copies the selected text to the clipboard and removes it from the control."""
		
		self.m_text.Cut()
	
	def DiscardEdits(self):
		"""Resets the internal modified flag as if the current changes had been saved."""
		
		self.m_text.DiscardEdits()
	
	def EmulateKeyPress(self, event):
		"""
		This function inserts into the control the character which would have been inserted if the given key event had occurred in the text control.

		The event object should be the same as the one passed to EVT_KEY_DOWN handler previously by wxWidgets. Please note that this function doesn’t currently work correctly for all keys under any platform but MSW.

		:param event:
		:type event: wx.KeyEvent
		
		:return: True if the event resulted in a change to the control, False otherwise.
		:rtype: bool
		"""
		
		return self.m_text.EmulateKeyPress(event)
	
	def FromDIP(self, val):
		return val
	
	def GetBestClientSize(self):
		"""

		:return:
		:rtype:	wx.Size
		"""
		
		size = self.m_text.GetBestSize()
		
		if self.IsClearButtonVisible():
			size.x += self.m_clearButton.GetBestSize().x + self.FromDIP(MARGIN)
		
		# horizontalBorder = FromDIP(1) + (size.y - size.y * 14 / 21 ) / 2
		horizontalBorder = (size.y - size.y * 14 / 21) / 2
		size.x += 2 * horizontalBorder
		
		return size
	
	def GetCompositeWindowParts(self):
		"""

		:return:
		:rtype:	wxWindowList
		"""
		
		return [self.m_text, self.m_clearButton]
	
	def GetDefaultStyle(self):
		"""
		:return: The style currently used for the new text.
		:rtype: wx.TextAttr
		"""
		
		return self.m_text.GetDefaultStyle()
	
	def GetInsertionPoint(self):
		"""
		Returns the insertion point, or cursor, position.

		This is defined as the zero based index of the character position to the right of the insertion point. For example, if the insertion point is at the end of the single-line text control, it is equal to GetLastPosition .

		:return:
		:rtype:	int
		"""
		
		return self.m_text.GetInsertionPoint()
	
	def GetLastPosition(self):
		"""
		Returns the zero based index of the last position in the text control, which is equal to the number of characters in the control.

		:return:
		:rtype: wx.TextPos
		"""
		return self.m_text.GetLastPosition()
	
	def GetLineLength(self, lineNo):
		"""
		Gets the length of the specified line, not including any trailing newline character(s).
		
		:param lineNo: Line number (starting from zero).
		:type lineNo: int

		:return: The length of the line, or -1 if lineNo was invalid.
		:rtype:	int
		"""
		
		return self.m_text.GetLineLength(lineNo)
	
	def GetLineText(self, lineNo):
		"""
		Returns the contents of a given line in the text control, not including any trailing newline character(s).
		
		:param lineNo: Line number (starting from zero).
		:type lineNo: int

		:return: The contents of the line.
		:rtype:	str
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
	
	def GetNumberOfLines(self):
		"""
		Returns the number of lines in the text control buffer.
		
		:return:
		:rtype:	int
		"""
		
		return 1
	
	def GetRange(self, from_, to_):
		"""
		Returns the string containing the text starting in the positions from and up to to in the control.

		The positions must have been returned by another wx.TextCtrl method. Please note that the positions in a multiline wx.TextCtrl do not correspond to the indices in the string returned by GetValue because of the different new line representations ( CR or CR LF) and so this method should be used to obtain the correct results instead of extracting parts of the entire value. It may also be more efficient, especially if the control contains a lot of data.

		:param from_:
		:type from_: int
		:param to_:
		:type to_: int

		:return:
		:rtype: str
		"""
		
		return self.m_text.GetRange(from_, to_)
	
	def GetSelection(self):
		"""
		Gets the current selection span.

		If the returned values are equal, there was no selection. Please note that the indices returned may be used with the other wx.TextCtrl methods but don’t necessarily represent the correct indices into the string returned by GetValue for multiline controls under Windows (at least,) you should use GetStringSelection to get the selected text.

		:return:
		:rtype: tuple
		"""

		return self.m_text.GetSelection()
	
	def GetStringSelection(self):
		"""
		Gets the text currently selected in the control.

		If there is no selection, the returned string is empty.

		:return:
		:rtype: str
		"""
		
		return self.m_text.GetStringSelection()
	
	def GetStyle(self, position, style):
		"""
		Returns the style at this position in the text control.
		
		Not all platforms support this function.
		
		:param position:
		:type position: int
		:param style:
		:type style: wx.TextAttr

		:return: True on success, False if an error occurred (this may also mean that the styles are not supported under this platform).
		:rtype: bool
		"""
		
		return self.m_text.GetStyle(position, style)
	
	def GetValue(self):
		"""
		Gets the contents of the control.
		
		Notice that for a multiline text control, the lines will be separated by (Unix-style) \n characters, even under Windows where they are separated by a \r\n sequence in the native control.
		
		:return:
		:rtype:	str
		"""
		
		return self.m_text.GetValue()
	
	def HitTestPos(self, pt):
		"""
		Finds the position of the character at the specified point.

		If the return code is not TE_HT_UNKNOWN the position of the character closest to this position is returned, otherwise the output parameter is not modified.
		
		Please note that this function is currently only implemented in Univ, wxMSW and wxGTK ports and always returns TE_HT_UNKNOWN in the other ports.

		:param pt:
		:type pt:

		:return:
		:rtype:	wxTextCtrlHitTestResult
		"""
		
		return self.m_text.HitTestPos(pt)
	
	def HitTest(self, pt):
		"""
		Finds the row and column of the character at the specified point.

		If the return code is not TE_HT_UNKNOWN the row and column of the character closest to this position are returned, otherwise the output parameters are not modified.
		
		Please note that this function is currently only implemented in Univ, wxMSW and wxGTK ports and always returns TE_HT_UNKNOWN in the other ports.

		NB: pt is in device coords (not adjusted for the client area origin nor scrolling)

		:param pt:
		:type pt:

		:return:
		:rtype:	wxTextCtrlHitTestResult
		"""
		
		return self.m_text.HitTest(pt)
	
	def IsClearButtonVisible(self):
		"""Returns the clear button’s visibility state"""
		return self.m_clearButton and self.m_clearButton.IsShown()
	
	def IsEditable(self):
		"""
		Returns True if the controls contents may be edited by user (note that it always can be changed by the program).
		
		In other words, this functions returns True if the control hasn't been put in read-only mode by a previous call to SetEditable .
		
		:return:
		:rtype:	bool
		"""
		
		return self.m_text.IsEditable()
	
	def IsEmpty(self):
		"""
		Returns True if the control is currently empty.

		This is the same as GetValue.empty() but can be much more efficient for the multiline controls containing big amounts of text.
		
		:return:
		:rtype:	bool
		"""
		
		return self.m_text.IsEmpty()
	
	def IsModified(self):
		"""
		Returns True if the text has been modified by user.
		
		Note that calling SetValue doesn’t make the control modified.
		
		:return:
		:rtype:	bool
		"""
		
		return self.m_text.IsModified()
	
	def IsMultiLine(self):
		"""
		Returns True if this is a multi line edit control and False otherwise.
		
		:return:
		:rtype:	bool
		"""
		
		return self.m_text.IsMultiLine()
	
	def IsSingleLine(self):
		"""
		Returns True if this is a single line edit control and False otherwise.
		
		:return:
		:rtype:	bool
		"""
		
		return self.m_text.IsSingleLine()
		
	def LayoutControls(self):
		if not self.m_text:
			return
		
		sizeTotal = self.GetClientSize()
		width = sizeTotal.x
		height = sizeTotal.y
		
		sizeText = self.m_text.GetBestSize()
		sizeClear = self.m_clearButton.GetBestSize()
		clearMargin = self.FromDIP(MARGIN)
		
		# make room for the clear button
		horizontalBorder = self.FromDIP(1) + (sizeText.y - sizeText.y * 14 / 21) / 2
		
		x = 0
		textWidth = width
		
		
		textWidth -= horizontalBorder
		
		textWidth -= + sizeClear.x + clearMargin + self.FromDIP(1)
		if textWidth < 0:
			textWidth = 0
		
		# position the subcontrols inside the client area
		
		if wx.Platform == "__WXMSW__":
			# The text control is too high up on Windows; normally a text control looks OK because
			# of the white border that's part of the theme border. We can also remove a pixel from
			# the height to fit the text control in, because the padding in EDIT_HEIGHT_FROM_CHAR_HEIGHT
			# is already generous.
			textY = self.FromDIP(1)
		else:
			textY = 0
		
		self.m_text.SetSize(x, textY, textWidth, height - textY)
		x += textWidth
		
		x += clearMargin
		self.m_clearButton.SetSize(x, (height - sizeClear.y) / 2,
								   sizeClear.x, sizeClear.y)
	
	def MarkDirty(self):
		"""Mark text as modified (dirty)."""

		self.m_text.MarkDirty()
	
	def OnClearButton(self, event):
		"""
		Event handler for clear button being pressed
		
		:param event:
		:type event: wx.CommandEvent
		"""
		
		self.m_text.Clear()
		event.Skip()
	
	def OnSize(self, event):
		"""
		Event handler for the size of the control being changed
		
		:param event:
		:type event: wx.SizeEvent
		"""
		
		self.LayoutControls()
	
	def Paste(self):
		self.m_text.Paste()
		
	def PositionToXY(self, pos):
		"""
		Converts given position to a zero-based column, line number pair.

		:param pos: Position
		:type pos: int

		:return:
		:rtype: tuple
		"""
		
		return self.m_text.PositionToXY(pos)
	
	def Redo(self):
		"""
		If there is a redo facility and the last operation can be redone, redoes the last operation.
		
		Does nothing if there is no redo facility.
		"""
		
		self.m_text.Redo()
	
	def Remove(self, from_, to_):
		"""
		Removes the text starting at the first given position up to (but not including) the character at the last position.

		This function puts the current insertion point position at to as a side effect.
		
		:param from_: The first position
		:type from_:	int
		:param to_: The last position
		:type to_:	int
		"""
		
		self.m_text.Remove(from_, to_)
	
	# def RenderClearBitmap(self, x, y):
	# 	"""
	#
	# 	:param x:
	# 	:type x:	int
	# 	:param y:
	# 	:type y: 	int
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
	
	def Replace(self, from_, to_, value):
		"""
		Replaces the text starting at the first position up to (but not including) the character at the last position with the given text.

		This function puts the current insertion point position at to as a side effect.
		
		:param from_: The first position
		:type from_:	int
		:param to_: The last position
		:type to_:	int
		:param value: The value to replace the existing text with.
		:type value: str
		"""
		
		self.m_text.Replace(from_, to_, value)
	
	@staticmethod
	def RescaleBitmap(bmp, sizeNeeded):
		"""

		:param bmp:
		:type bmp: wx.Bitmap
		:param sizeNeeded:
		:type sizeNeeded: wx.Size
		"""
		
		if not sizeNeeded.IsFullySpecified():
			raise ValueError("New size must be given")
		
		img = bmp.ConvertToImage()
		img.Rescale(sizeNeeded.x, sizeNeeded.y)
		bmp = wx.Bitmap(img)
	
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
	
	def SelectAll(self):
		"""Selects all text in the control."""
		
		self.m_text.SelectAll()
		
	def SelectNone(self):
		"""Deselects selected text in the control."""
		
		self.m_text.SelectNone()
	
	def SetClearBitmap(self, bitmap):
		"""
		
		:param bitmap:
		:type bitmap:	 wxBitmap
		"""
		
		if bitmap.IsOk:
			self.m_clearBitmap = bitmap
			if self.m_clearButton:
				self.m_clearButton.SetBitmapLabel(self.m_clearBitmap)
	
	def SetDefaultStyle(self, style):
		"""
		Changes the default style to use for the new text which is going to be added to the control.
		
		This applies both to the text added programmatically using WriteText or AppendText and to the text entered by the user interactively.
		
		If either of the font, foreground, or background colour is not set in style, the values of the previous default style are used for them. If the previous default style didn’t set them neither, the global font or colours of the text control itself are used as fall back.
		
		However if the style parameter is the default wx.TextAttr, then the default style is just reset (instead of being combined with the new style which wouldn’t change it at all).
		
		:param style: The style for the new text
		:type style: wx.TextAttr

		:return: True on success, False if an error occurred (this may also mean that the styles are not supported under this platform).
		:rtype: bool
		"""
		
		return self.m_text.SetDefaultStyle(style)
	
	def SetEditable(self, editable):
		"""
		Makes the text item editable or read-only, overriding the wx.TE_READONLY flag.
		
		:param editable: If True, the control is editable. If False, the control is read-only.
		:type editable:	bool
		"""
		
		self.m_text.SetEditable(editable)
	
	def SetInsertionPoint(self, pos):
		"""
		Sets the insertion point at the given position.
		
		:param pos: Position to set, in the range from 0 to GetLastPosition inclusive.
		:type pos: int
		"""
		
		self.m_text.SetInsertionPoint(pos)
	
	def SetInsertionPointEnd(self):
		"""
		Sets the insertion point at the end of the text control.

		This is equivalent to calling wx.TextCtrl.SetInsertionPoint with wx.TextCtrl.GetLastPosition argument.
		"""
		
		self.m_text.SetInsertionPointEnd()
	
	# SetMargins
	
	def SetMaxLength(self, len):
		"""
		This function sets the maximum number of characters the user can enter into the control.
		
		In other words, it allows limiting the text value length to len not counting the terminating NUL character.
		
		If len is 0, the previously set max length limit, if any, is discarded and the user may enter as much text as the underlying native text control widget supports (typically at least 32Kb). If the user tries to enter more characters into the text control when it already is filled up to the maximal length, a wxEVT_TEXT_MAXLEN event is sent to notify the program about it (giving it the possibility to show an explanatory message, for example) and the extra input is discarded.
		
		Note that in wxGTK this function may only be used with single line text controls.

		:param len:
		:type len:	long
		"""
		
		self.m_text.SetMaxLength(len)
	
	def SetModified(self, modified):
		"""
		Marks the control as being modified by the user or not.

		:param modified:
		:type modified: bool
		"""
		
		self.m_text.SetModified(modified)
	
	def SetSelection(self, from_, to_):
		"""
		Selects the text starting at the first position up to (but not including) the character at the last position.
	
		If both parameters are equal to -1 all text in the control is selected.
		
		Notice that the insertion point will be moved to from by this function.

		:param from_: The first position
		:type from_: int
		:param to_: The last position
		:type to_: int
		"""
		
		self.m_text.SetSelection(from_, to_)
	
	def SetStyle(self, start, end, style):
		"""
		Changes the style of the given range.

		If any attribute within style is not set, the corresponding attribute from GetDefaultStyle is used.

		:param start: The start of the range to change.
		:type start: int
		:param end: The end of the range to change.
		:type end: int
		:param style: The new style for the range.
		:type style: wx.TextAttr

		:return: True on success, False if an error occurred (this may also mean that the styles are not supported under this platform).
		:rtype: bool
		"""
		
		return self.m_text.SetStyle(start, end, style)
	
	def SetValue(self, value):
		"""
		Sets the new text control value.

		It also marks the control as not-modified which means that IsModified() would return False immediately after the call to SetValue .
		
		The insertion point is set to the start of the control (i.e. position 0) by this function unless the control value doesn’t change at all, in which case the insertion point is left at its original position.
		
		Note that, unlike most other functions changing the controls values, this function generates a wxEVT_TEXT event. To avoid this you can use ChangeValue instead.

		:param value: The new value to set. It may contain newline characters if the text control is multi-line.
		:type value: str
		"""
	
		self.m_text.SetValue(value)
	
	def ShowPosition(self, pos):
		"""
		Makes the line containing the given position visible.
		
		:param pos: The position that should be visible.
		:type pos: int
		"""
		
		self.m_text.ShowPosition(pos)
	
	def ShouldInheritColours(self):
			"""
			
			:rtype: bool
			
			:return:
			:rtype:
			"""
		
			return True
	
	def Undo(self):
		"""
		If there is an undo facility and the last operation can be undone, undoes the last operation.
		
		Does nothing if there is no undo facility.
		"""
		
		self.m_text.Undo()
	
	def WriteText(self, text):
		"""
		Writes the text into the text control at the current insertion position.
		
		:param text: Text to write to the text control
		:type text: str
		"""
		
		self.m_text.WriteText(text)
	
	def XYToPosition(self, x, y):
		"""
		Converts the given zero based column and line number to a position.

		:param x: The column number
		:type x: int
		:param y: The line number
		:type y: int

		:rtype: int
		"""
		
		return self.m_text.XYToPosition(x, y)
	
	
	
if __name__ == '__main__':
	from wx.tools import img2py
	
	print(img2py.img2py("./Clear_Button_16.png", __file__, append=True))
	

#----------------------------------------------------------------------
Clear_Button_16 = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlw'
    b'SFlzAAAIJQAACCUBaAtNGQAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoA'
    b'AACwSURBVDiN3dExDgFhEAXgb9FoKJwBCSdwAzdwAKUrKEVDKzqFEygUGiqJOziAE4hGIgq/'
    b'WJu1GyWv+jNv5r038/PziFJqZQxRzJg7YvFJYIQedh+G2zijm0Y2cUEHNdRjXAUtDLB5Fgux'
    b'hgjzEO2AKyZhqIJlxkqgjxOqCdc1tkFIVoJbnkMeouA0i7mvvFZ4vt8SJNHw5RFLCYEjph4H'
    b'y/vGVAEYe9wmjYN9MPoX3AF8gB60pKn/NAAAAABJRU5ErkJggg==')

