#!/usr/bin/env python
#
#  logctrl.py
"""
Log Control, supporting text copying and zoom.
"""
#
#  Copyright (c) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#  Based on PyCrust by Patrick K. O'Brien <pobrien@orbtech.com>
#   and https://wiki.wxpython.org/StyledTextCtrl%20Log%20Window%20Demo
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
#

# stdlib
import keyword
import os
import time
from typing import List, Optional

# 3rd party
import wx  # type: ignore
from wx import stc

# this package
from domdf_wxpython_tools.keyboard import gen_keymap
from domdf_wxpython_tools.utils import generate_faces

__all__ = ["LogCtrl"]

# IDs
ID_WRAP = wx.NewIdRef()
ID_SHOW_LINENUMBERS = wx.NewIdRef()
ID_ZOOM_IN = wx.NewIdRef()
ID_ZOOM_OUT = wx.NewIdRef()
ID_ZOOM_DEFAULT = wx.NewIdRef()
ID_ZOOM_SET = wx.NewIdRef()

# Key bindings:
# Home              Go to the beginning of the line.
# Shift+Home        Select to the beginning of the command or line.
# Shift+End         Select to the end of the line.
# End               Go to the end of the line.
# Ctrl+C            Copy selected text
# Ctrl+]            Increase font size.
# Ctrl+[            Decrease font size.
# Ctrl+=            Default font size.
# Ctrl+F            Search
# TODO: F3                Search next


class LogCtrl(stc.StyledTextCtrl):
	"""
	Log Window based on StyledTextCtrl.

	:param parent: The parent window.
	:param id: An identifier for the Log window. wx.ID_ANY is taken to mean a default.
	:param pos: The Log window position. The value ``wx.DefaultPosition`` indicates a default position, chosen by either the windowing system or wxWidgets, depending on platform.
	:param size: The Log window size. The value ::wxDefaultSize indicates a default size, chosen by either the windowing system or wxWidgets, depending on platform.
	:param style: The window style. See wxPanel.
	:param name: Window name.
	"""

	findDlg: Optional[wx.FindReplaceDialog]

	def __init__(
			self,
			parent: wx.Window,
			id: int = wx.ID_ANY,  # noqa: A002  # pylint: disable=redefined-builtin
			pos: wx.Point = wx.DefaultPosition,
			size: wx.Size = wx.DefaultSize,
			style: int = wx.CLIP_CHILDREN | wx.SUNKEN_BORDER,
			name: str = "Log"
			):

		stc.StyledTextCtrl.__init__(self, parent, id, pos, size, style, name)

		self._FACES = generate_faces()
		self._keyMap = gen_keymap()
		self._config()
		self.default_zoom = self.GetZoom()
		self._styles: List[Optional[str]] = [None] * 32
		self._free = 1

		# dispatcher.connect(receiver=self._fontsizer, signal='FontIncrease')
		# dispatcher.connect(receiver=self._fontsizer, signal='FontDecrease')
		# dispatcher.connect(receiver=self._fontsizer, signal='FontDefault')

		self.findDlg = None
		self.findData = wx.FindReplaceData()
		self.findData.SetFlags(wx.FR_DOWN)

		self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
		self.Bind(wx.EVT_FIND_CLOSE, self.OnFindClose)
		self.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
		self.Bind(wx.EVT_MENU, lambda event: self.Copy(), id=wx.ID_COPY)
		self.Bind(wx.EVT_MENU, lambda event: self.SelectAll(), id=wx.ID_SELECTALL)
		self.Bind(wx.EVT_MENU, self.OnFindText, id=wx.ID_FIND)
		# self.Bind(wx.EVT_MENU, self.OnWrap, id=ID_WRAP)
		self.Bind(wx.EVT_MENU, self.ToggleWrap, id=ID_WRAP)
		# self.Bind(wx.EVT_MENU, self.OnShowLineNumbers, id=ID_SHOW_LINENUMBERS)
		self.Bind(wx.EVT_MENU, self.ToggleLineNumbers, id=ID_SHOW_LINENUMBERS)
		self.Bind(wx.EVT_MENU, self.OnZoomIn, id=ID_ZOOM_IN)
		self.Bind(wx.EVT_MENU, self.OnZoomOut, id=ID_ZOOM_OUT)
		self.Bind(wx.EVT_MENU, self.OnZoomDefault, id=ID_ZOOM_DEFAULT)
		# TODO: Default Zoom and Set Zoom

		# Display the introductory banner information.
		self.AppendText('''Click "▶ Run Comparison" to start

Right click for options
''')
		# TODO: Make this not specific to GSMatch

		wx.CallAfter(self.ScrollToLine, 0)

	def _config(self):
		self.wrap()
		self.setDisplayLineNumbers(False)

		self.SetLexer(stc.STC_LEX_PYTHON)
		self.SetKeyWords(0, ' '.join(keyword.kwlist))

		self.setStyles(self._FACES)
		self.SetViewWhiteSpace(False)
		self.SetWrapMode(True)
		try:
			self.SetEndAtLastLine(False)
		except AttributeError:
			pass

		self.SetMargins(5, 5)

	def onKeyPress(self, event):
		"""
		Event Handler for key being pressed.
		"""

		keycode = event.GetKeyCode()
		keyname = self._keyMap.get(keycode, None)
		modifiers = ''
		for mod, ch in (
			(event.ControlDown(), "Ctrl+"),
			(event.AltDown(), "Alt+"),
			(event.ShiftDown(), "Shift+"),
			(event.MetaDown(), "Meta+"),
			):
			if mod:
				modifiers += ch

		if keyname is None:
			if 27 < keycode < 256:
				keyname = chr(keycode)
			else:
				keyname = "(%s)unknown" % keycode

		combination = modifiers + keyname

		commands = {
				"Ctrl+A": self.SelectAll,
				"Ctrl+C": self.Copy,
				"Ctrl+F": self.OnFindText,
				"UP": self.LineUp,
				"DOWN": self.LineDown,
				"RIGHT": self.CharRight,
				"LEFT": self.CharLeft,
				"Ctrl+RIGHT": self.WordRight,
				"Ctrl+LEFT": self.WordLeft,
				"END": self.LineEnd,
				"Shift+END": self.LineEndExtend,
				"HOME": self.Home,
				"Shift+HOME": self.HomeExtend,
				"PAGEDOWN": self.PageDown,
				"PAGEUP": self.PageUp,
				"Shift+PAGEDOWN": self.PageDownExtend,
				"Shift+PAGEUP": self.PageUpExtend,
				"Shift+LEFT": self.CharLeftExtend,
				"Shift+RIGHT": self.CharRightExtend,
				"Shift+UP": self.LineUpExtend,
				"Shift+DOWN": self.LineDownExtend,
				"Ctrl+Shift+LEFT": self.WordLeftExtend,
				"Ctrl+Shift+RIGHT": self.WordRightExtend,
				"Ctrl+]": self.ZoomIn,
				"Ctrl+[": self.ZoomOut,  # "ESCAPE": here we should remove focus from the widget,
				"Ctrl+W": self.ToggleWrap,
				"Ctrl+L": self.ToggleLineNumbers,
				}

		if combination in commands:
			commands[combination]()
		elif combination == "Ctrl+=":
			self.SetZoom(self.default_zoom)

		print(combination)

	def fixLineEndings(self, text):
		"""
		Return text with line endings replaced by OS-specific endings.

		:param text:
		"""

		lines = text.split('\r\n')
		for idx, line in enumerate(lines):
			chunks = line.split('\r')
			for idx, chunk in enumerate(chunks):
				chunks[idx] = os.linesep.join(chunk.split('\n'))
			lines[idx] = os.linesep.join(chunks)
		text = os.linesep.join(lines)
		return text

	def setStyles(self, faces):
		"""
		Configure font size, typeface and color for lexer.

		:param faces:
		"""

		# Default style
		self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:{mono},size:{size:d},back:{backcol}".format(**faces))

		self.StyleClearAll()
		self.SetSelForeground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
		self.SetSelBackground(True, wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

		styles = [  # Built in styles
			(stc.STC_STYLE_LINENUMBER, f"back:#C0C0C0,face:{faces}(mono)s,size:{faces}(lnsize)d"),
			(stc.STC_STYLE_CONTROLCHAR, f"face:{faces}(mono)s"),
			(stc.STC_STYLE_BRACELIGHT, "fore:#0000FF,back:#FFFF88"),
			(stc.STC_STYLE_BRACEBAD, "fore:#FF0000,back:#FFFF88"),
			# Python styles
			(stc.STC_P_DEFAULT, f"face:{faces}(mono)s"),
			(stc.STC_P_COMMENTLINE, f"fore:#007F00,face:{faces}(mono)s"),
			(stc.STC_P_NUMBER, ''),
			(stc.STC_P_STRING, f"fore:#7F007F,face:{faces}(mono)s"),
			(stc.STC_P_CHARACTER, f"fore:#7F007F,face:{faces}(mono)s"),
			# (stc.STC_P_WORD, "fore:#00007F,bold"),
			(stc.STC_P_TRIPLE, "fore:#7F0000"),
			(stc.STC_P_TRIPLEDOUBLE, "fore:#000033,back:#FFFFE8"),
			# (stc.STC_P_CLASSNAME, "fore:#0000FF,bold"),
			# (stc.STC_P_DEFNAME, "fore:#007F7F,bold"),
			(stc.STC_P_OPERATOR, ''),
			(stc.STC_P_IDENTIFIER, ''),
			(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F"),
			(stc.STC_P_STRINGEOL, f"fore:#000000,face:{faces}(mono)s,back:#E0C0E0,eolfilled"),
			]

		for style in styles:
			self.StyleSetSpec(*style)

	def getStyle(self, c: str = "black"):
		"""
		Returns a style for a given colour if one exists.

		If no style exists for the colour, make a new style.

		If we run out of styles, (only 32 allowed here) we go to the top of the list and reuse previous styles.

		:param c:
		"""

		free = self._free
		if c and isinstance(c, str):
			c = c.lower()
		else:
			c = "black"

		try:
			style = self._styles.index(c)
			return style

		except ValueError:
			style = free
			self._styles[style] = c
			self.StyleSetForeground(style, wx.NamedColour(c))

			free += 1
			if free > 31:
				free = 0
			self._free = free
			return style

	def OnZoomIn(self, *_):
		"""
		Event Handler for zooming in
		"""

		self.ZoomIn()

	def OnZoomOut(self, *_):
		"""
		Event Handler for zooming out
		"""

		self.ZoomOut()

	def OnZoomDefault(self, *_):
		"""
		Event Handler for resetting the zoom
		"""

		self.SetZoom(self.default_zoom)

	def setDisplayLineNumbers(self, state):
		self.lineNumbers = state
		if state:
			self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
			self.SetMarginWidth(1, 40)
		else:
			# Leave a small margin so the feature hidden lines marker can be seen
			self.SetMarginType(1, 0)
			self.SetMarginWidth(1, 10)

	# def OnShowLineNumbers(self, event):
	# 	print("sln")
	# 	if hasattr(self, 'lineNumbers'):
	# 		self.lineNumbers = event.IsChecked()
	# 		self.setDisplayLineNumbers(self.lineNumbers)

	def ToggleLineNumbers(self, *_):
		self.setDisplayLineNumbers(not self.lineNumbers)

	def CanCopy(self) -> bool:
		"""
		Returns :py:obj:`True` if text is selected and can be copied, :py:obj:`False` otherwise.

		:rtype: bool
		"""
		return self.GetSelectionStart() != self.GetSelectionEnd()

	def Copy(self):
		"""
		Copy the selection and place it on the clipboard.
		"""

		if self.CanCopy():
			command = self.GetSelectedText()
			data = wx.TextDataObject(command)
			self._clip(data)

	@staticmethod
	def _clip(data):
		"""
		Internal function for copying to clipboard
		"""

		if wx.TheClipboard.Open():
			wx.TheClipboard.UsePrimarySelection(False)
			wx.TheClipboard.SetData(data)
			wx.TheClipboard.Flush()
			wx.TheClipboard.Close()

	def wrap(self, wrap: bool = True):
		"""
		Set whether text is word wrapped.

		:param wrap: Whether the text should be word wrapped
		"""

		try:
			self.SetWrapMode(wrap)
		except AttributeError:
			return "Wrapping is not available in this version."

	#
	# def OnWrap(self, event):
	# 	self.SetWrapMode(event.IsChecked())

	def ToggleWrap(self, *_) -> None:
		"""
		Toggle word wrap.
		"""

		self.SetWrapMode(not self.GetWrapMode())

	def GetContextMenu(self):
		"""
		Create and return a context menu for the log.
		This is used instead of the scintilla default menu
		in order to correctly respect our immutable buffer.
		"""

		menu = wx.Menu()
		menu.Append(wx.ID_COPY, "&Copy")
		menu.Append(wx.ID_SELECTALL, "Select &All \tCtrl+A")
		menu.AppendSeparator()
		menu.Append(wx.ID_FIND, "&Find \tCtrl+F", "Search for text in the log")
		menu.Append(ID_WRAP, "&Wrap Lines\tCtrl+W", "Wrap lines at right edge", wx.ITEM_CHECK)
		menu.Append(ID_SHOW_LINENUMBERS, "&Show Line Numbers\tCtrl+L", "Show Line Numbers", wx.ITEM_CHECK)
		menu.AppendSeparator()
		menu.Append(ID_ZOOM_IN, "Zoom &In\tCtrl+]", "Zoom In")
		menu.Append(ID_ZOOM_OUT, "Zoom &Out\tCtrl+[", "Zoom Out")
		menu.Append(ID_ZOOM_DEFAULT, "&Reset Zoom\tCtrl+=", "Zoom Out")
		menu.Append(ID_ZOOM_SET, "Set &Zoom", "Zoom Out")

		menu.Check(ID_WRAP, self.GetWrapMode())
		menu.Check(ID_SHOW_LINENUMBERS, self.lineNumbers)

		return menu

	def OnContextMenu(self, _):
		"""
		vent Handler for showing the context menu
		"""

		menu = self.GetContextMenu()
		self.PopupMenu(menu)

	# Find Dialog Methods

	def GetLastPosition(self):
		return self.GetLength()

	def GetRange(self, start, end):
		return self.GetTextRange(start, end)

	def GetSelection(self):
		return self.GetAnchor(), self.GetCurrentPos()

	def ShowPosition(self, pos):
		line = self.LineFromPosition(pos)
		# self.EnsureVisible(line)
		self.GotoLine(line)

	def DoFindNext(self, findData, findDlg=None):
		backward = not (findData.GetFlags() & wx.FR_DOWN)
		matchcase = (findData.GetFlags() & wx.FR_MATCHCASE) != 0
		end = self.GetLength()
		# Changed to reflect the fact that StyledTextControl is in UTF-8 encoding
		textstring = self.GetTextRange(0, end).encode("utf-8")
		findstring = findData.GetFindString().encode("utf-8")
		if not matchcase:
			textstring = textstring.lower()
			findstring = findstring.lower()
		if backward:
			start = self.GetSelection()[0]
			loc = textstring.rfind(findstring, 0, start)
		else:
			start = self.GetSelection()[1]
			loc = textstring.find(findstring, start)

		# if it wasn't found then restart at begining
		if loc == -1 and start != 0:
			if backward:
				start = end
				loc = textstring.rfind(findstring, 0, start)
			else:
				start = 0
				loc = textstring.find(findstring, start)

		# was it still not found?
		if loc == -1:
			dlg = wx.MessageDialog(
					self,
					"Unable to find the search text.",
					"Not found!",
					wx.OK | wx.ICON_INFORMATION,
					)
			dlg.ShowModal()
			dlg.Destroy()
		if findDlg:
			if loc == -1:
				wx.CallAfter(findDlg.SetFocus)
				return
			else:
				findDlg.Close()

		# show and select the found text
		self.ShowPosition(loc)
		self.SetSelection(loc, loc + len(findstring))

	def OnFindText(self, *_):
		if self.findDlg is not None:
			return

		self.findDlg = wx.FindReplaceDialog(self, self.findData, "Find", wx.FR_NOWHOLEWORD)
		self.findDlg.Show()

	def OnFindClose(self, _):
		if self.findDlg is not None:
			self.findDlg.Destroy()
			self.findDlg = None

	# Save Methods

	def bufferHasChanged(self):
		# the log buffers can always be saved
		return True

	def bufferSave(self):

		appname = wx.GetApp().GetAppName()
		default = appname + '-' + time.strftime("%Y%m%d-%H%M.py")
		filename = wx.FileSelector(
				"Save File As",
				"Saving",
				default_filename=default,
				default_extension="py",
				wildcard="*.py",
				flags=wx.SAVE | wx.OVERWRITE_PROMPT
				)

		if not filename:
			return

		text = self.GetText()

		try:
			f = open(filename, 'w')
			f.write(text)
			f.close()
		except:  # TODO: Find error type
			d = wx.MessageDialog(self, "Error saving session", "Error", wx.OK | wx.ICON_ERROR)

			d.ShowModal()
			d.Destroy()

	def write(self, text):
		"""
		Display text in the log.

		Replace line endings with OS-specific endings.

		:param text:
		"""

		text = self.fixLineEndings(text)
		self.AddText(text)
		self.EnsureCaretVisible()

	def Append(self, text, c=None):
		"""
		Add the text to the end of the control using colour c which
		should be suitable for feeding directly to wx.NamedColour.

		:param text: ... Should be a unicode string or contain only ascii data.
		:param c:
		"""

		style = self.getStyle(c)
		lenText = len(text.encode("utf8"))
		end = self.GetLength()
		self.AppendText(text)
		self.StartStyling(end, 31)
		self.SetStyling(lenText, style)
		self.EnsureCaretVisible()

	def AppendStderr(self, text):
		"""
		Add the stderr text to the end of the control using colour "red"

		:param text: ... Should be a unicode string or contain only ascii data.
		"""

		self.Append(text, "red")
