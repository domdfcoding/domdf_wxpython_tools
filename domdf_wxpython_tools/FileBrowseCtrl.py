#!/usr/bin/env python
#   -*- coding: utf-8 -*-
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
import wx
from wx.lib.filebrowsebutton import FileBrowseButton

# this package
# from . import icons
from domdf_wxpython_tools.dialogs import file_dialog_wildcard

from domdf_wxpython_tools.ClearableTextCtrl import ClearableTextCtrl

# ----------------------------------------------------------------------

# TODO: validate filetypes
# TODO: Change SearchCtrl cancel button to something more resembling clearing the control. DDF 08/01/2020

class FileBrowseCtrl(FileBrowseButton):
	"""
	A control to allow the user to type in a filename or browse with
	the standard file dialog to select file.

	Based on and subclassed from wx.lib.filebrowsebutton.FileBrowseButton but
	with a wx.SearchCtrl in place of the wx.TextCtrl to provide the cancel/clear
	button and with an icon on the browse button.
	"""
	
	def __init__(
			self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
			style=wx.TAB_TRAVERSAL | wx.FD_DEFAULT_STYLE, labelText="File Entry:", buttonText="Browse",
			toolTip="Type a filename or click the browse button to choose a file",
			# following are the values for a file dialog box
			dialogTitle="Choose a file", initialValue="",
			# callback for when value changes (optional)
			changeCallback=lambda x: x,
			labelWidth=0, name='fileBrowseButton', show_cancel_btn=True,
			fileMask="All files (*.*)|*.*",
			dialog_title="File Picker", **kwargs
			):
		"""



		:param parent:			Parent window. Should not be None.
		:type parent:			wx.Window
		:param id:				Control identifier. A value of -1 denotes a default value.
		:type id:				wx.WindowID
		:param pos:				Control position
		:type pos:				wx.Point
		:param size:			Control size
		:type size:				wx.Size
		:param style:			Window style. See wx.Window and ClearableTextCtrl for supported styles
		:type style:			int
		:param labelText:		Text for label to left of text field
		:type labelText:		str
		:param buttonText:		Text for button which launches the file dialog
		:type buttonText:		str
		:param toolTip:			Help text
		:type toolTip:			str
		:param dialogTitle:		Title used in file dialog
		:type dialogTitle:		str
		:param initialValue:	The initial value of the TextCtrl
		:type initialValue:		str
		:param changeCallback:	Optional callback called for all changes in value of the control
		:type changeCallback:
		:param labelWidth:		Width of the label
		:type labelWidth:
		:param name:
		:type name:
		:param show_cancel_btn:	Whether to show or hide the cancel button.
		:type show_cancel_btn:	Bool
		:param dialog_title:	The title of the FileDialog
		:type dialog_title:		str
		:param fileMask:		File mask (glob pattern, such as *.*) to use in file dialog. See wx.FileDialog for more information
		:type fileMask:			str
		"""
		
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
		self.SetValue(initialValue, 0)
	
	# self.SetMinSize((-1, 34))
	# # if size.y < 34:
	# # 	size.y = 34
	# self.SetSize(size)
	
	def createTextControl(self):
		"""Create the text control"""
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
		"""Create the browse-button control"""
		# button = wx.Button(self, -1, self.buttonText)
		button = wx.BitmapButton(self, -1,
								 bitmap=wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16)))
		# button.SetToolTip(self.toolTip)
		button.SetToolTip(self.buttonText)
		button.Bind(wx.EVT_BUTTON, self.OnBrowse)
		# button.SetMinSize((29, 29))
		# button.SetSize((29, 29))
		return button
	
	def OnBrowse(self, event=None):
		""" Going to browse for file... """
		
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
				self, wildcard=self.fileMask,
				style=self.style,
				defaultDir=default_path,
				title=self.dialog_title,
				)
		
		if pathname:
			self.textControl.ChangeValue(pathname[0])
			self.textControl.SetFocus()
	
	def GetValue(self):
		"""
		Gets the contents of the control.

		Notice that for a multiline text control, the lines will be separated by (Unix-style) \n characters, even under Windows where they are separated by a \r\n sequence in the native control.

		:rtype:	string
		"""
		
		return self.textControl.GetValue()
	
	def SetValue(self, value, callBack=1):
		"""
		Sets the new text control value.

		It also marks the control as not-modified which means that IsModified() would return False immediately after the call to SetValue .

		The insertion point is set to the start of the control (i.e. position 0) by this function unless the control value doesn’t change at all, in which case the insertion point is left at its original position.

		Note that, unlike most other functions changing the controls values, this function generates a wxEVT_TEXT event. To avoid this you can use ChangeValue instead.

		Parameters:	value (string) – The new value to set. It may contain newline characters if the text control is multi-line.
		"""
		
		save = self.callCallback
		self.callCallback = callBack
		self.textControl.SetValue(value)
		self.textControl.SetForegroundColour(wx.BLACK)
		self.callCallback = save
	
	def GetLabel(self):
		""" Retrieve the label's current text """
		return self.label.GetLabel()
	
	def SetLabel(self, value):
		""" Set the label's current text """
		rvalue = self.label.SetLabel(value)
		self.Refresh(True)
		return rvalue
	
	def GetLineLength(self, lineNo):
		"""
		Gets the length of the specified line, not including any trailing newline character(s).

		:param lineNo: Line number (starting from zero).
		:type lineNo: int

		:return: The length of the line, or -1 if lineNo was invalid.
		:rtype: int
		"""
		
		return self.textControl.GetLineLength(lineNo)
	
	def GetLineText(self, lineNo):
		"""
		Returns the contents of a given line in the text control, not including any trailing newline character(s).

		:param lineNo: Line number (starting from zero).
		:type lineNo: int

		:return: The contents of the line.
		:rtype: string
		"""
		
		return self.textControl.GetLineText(lineNo)
	
	def GetNumberOfLines(self):
		"""
		Returns the number of lines in the text control buffer.

		:return:
		:rtype: int
		"""
		
		return 1
	
	def IsModified(self):
		"""
		Returns True if the text has been modified by user.

		Note that calling SetValue doesn’t make the control modified.

		:return:
		:rtype: bool
		"""
		
		return self.textControl.IsModified()
	
	def IsMultiLine(self):
		"""
		Returns True if this is a multi line edit control and False otherwise.

		:return:
		:rtype: bool
		"""
		
		return False
	
	def IsSingleLine(self):
		"""
		Returns True if this is a single line edit control and False otherwise.

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
	
	def SetModified(self, modified):
		"""
		Marks the control as being modified by the user or not.

		:param modified:
		:type modified: bool

		:return:
		:rtype:
		"""
		
		return self.textControl.SetModified(modified)
	
	def AppendText(self, text):
		"""
		Appends the text to the end of the text control.

		:param text: Text to write to the text control
		:type text: string
		"""
		return self.textControl.AppendText(text)
	
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
	# 	:return: True if the auto-completion was enabled or False if the
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
	# 	:return: True if the auto-completion was enabled or False if the
	# 	operation failed, typically because auto-completion is not supported
	# 	by the current platform.
	# 	:rtype: bool
	# 	"""
	#
	# 	return self.textControl.AutoCompleteFileNames()
	#
	#
	def CanCopy(self):
		"""
		Returns True if the selection can be copied to the clipboard.

		:rtype: bool
		"""
		
		return self.textControl.CanCopy()
	
	def CanCut(self):
		"""
		Returns True if the selection can be cut to the clipboard.

		:rtype: bool
		"""
		
		return self.textControl.CanCut()
	
	def CanPaste(self):
		"""
		Returns True if the contents of the clipboard can be pasted into the text control.

		On some platforms (Motif, GTK) this is an approximation and returns True if the control is editable, False otherwise.

		:rtype: bool
		"""
		
		return self.textControl.CanPaste()
	
	def CanRedo(self):
		"""
		Returns True if there is a redo facility available and the last operation can be redone.

		:rtype: bool
		"""
		
		return self.textControl.CanRedo()
	
	def CanUndo(self):
		"""
		Returns True if there is an undo facility available and the last operation can be undone.

		:rtype:	bool
		"""
		
		return self.textControl.CanUndo()
	
	def ChangeValue(self, value):
		"""
		Sets the new text control value.

		It also marks the control as not-modified which means that IsModified()
		would return False immediately after the call to ChangeValue .

		The insertion point is set to the start of the control (i.e. position 0) by this function.

		This functions does not generate the wxEVT_TEXT event but otherwise is identical to SetValue .

		:param value: The new value to set. It may contain newline characters if the text control is multi-line.
		:type value: str

		:return:
		:rtype:
		"""
		
		return self.textControl.ChangeValue(value)
	
	def Clear(self):
		"""
		Clears the text in the control.

		Note that this function will generate a wxEVT_TEXT event, i.e. its effect is identical to calling SetValue (“”).
		"""
		self.textControl.Clear()
	
	def Copy(self):
		"""
		Copies the selected text to the clipboard.
		"""
		
		return self.textControl.Copy()
	
	def Cut(self):
		"""
		Copies the selected text to the clipboard and removes it from the control.
		"""
		
		return self.textControl.Cut()
	
	def GetLastPosition(self):
		"""
		Returns the zero based index of the last position in the text control, which is equal to the number of characters in the control.

		:rtype:	wx.TextPos
		"""
		
		return self.textControl.GetLastPosition()
	
	def GetRange(self, from_, to_):
		"""
		Returns the string containing the text starting in the positions
		from and up to to in the control.

		The positions must have been returned by another wx.TextCtrl method.

		:param from_:
		:type from_: int
		:param to_:
		:type to_: int

		:return:
		:rtype: str
		"""
		
		return self.textControl.GetRange(from_, to_)
	
	def GetSelection(self):
		"""
		Gets the current selection span.

		If the returned values are equal, there was no selection. Please note
		that the indices returned may be used with the other wx.TextCtrl methods
		but don’t necessarily represent the correct indices into the string
		returned by GetValue.

		:return:
		:rtype: tuple
		"""
		
		return self.textControl.GetSelection()
	
	def GetStringSelection(self):
		"""
		Gets the text currently selected in the control.

		If there is no selection, the returned string is empty.

		:return:
		:rtype: string
		"""
		
		return self.textControl.GetStringSelection()
	
	def IsEditable(self):
		"""
		Returns True if the controls contents may be edited by user (note that it always can be changed by the program).

		In other words, this functions returns True if the control hasn’t been put in read-only mode by a previous call to SetEditable .

		:rtype:	bool
		"""
		
		return True
	
	def IsEmpty(self):
		"""
		Returns True if the control is currently empty.

		This is the same as GetValue .empty() but can be much more efficient for the multiline controls containing big amounts of text.

		:rtype:	bool
		"""
		
		return self.textControl.IsEmpty()
	
	def Paste(self):
		"""
		Pastes text from the clipboard to the text item.
		"""
		
		return self.textControl.Paste()
	
	def Redo(self):
		"""
		If there is a redo facility and the last operation can be redone, redoes the last operation.

		Does nothing if there is no redo facility.
		"""
		
		return self.textControl.Redo()
	
	def Remove(self, from_, to_):
		"""
		Removes the text starting at the first given position up to (but not including) the character at the last position.

		This function puts the current insertion point position at to as a side effect.

		:param from_: The first position
		:type from_: int
		:param to_: The last position
		:type to_: int
		"""
		
		return self.textControl.Remove(from_, to_)
	
	def Replace(self, from_, to_, value):
		"""
		Replaces the text starting at the first position up to (but not including) the character at the last position with the given text.

		This function puts the current insertion point position at to as a side effect.

		:param from_: The first position
		:type from_: int
		:param to_: The last position
		:type to_: int
		:param value: The value to replace the existing text with
		:type value: string
		"""
		
		return self.textControl.Replace(from_, to_, value)
	
	def SelectAll(self):
		"""
		Selects all text in the control.

		See also SetSelection
		"""
		
		return self.textControl.SelectAll()
	
	def SelectNone(self):
		"""
		Deselects selected text in the control.
		"""
		
		return self.textControl.SelectNone()
	
	def SetSelection(self, from_, to_):
		"""
		Selects the text starting at the first position up to (but not including) the character at the last position.

		If both parameters are equal to -1 all text in the control is selected.

		Notice that the insertion point will be moved to from by this function.

		:param from_: The first position
		:type from_: long
		:param to_: The last position
		:type to_: long

		See also SelectAll
		"""
		
		return self.textControl.SetSelection(from_, to_)
	
	def Undo(self):
		"""
		If there is an undo facility and the last operation can be undone, undoes the last operation.

		Does nothing if there is no undo facility.
		"""
		
		return self.textControl.Undo()
	
	def WriteText(self, text):
		"""
		Writes the text into the text control at the current insertion position.

		:param text: Text to write to the text control
		:type text: string
		"""
		
		return self.textControl.WriteText(text)


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
			Set current history list, if selectionIndex is not None, select that index

		"""
	
	def __init__(self, *arguments, **namedarguments):
		self.history = namedarguments.get("history")
		if self.history:
			del namedarguments["history"]
		
		self.historyCallBack = None
		if callable(self.history):
			self.historyCallBack = self.history
			self.history = None
		name = namedarguments.get('name', 'fileBrowseButtonWithHistory')
		namedarguments['name'] = name
		FileBrowseCtrl.__init__(self, *arguments, **namedarguments)
	
	def createTextControl(self):
		"""Create the text control"""
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
		"""Set the current history list"""
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
		"""Return the current history list"""
		if self.historyCallBack != None:
			return self.historyCallBack()
		elif self.history:
			return list(self.history)
		else:
			return []
	
	def OnSetFocus(self, event):
		"""When the history scroll is selected, update the history"""
		if self.historyCallBack != None:
			self.SetHistory(self.historyCallBack(), control=self.textControl)
		event.Skip()
	
	if wx.Platform == "__WXMSW__":
		def SetValue(self, value, callBack=1):
			""" Convenient setting of text control value, works
				around limitation of wx.ComboBox """
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
			self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize,
			style=wx.TAB_TRAVERSAL | wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON, labelText='Select a directory:',
			buttonText='Browse', toolTip='Type directory name or browse to select',
			dialogTitle='', initialValue=None, changeCallback=None,
			name='DirBrowseCtrl'
			):
		
		if initialValue is None:
			initialValue = os.getcwd()
		
		FileBrowseCtrl.__init__(
				self, parent, id, pos, size, style, labelText, buttonText,
				toolTip, dialogTitle, initialValue,
				changeCallback=changeCallback, name=name)
	
	def OnBrowse(self, ev=None):
		
		if self.GetValue() == '':
			default_path = pathlib.Path(self.initialValue)
		else:
			default_path = pathlib.Path(self.GetValue())
			if default_path.is_file():
				default_path = default_path.parent
		
		if not default_path.exists():
			default_path = pathlib.Path.home()
		
		default_path = str(default_path)
		
		dialog = wx.DirDialog(
				self, message=self.dialogTitle,
				defaultPath=default_path, style=self.style)
		
		if dialog.ShowModal() == wx.ID_OK:
			self.ChangeValue(dialog.GetPath())
		dialog.Destroy()
		
		self.textControl.SetFocus()


#

# ----------------------------------------------------------------------


if __name__ == "__main__":
	# from skeletonbuilder import rulesfile
	class SimpleCallback:
		def __init__(self, tag):
			self.tag = tag
		
		def __call__(self, event):
			print(self.tag, event.GetString())
	
	
	class DemoFrame(wx.Frame):
		def __init__(self, parent):
			wx.Frame.__init__(self, parent, -1, "File entry with browse", size=(500, 260))
			self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
			panel = wx.Panel(self, -1)
			innerbox = wx.BoxSizer(wx.VERTICAL)
			control = FileBrowseCtrl(
					panel,
					style=wx.TAB_TRAVERSAL | wx.FD_SAVE,
					fileMask="All files (*.*)|*.*|JPEG files (*.jpeg)|*.jpeg;*.jpg"
					)
			innerbox.Add(control, 0, wx.EXPAND)
			middlecontrol = FileBrowseCtrlWithHistory(
					panel,
					labelText="With History",
					history=["c:\\temp", "c:\\tmp", "r:\\temp", "z:\\temp"],
					changeCallback=SimpleCallback("With History"),
					)
			innerbox.Add(middlecontrol, 0, wx.EXPAND)
			middlecontrol = FileBrowseCtrlWithHistory(
					panel,
					labelText="History callback",
					history=self.historyCallBack,
					changeCallback=SimpleCallback("History callback"),
					)
			innerbox.Add(middlecontrol, 0, wx.EXPAND)
			self.bottomcontrol = control = FileBrowseCtrl(
					panel,
					labelText="With Callback",
					style=wx.SUNKEN_BORDER | wx.CLIP_CHILDREN,
					changeCallback=SimpleCallback("With Callback"),
					)
			innerbox.Add(control, 0, wx.EXPAND)
			self.bottommostcontrol = control = DirBrowseCtrl(
					panel,
					labelText="Simple dir browse button",
					style=wx.SUNKEN_BORDER | wx.CLIP_CHILDREN)
			innerbox.Add(control, 0, wx.EXPAND)
			ID = wx.NewIdRef()
			innerbox.Add(wx.Button(panel, ID, "Change Label", ), 1, wx.EXPAND)
			self.Bind(wx.EVT_BUTTON, self.OnChangeLabel, id=ID)
			ID = wx.NewIdRef()
			innerbox.Add(wx.Button(panel, ID, "Change Value", ), 1, wx.EXPAND)
			self.Bind(wx.EVT_BUTTON, self.OnChangeValue, id=ID)
			panel.SetAutoLayout(True)
			panel.SetSizer(innerbox)
			self.history = {"c:\\temp": 1, "c:\\tmp": 1, "r:\\temp": 1, "z:\\temp": 1}
		
		def historyCallBack(self):
			keys = self.history.keys()
			list(keys).sort()
			return keys
		
		def OnFileNameChangedHistory(self, event):
			self.history[event.GetString()] = 1
		
		def OnCloseMe(self, event):
			self.Close(True)
		
		def OnChangeLabel(self, event):
			self.bottomcontrol.SetLabel("Label Updated")
		
		def OnChangeValue(self, event):
			self.bottomcontrol.SetValue("r:\\somewhere\\over\\the\\rainbow.htm")
		
		def OnCloseWindow(self, event):
			self.Destroy()
	
	
	class DemoApp(wx.App):
		def OnInit(self):
			wx.InitAllImageHandlers()
			frame = DemoFrame(None)
			frame.Show(True)
			self.SetTopWindow(frame)
			return True
	
	#
	# def test():
	# 	app = DemoApp(0)
	# 	app.MainLoop()
	
	print('Creating dialog')
	app = DemoApp(0)
	app.MainLoop()
