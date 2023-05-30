#!/usr/bin/env python
#
#  FileBrowseCtrl.py
#
#  Copyright (c) 2019-2020  Dominic Davis-Foster <dominic@davis-foster.co.uk>
#  Adapted from wx.lib.filebrowsebutton.FileBrowseButton.
#  Original header below:
# ----------------------------------------------------------------------
# Name:        FileBrowseCtrl
# Purpose:     Composite controls that provide a Browse button next to
#              either a ClearableTextCtrl or a wxComboBox.  The Browse button
#              launches a wxFileDialog and loads the result into the
#              other control.
#
# Author:      Mike Fletcher, Dominic Davis-Foster
#
# Copyright:   (c) 2000-2018 by Total Control Software
# Licence:     wxWindows license
# Tags:        phoenix-port
# ----------------------------------------------------------------------
# 12/02/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o 2.5 Compatibility changes
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

# stdlib
import os
import pathlib

# 3rd party
import wx  # type: ignore
from domdf_python_tools.typing import PathLike
from wx.lib.filebrowsebutton import FileBrowseButton  # type: ignore

# this package
from domdf_wxpython_tools.clearable_textctrl import ClearableTextCtrl
from domdf_wxpython_tools.dialogs import file_dialog_wildcard
from domdf_wxpython_tools.textctrlwrapper import TextCtrlWrapper

__all__ = ["FileBrowseCtrl", "FileBrowseCtrlWithHistory", "DirBrowseCtrl"]

# ----------------------------------------------------------------------

# TODO: validate filetypes
# TODO: Change SearchCtrl cancel button to something more resembling clearing the control. DDF 08/01/2020

# TODO: Control doesn't indicate when it has focus; on GTK there should be an orange border but there isn't


class FileBrowseCtrl(TextCtrlWrapper, FileBrowseButton):
	"""
	A control to allow the user to type in a filename or browse with
	the standard file dialog to select file.

	Based on and subclassed from wx.lib.filebrowsebutton.FileBrowseButton but
	with a wx.SearchCtrl in place of the wx.TextCtrl to provide the cancel/clear
	button and with an icon on the browse button.

	:param parent:			Parent window. Should not be :py:obj:`None`.
	:param id:				Control identifier. A value of ``-1`` denotes a default value.
	:param pos:				Control position
	:param size:			Control size
	:param style:			Window style. See wx.Window and ClearableTextCtrl for supported styles
	:param labelText:		Text for label to left of text field
	:param buttonText:		Text for button which launches the file dialog
	:param toolTip:			Help text
	:param dialogTitle:		Title used in file dialog
	:param initialValue:	The initial value of the TextCtrl
	:param changeCallback:	Optional callback called for all changes in value of the control
	:param labelWidth:		Width of the label
	:param name:
	:param show_cancel_btn:	Whether to show or hide the cancel button.
	:param dialog_title:	The title of the FileDialog
	:param fileMask:		File mask (glob pattern, such as `*.*`) to use in file dialog. See wx.FileDialog for more information
	"""  # noqa: D400

	def __init__(
			self,
			parent: wx.Window,
			id: int = wx.ID_ANY,  # noqa: A002  # pylint: disable=redefined-builtin
			pos: wx.Point = wx.DefaultPosition,
			size: wx.Size = wx.DefaultSize,
			style: int = wx.TAB_TRAVERSAL | wx.FD_DEFAULT_STYLE,
			labelText: str = "File Entry:",
			buttonText: str = "Browse",
			toolTip: str = "Type a filename or click the browse button to choose a file",
			# following are the values for a file dialog box
			dialogTitle: str = "Choose a file",
			initialValue: str = '',
			# callback for when value changes (optional)
			changeCallback=lambda x: x,
			labelWidth=0,
			name="fileBrowseButton",
			show_cancel_btn: bool = True,
			fileMask: str = "All files (*.*)|*.*",
			dialog_title: str = "File Picker",
			**kwargs
			):

		# Store Variables
		self._parent = parent
		self.labelText = labelText
		self.buttonText = buttonText
		self.toolTip = toolTip
		self.dialogTitle = dialogTitle
		self.initialValue = initialValue
		self.fileMask = fileMask
		self.dialog_title = dialog_title
		self.file_dialog_kwargs = kwargs
		self.style = style
		self.changeCallback = changeCallback
		self.callCallback = True
		self.labelWidth = labelWidth
		self.show_cancel_btn = show_cancel_btn

		# create the dialog
		self.createDialog(parent, id, pos, size, style, name)
		# Setting a value causes the changeCallback to be called.
		# In this case that would be before the return of the
		# constructor. Not good. So a default value on
		# SetValue is used to disable the callback

		self.textcontrol = self.textControl
		self.SetValue(initialValue, 0)

	# self.SetMinSize((-1, 34))
	# # if size.y < 34:
	# # 	size.y = 34
	# self.SetSize(size)

	def createTextControl(self):
		"""
		Create the text control.
		"""

		# textControl = wx.TextCtrl(self, -1)
		# textControl = SearchCtrl(self, -1, style=wx.BORDER_NONE)# TODO: make this work, style=self.style)
		textControl = ClearableTextCtrl(self, -1)
		# textControl.ShowSearchButton(False)
		# textControl.SetDescriptiveText("")
		# if self.show_cancel_btn:
		# 	textControl.ShowCancelButton(self.show_cancel_btn)
		if self.toolTip:
			textControl.SetToolTip(self.toolTip)
		if self.changeCallback:
			textControl.Bind(wx.EVT_TEXT, self.OnChanged)
			textControl.Bind(wx.EVT_COMBOBOX, self.OnChanged)
		textControl.SetMinSize((-1, 29))
		# textControl.SetSize((-1, 29))

		return textControl

	def createBrowseButton(self):
		"""
		Create the browse-button control.
		"""

		# button = wx.Button(self, -1, self.buttonText)
		button = wx.BitmapButton(
				self, -1, bitmap=wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16))
				)
		# button.SetToolTip(self.toolTip)
		button.SetToolTip(self.buttonText)
		button.Bind(wx.EVT_BUTTON, self.OnBrowse)
		# button.SetMinSize((29, 29))
		# button.SetSize((29, 29))
		return button

	def OnBrowse(self, event=None):
		"""
		Going to browse for file...
		"""

		default_path: PathLike

		if self.GetValue() == '':
			default_path = pathlib.Path(self.initialValue).parent
		else:
			default_path = pathlib.Path(self.GetValue())
			if default_path.is_file():
				default_path = default_path.parent

		if not default_path.exists():
			default_path = pathlib.Path.home()

		default_path = str(default_path)

		pathname = file_dialog_wildcard(
				self,
				wildcard=self.fileMask,
				style=self.style,
				defaultDir=default_path,
				title=self.dialog_title,
				)

		if pathname:
			self.textControl.ChangeValue(pathname[0])
			self.textControl.SetFocus()

	def SetValue(self, value, callBack=1):
		"""
		Sets the new text control value.

		It also marks the control as not-modified which means that IsModified() would return :py:obj:`False` immediately after the call to SetValue .

		The insertion point is set to the start of the control (i.e. position 0) by this function unless the control value doesn't change at all, in which case the insertion point is left at its original position.

		Note that, unlike most other functions changing the controls values, this function generates a wxEVT_TEXT event. To avoid this you can use ChangeValue instead.

		Parameters:	value (string) – The new value to set. It may contain newline characters if the text control is multi-line.
		"""

		save = self.callCallback
		self.callCallback = callBack
		self.textControl.SetValue(value)
		self.textControl.SetForegroundColour(wx.BLACK)
		self.callCallback = save

	def GetLabel(self):
		"""
		Retrieve the label's current text.
		"""

		return self.label.GetLabel()

	def SetLabel(self, value):
		"""
		Set the label's current text.
		"""

		rvalue = self.label.SetLabel(value)
		self.Refresh(True)
		return rvalue

	def GetLineLength(self, lineNo: int) -> int:
		"""
		Gets the length of the specified line, not including any trailing newline character(s).

		:param lineNo: Line number (starting from zero).

		:return: The length of the line, or ``-1`` if ``lineNo`` was invalid.
		"""

		return self.textControl.GetLineLength(lineNo)

	def GetLineText(self, lineNo: int) -> str:
		"""
		Returns the contents of a given line in the text control, not including any trailing newline character(s).

		:param lineNo: Line number (starting from zero).

		:return: The contents of the line.
		"""

		return self.textControl.GetLineText(lineNo)

	def GetNumberOfLines(self) -> int:
		"""
		Returns the number of lines in the text control buffer.

		:return:
		:rtype: int
		"""

		return 1

	def IsModified(self) -> bool:
		"""
		Returns :py:obj:`True` if the text has been modified by user.

		Note that calling SetValue doesn't make the control modified.

		:return:
		:rtype: bool
		"""

		return self.textControl.IsModified()

	def IsMultiLine(self) -> bool:
		"""
		Returns :py:obj:`True` if this is a multi line edit control and :py:obj:`False` otherwise.

		:return:
		:rtype: bool
		"""

		return False

	def IsSingleLine(self) -> bool:
		"""
		Returns :py:obj:`True` if this is a single line edit control and :py:obj:`False` otherwise.

		:return:
		:rtype: bool
		"""

		return True

	def MarkDirty(self):
		"""
		Mark text as modified (dirty).

		:return:
		:rtype:
		"""

		return self.textControl.MarkDirty()

	def SetModified(self, modified: bool):
		"""
		Marks the control as being modified by the user or not.

		:param modified:
		"""

		return self.textControl.SetModified(modified)

	#
	# def AutoCompleteDirectories(self):
	# 	"""
	# 	Call this function to enable auto-completion of the text using the file
	# 	system directories.
	#
	# 	Unlike AutoCompleteFileNames which completes both file names and
	# 	directories, this function only completes the directory names.
	#
	# 	Notice that currently this function is only implemented in wxMSW port
	# 	and does nothing under the other platforms.
	#
	# 	:return: :py:obj:`True` if the auto-completion was enabled or :py:obj:`False` if the
	# 	operation failed, typically because auto-completion is not supported
	# 	by the current platform.
	# 	:rtype: bool
	# 	"""
	#
	# 	return self.textControl.AutoCompleteDirectories()
	#
	# def AutoCompleteFileNames(self):
	# 	"""
	# 	Call this function to enable auto-completion of the text typed in a
	# 	single-line text control using all valid file system paths.
	#
	# 	Notice that currently this function is only implemented in wxMSW port
	# 	and does nothing under the other platforms.
	#
	# 	:return: :py:obj:`True` if the auto-completion was enabled or :py:obj:`False` if the
	# 	operation failed, typically because auto-completion is not supported
	# 	by the current platform.
	# 	:rtype: bool
	# 	"""
	#
	# 	return self.textControl.AutoCompleteFileNames()
	#
	#

	def ChangeValue(self, value: str):
		"""
		Sets the new text control value.

		It also marks the control as not-modified which means that IsModified()
		would return :py:obj:`False` immediately after the call to ChangeValue .

		The insertion point is set to the start of the control (i.e. position 0) by this function.

		This functions does not generate the wxEVT_TEXT event but otherwise is identical to SetValue .

		:param value: The new value to set. It may contain newline characters if the text control is multi-line.
		"""

		return self.textControl.ChangeValue(value)

	def GetRange(self, from_: int, to_: int) -> str:
		r"""
		Returns the string containing the text starting in the positions
		from and up to in the control.

		The positions must have been returned by another wx.TextCtrl method.

		:param from\_:
		:param to\_:
		"""

		return self.textControl.GetRange(from_, to_)

	def IsEditable(self) -> bool:
		"""
		Returns :py:obj:`True` if the controls contents may be edited by user (note that it always can be changed by the program).

		In other words, this functions returns :py:obj:`True` if the control hasn't been put in read-only mode by a previous call to SetEditable .

		:rtype:	bool
		"""

		return True


class FileBrowseCtrlWithHistory(FileBrowseCtrl):
	"""
	with following additions:
		__init__(..., history=None)

			history -- optional list of paths for initial history drop-down
				(must be passed by name, not a positional argument)
				If history is callable it will must return a list used
				for the history drop-down

			changeCallback -- as for FileBrowseCtrl, but with a work-around
				for win32 systems which don't appear to create wx.EVT_COMBOBOX
				events properly.  There is a (slight) chance that this work-around
				will cause some systems to create two events for each Combobox
				selection. If you discover this condition, please report it!

			As for a FileBrowseCtrl.__init__ otherwise.

		GetHistoryControl()
			Return reference to the control which implements interfaces
			required for manipulating the history list.  See GetHistoryControl
			documentation for description of what that interface is.

		GetHistory()
			Return current history list

		SetHistory( value=(), selectionIndex = None )
			Set current history list, if selectionIndex is not :py:obj:`None`, select that index

		"""

	def __init__(self, *arguments, **namedarguments):
		self.history = namedarguments.get("history")
		if self.history:
			del namedarguments["history"]

		self.historyCallBack = None
		if callable(self.history):
			self.historyCallBack = self.history
			self.history = None
		name = namedarguments.get("name", "fileBrowseButtonWithHistory")
		namedarguments["name"] = name
		FileBrowseCtrl.__init__(self, *arguments, **namedarguments)

	def createTextControl(self):
		"""
		Create the text control.
		"""

		textControl = wx.ComboBox(self, -1, style=wx.CB_DROPDOWN)
		textControl.SetToolTip(self.toolTip)
		textControl.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
		if self.changeCallback:
			textControl.Bind(wx.EVT_TEXT, self.OnChanged)
			textControl.Bind(wx.EVT_COMBOBOX, self.OnChanged)
		if self.history:
			history = self.history
			self.history = None
			self.SetHistory(history, control=textControl)
		return textControl

	def GetHistoryControl(self):
		"""
		Return a pointer to the control which provides (at least)
		the following methods for manipulating the history list:

			Append( item ) -- add item
			Clear() -- clear all items
			Delete( index ) -- 0-based index to delete from list
			SetSelection( index ) -- 0-based index to select in list

		Semantics of the methods follow those for the wxComboBox control
		"""
		return self.textControl

	def SetHistory(self, value=(), selectionIndex=None, control=None):
		"""
		Set the current history list
		"""

		if control is None:
			control = self.GetHistoryControl()
		if self.history == value:
			return
		self.history = value
		# Clear history values not the selected one.
		tempValue = control.GetValue()
		# clear previous values
		control.Clear()
		control.SetValue(tempValue)
		# walk through, appending new values
		for path in value:
			control.Append(path)
		if selectionIndex is not None:
			control.SetSelection(selectionIndex)

	def GetHistory(self):
		"""
		Return the current history list
		"""

		if self.historyCallBack is not None:
			return self.historyCallBack()
		elif self.history:
			return list(self.history)
		else:
			return []

	def OnSetFocus(self, event):
		"""
		When the history scroll is selected, update the history
		"""

		if self.historyCallBack is not None:
			self.SetHistory(self.historyCallBack(), control=self.textControl)
		event.Skip()

	if wx.Platform == "__WXMSW__":

		def SetValue(self, value, callBack=1):
			"""
			Convenient setting of text control value.

			Works around limitation of :py:class:`wx.ComboBox`.
			"""

			save = self.callCallback
			self.callCallback = callBack
			self.textControl.SetValue(value)
			self.callCallback = save

			# Hack to call an event handler
			class LocalEvent:

				def __init__(self, string):
					self._string = string

				def GetString(self):
					return self._string

			if callBack == 1:
				# The callback wasn't being called when SetValue was used ??
				# So added this explicit call to it
				self.changeCallback(LocalEvent(value))


class DirBrowseCtrl(FileBrowseCtrl):

	def __init__(
			self,
			parent: wx.Window,
			id=-1,  # noqa: A002  # pylint: disable=redefined-builtin
			pos=wx.DefaultPosition,
			size=wx.DefaultSize,
			style=wx.TAB_TRAVERSAL | wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON,
			labelText="Select a directory:",
			buttonText="Browse",
			toolTip="Type directory name or browse to select",
			dialogTitle='',
			initialValue=None,
			changeCallback=None,
			name="DirBrowseCtrl"
			):

		if initialValue is None:
			initialValue = os.getcwd()

		FileBrowseCtrl.__init__(
				self,
				parent,
				id=id,
				pos=pos,
				size=size,
				style=style,
				labelText=labelText,
				buttonText=buttonText,
				toolTip=toolTip,
				dialogTitle=dialogTitle,
				initialValue=initialValue,
				# callback for when value changes (optional)
				changeCallback=changeCallback,
				name=name,
				)

	def OnBrowse(self, ev=None):

		default_path: PathLike

		if self.GetValue() == '':
			default_path = pathlib.Path(self.initialValue)
		else:
			default_path = pathlib.Path(self.GetValue())
			if default_path.is_file():
				default_path = default_path.parent

		if not default_path.exists():
			default_path = pathlib.Path.home()

		default_path = str(default_path)

		dialog = wx.DirDialog(self, message=self.dialogTitle, defaultPath=default_path, style=self.style)

		if dialog.ShowModal() == wx.ID_OK:
			self.ChangeValue(dialog.GetPath())
		dialog.Destroy()

		self.textControl.SetFocus()
