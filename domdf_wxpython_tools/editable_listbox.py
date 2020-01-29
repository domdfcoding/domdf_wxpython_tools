#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  editable_listbox.py
"""
A Python implementation of wx.EditableListBox, a ListBox with editable items.

Available in two flavours:
	> Vanilla, that accepts any string value; and
	> Numerical, that only accepts numerical values.
	  Those could be str, int, float or decimal.Decimal, but decimal.Decimal
	  is used internally and is the type that will be returned.
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Based on src/generic/editlbox.cpp from wxWidgets
#  Copyright (c) Vaclav Slavik
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
from decimal import Decimal

# 3rd party
import wx
import wx.adv
from mathematical.utils import rounders

# This package
from domdf_wxpython_tools.validators import FloatValidator


# IDs
ID_ELB_DELETE = wx.NewIdRef()
ID_ELB_EDIT = wx.NewIdRef()
ID_ELB_NEW = wx.NewIdRef()
ID_ELB_UP = wx.NewIdRef()
ID_ELB_DOWN = wx.NewIdRef()
ID_ELB_LISTCTRL = wx.NewIdRef()


# XPM for Buttons

edit_btn_xpm = [
	b"16 16 3 1",
	b"   c None",
	b".  c #000000",
	b"+  c #00007F",
	b"                ",
	b"                ",
	b"      .. ..     ",
	b"        .       ",
	b"        .       ",
	b"  ++++  .  ++++ ",
	b"     ++ . ++  ++",
	b"  +++++ . ++++++",
	b" ++  ++ . ++    ",
	b" ++  ++ . ++  ++",
	b"  +++++ .  ++++ ",
	b"        .       ",
	b"        .       ",
	b"      .. ..     ",
	b"                ",
	b"                "
		]

numerical_edit_btn_xpm = [
	b"16 16 3 1",
	b"   c None",
	b".  c #000000",
	b"+  c #00007F",
	b"                ",
	b"                ",
	b"      .. ..     ",
	b"        .       ",
	b"   ++   .  ++++ ",
	b"  +++   . ++  ++",
	b" ++++   . ++  ++",
	b"   ++   . ++  ++",
	b"   ++   . ++  ++",
	b"   ++   . ++  ++",
	b" ++++++ .  ++++ ",
	b"        .       ",
	b"        .       ",
	b"      .. ..     ",
	b"                ",
	b"                "
		]

new_btn_xpm = [
	b"16 16 5 1",
	b"   c None",
	b".  c #7F7F7F",
	b"+  c #FFFFFF",
	b"@  c #FFFF00",
	b"#  c #000000",
	b"                ",
	b"                ",
	b" .  .+ .@       ",
	b"  . .@.@# # #   ",
	b"  @.@+....   #  ",
	b" ... @@         ",
	b"  @ . @.     #  ",
	b" .# .@          ",
	b"    .        #  ",
	b"  #             ",
	b"             #  ",
	b"  #             ",
	b"             #  ",
	b"  # # # # # #   ",
	b"                ",
	b"                "
		]

delete_btn_xpm = [
	b"16 16 3 1",
	b"   c None",
	b".  c #7F0000",
	b"+  c #FFFFFF",
	b"                ",
	b"                ",
	b"                ",
	b" ..+        ..+ ",
	b" ....+     ..+  ",
	b"  ....+   ..+   ",
	b"    ...+ .+     ",
	b"     .....+     ",
	b"      ...+      ",
	b"     .....+     ",
	b"    ...+ ..+    ",
	b"   ...+   ..+   ",
	b"  ...+     .+   ",
	b"  ...+      .+  ",
	b"   .         .  ",
	b"                "
		]

down_btn_xpm = [
	b"16 16 2 1",
	b"   c None",
	b".  c #000000",
	b"                ",
	b"                ",
	b"         ...    ",
	b"        ...     ",
	b"       ...      ",
	b"       ...      ",
	b"       ...      ",
	b"       ...      ",
	b"   ...........  ",
	b"    .........   ",
	b"     .......    ",
	b"      .....     ",
	b"       ...      ",
	b"        .       ",
	b"                ",
	b"                "
		]

up_btn_xpm = [
	b"16 16 2 1",
	b"   c None",
	b".  c #000000",
	b"                ",
	b"        .       ",
	b"       ...      ",
	b"      .....     ",
	b"     .......    ",
	b"    .........   ",
	b"   ...........  ",
	b"       ...      ",
	b"       ...      ",
	b"       ...      ",
	b"       ...      ",
	b"      ...       ",
	b"     ...        ",
	b"                ",
	b"                ",
	b"                "
		]


class CleverListCtrl(wx.ListCtrl):
	"""
	list control with auto-resizable column:
	"""
	def __init__(
			self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
			size=wx.DefaultSize, style=wx.LC_ICON,
			validator=wx.DefaultValidator, name=wx.ListCtrlNameStr
			):
		"""
		:param parent:
		:type parent: wx.Window
		:param id:
		:type id: wx.WindowID
		:param pos:
		:type pos: wx.Point
		:param size:
		:type size: wx.Size
		:param style:
		:type style: int
		:param validator:
		:type validator: wx.Validator
		:param name:
		:type name: str
		"""
		
		wx.ListCtrl.__init__(self, parent, id, pos, size, style, validator, name)
		
		self.CreateColumns()
		
		self.Bind(wx.EVT_SIZE, self.OnSize)
	
	def CreateColumns(self):
		self.InsertColumn(0, "item")
		self.SizeColumns()
	
	def SizeColumns(self):
		w = self.GetSize().x
		
		if wx.Platform == "__WXMSW__":
			w -= wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X, self) + 6
		else:
			w -= 2 * wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X, self)
		
		if w < 0:
			w = 0
		self.SetColumnWidth(0, w)
	
	# private
	def OnSize(self, event):
		self.SizeColumns()
		event.Skip()


class EditableListBox(wx.Panel):
	def __init__(self, parent, id=wx.ID_ANY, label="",
			pos=wx.DefaultPosition, size=wx.DefaultSize,
			style=wx.adv.EL_DEFAULT_STYLE, name=wx.adv.EditableListBoxNameStr
			):
		"""
		This class provides a composite control that lets the user easily enter
		and edit a list of strings.

		Styles supported:
			> wx.adv.EL_ALLOW_NEW - Allow user to create new items.
			> wx.adv.EL_ALLOW_EDIT - Allow user to edit text in the control.
			> wx.adv.EL_ALLOW_DELETE - Allow user to delete text from the control.

		:param parent:
		:type parent: wx.Window
		:param id:
		:type id: wx.WindowID
		:param label:
		:type label: wx.String
		:param pos:
		:type pos: wx.Point
		:param size:
		:type size:  wx.Size
		:param style:
		:type style: int
		:param name:
		:type name: str
		"""
		
		wx.Panel.__init__(self, parent, id, pos, size, style, name)
		
		self.m_style = style
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		subp = wx.Panel(self, style=wx.SUNKEN_BORDER | wx.TAB_TRAVERSAL)
		subsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		subsizer.Add(wx.StaticText(subp, wx.ID_ANY, label),
					 1, wx.CENTER | wx.LEFT, 5)
		# TODO: if width too small put label on row above buttons
		# Min width to see all buttons = (152, 250)
		
		if self.m_style & wx.adv.EL_ALLOW_EDIT:
			self.m_bEdit = wx.BitmapButton(subp, ID_ELB_EDIT, wx.Bitmap(
				edit_btn_xpm))  # wx.ArtProvider.GetBitmap(wx.ART_EDIT, wx.ART_BUTTON))
			self.m_bEdit.SetToolTip("Edit item")
			subsizer.Add(self.m_bEdit, 0, wx.CENTER)
		
		if self.m_style & wx.adv.EL_ALLOW_NEW:
			self.m_bNew = wx.BitmapButton(subp, ID_ELB_NEW,
										  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_BUTTON))
			self.m_bNew.SetToolTip("New item")
			subsizer.Add(self.m_bNew, 0, wx.CENTER)
		
		if self.m_style & wx.adv.EL_ALLOW_DELETE:
			self.m_bDel = wx.BitmapButton(subp, ID_ELB_DELETE, wx.Bitmap(delete_btn_xpm))
			self.m_bDel.SetToolTip("Delete item")
			subsizer.Add(self.m_bDel, 0, wx.CENTER)
		
		if not (self.m_style & wx.adv.EL_NO_REORDER):
			self.m_bUp = wx.BitmapButton(subp, ID_ELB_UP,
										 wx.ArtProvider.GetBitmap(wx.ART_GO_UP, wx.ART_BUTTON))
			self.m_bUp.SetToolTip("Move up")
			subsizer.Add(self.m_bUp, 0, wx.CENTER)
			
			self.m_bDown = wx.BitmapButton(subp, ID_ELB_DOWN,
										   wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, wx.ART_BUTTON))
			self.m_bDown.SetToolTip("Move down")
			subsizer.Add(self.m_bDown, 0, wx.CENTER)
		
		subp.SetSizer(subsizer)
		subsizer.Fit(subp)
		
		sizer.Add(subp, 0, wx.EXPAND)
		
		st = wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL | wx.SUNKEN_BORDER
		
		if style & wx.adv.EL_ALLOW_EDIT:
			st |= wx.LC_EDIT_LABELS
		
		self.m_listCtrl = CleverListCtrl(self, ID_ELB_LISTCTRL, wx.DefaultPosition, wx.DefaultSize, st)
		
		self.SetStrings([])
		
		sizer.Add(self.m_listCtrl, 1, wx.EXPAND)
		
		self.SetSizer(sizer)
		self.Layout()
		
		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, id=ID_ELB_LISTCTRL)
		self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnBeginLabelEdit, id=ID_ELB_LISTCTRL)
		self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnEndLabelEdit, id=ID_ELB_LISTCTRL)
		self.Bind(wx.EVT_BUTTON, self.OnNewItem, id=ID_ELB_NEW)
		self.Bind(wx.EVT_BUTTON, self.OnUpItem, id=ID_ELB_UP)
		self.Bind(wx.EVT_BUTTON, self.OnDownItem, id=ID_ELB_DOWN)
		self.Bind(wx.EVT_BUTTON, self.OnEditItem, id=ID_ELB_EDIT)
		self.Bind(wx.EVT_BUTTON, self.OnDelItem, id=ID_ELB_DELETE)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.m_listCtrl)
	
	def OnItemActivated(self, evt):
		self.curRow = evt.GetIndex()
		print(123)
		self.m_listCtrl.EditLabel(self.curRow)
		evt.Skip()
	
	def SetStrings(self, strings):
		"""
		Replaces current contents with given strings.
		
		:param strings: list of strings
		:type strings: list of str
		"""
		
		self.m_listCtrl.DeleteAllItems()
		for i in range(len(strings)):
			self.m_listCtrl.InsertItem(i, str(strings[i]))
		
		self.m_listCtrl.InsertItem(len(strings), '')
		self.m_listCtrl.SetItemState(0, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
	
	def GetStrings(self):
		"""
		Returns a list of the current contents of the control.
		
		:return: list of strings
		:rtype: list of str
		"""
		
		strings = []
		
		for i in range(self.m_listCtrl.GetItemCount()):
			val = self.m_listCtrl.GetItemText(i)
			if val:
				strings.append(val)
	
		return strings
	
	def OnItemSelected(self, event):
		self.m_selection = event.GetIndex()
		if not (self.m_style & wx.adv.EL_NO_REORDER):
			self.m_bUp.Enable(self.m_selection != 0 and self.m_selection < self.m_listCtrl.GetItemCount() - 1)
			self.m_bDown.Enable(self.m_selection < self.m_listCtrl.GetItemCount() - 2)
			
		if self.m_style & wx.adv.EL_ALLOW_EDIT:
			self.m_bEdit.Enable(self.m_selection < self.m_listCtrl.GetItemCount())
			if self.m_style & wx.adv.EL_ALLOW_DELETE:
				self.m_bDel.Enable(self.m_selection < self.m_listCtrl.GetItemCount() - 1)
	
	def OnNewItem(self, event):
		self.m_listCtrl.SetItemState(
				self.m_listCtrl.GetItemCount() - 1,
				wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED
				)
		
		self.m_listCtrl.EditLabel(self.m_selection)
	
	def OnBeginLabelEdit(self, event):
		event.Skip()
		
		# To ensure it happens after editing starts
		wx.CallAfter(self.SetupEditControl)
	
	def SetupEditControl(self):
		edit_control = self.m_listCtrl.GetEditControl()
		
		# Bind Events
		edit_control.Bind(wx.EVT_TEXT, self.on_value_changed)
		edit_control.Bind(wx.EVT_TEXT_ENTER, self.on_value_changed)
		
		return edit_control
	
	def on_value_changed(self, event):  # wxGlade: CalibreMeasurementPanel.<event_handler>
		event.Skip()
	
	def OnEndLabelEdit(self, event):
		# return
		if event.GetIndex() == self.m_listCtrl.GetItemCount()-1 and event.GetText():
			# The user edited last (empty) line, i.e. added new entry. We have to
			# add new empty line here so that adding one more line is still
			# possible:
			self.m_listCtrl.InsertItem(self.m_listCtrl.GetItemCount(), '')
			
			# Simulate a wxEVT_LIST_ITEM_SELECTED event for the new item,
			# so that the buttons are enabled/disabled properly
			selectionEvent = wx.ListEvent(wx.wxEVT_LIST_ITEM_SELECTED, self.m_listCtrl.GetId())
			selectionEvent.SetIndex(event.GetIndex())
			self.m_listCtrl.GetEventHandler().ProcessEvent(selectionEvent)
	
	def OnDelItem(self, event):
		
		self.m_listCtrl.DeleteItem(self.m_selection)
		self.m_listCtrl.SetItemState(self.m_selection, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
	
	def OnEditItem(self, event):
		
		self.m_listCtrl.EditLabel(self.m_selection)
	
	def SwapItems(self, i1, i2):
		"""
		
		:param i1:
		:type i1: int
		:param i2:
		:type i2: int
		"""
		
		# swap the text
		t1 = self.m_listCtrl.GetItemText(i1)
		t2 = self.m_listCtrl.GetItemText(i2)
		self.m_listCtrl.SetItemText(i1, t2)
		self.m_listCtrl.SetItemText(i2, t1)

		# swap the item data
		d1 = self.m_listCtrl.GetItemData(i1)
		d2 = self.m_listCtrl.GetItemData(i2)
		self.m_listCtrl.SetItemData(i1, d2)
		self.m_listCtrl.SetItemData(i2, d1)
	
	def OnUpItem(self, event):
		
		self.SwapItems(self.m_selection - 1, self.m_selection)
		self.m_listCtrl.SetItemState(
				self.m_selection - 1,
				wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
	
	def OnDownItem(self, event):
		
		self.SwapItems(self.m_selection + 1, self.m_selection)
		self.m_listCtrl.SetItemState(
				self.m_selection + 1,
				wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
	
	def GetListCtrl(self):
		"""
		Returns a reference to the actual list control portion of the custom control.
		
		:return:
		:rtype: wx.ListCtrl
		"""
		
		return self.m_listCtrl
	
	def GetDelButton(self):
		"""
		Retrieves a reference to the BitmapButton that is used as the 'delete' button in the control.
		"""
		
		return self.m_bDel
	
	def GetNewButton(self):
		"""
		Retrieves a reference to the BitmapButton that is used as the 'new' button in the control.
		"""
		
		return self.m_bNew
	
	def GetUpButton(self):
		"""
		Retrieves a reference to the BitmapButton that is used as the 'up' button in the control.
		"""
		
		return self.m_bUp
	
	def GetDownButton(self):
		"""
		Retrieves a reference to the BitmapButton that is used as the 'down' button in the control.
		"""
		
		return self.m_bDown
	
	def GetEditButton(self):
		"""
		Retrieves a reference to the BitmapButton that is used as the 'edit' button in the control.
		"""
		
		return self.m_bEdit
			
			
class EditableNumericalListBox(EditableListBox):
	def __init__(self, parent, id=wx.ID_ANY, label="", decimal_places=-1,
			pos=wx.DefaultPosition, size=wx.DefaultSize,
			style=wx.adv.EL_DEFAULT_STYLE, name=wx.adv.EditableListBoxNameStr
			):
		"""
		
		:param parent:
		:type parent: wx.Window
		:param id:
		:type id: wx.WindowID
		:param label:
		:type label: wx.String
		:param pos:
		:type pos: wx.Point
		:param size:
		:type size:  wx.Size
		:param style:
		:type style: int
		:param name:
		:type name: str
		"""
		
		EditableListBox.__init__(self, parent, id, label, pos, size, style, name)
		
		self.SetDecimalPlaces(decimal_places)
		
		# Change bitmap for Edit button
		self.m_bEdit.SetBitmap(wx.Bitmap(numerical_edit_btn_xpm))
		self.m_bEdit.SetBitmapDisabled(wx.NullBitmap)
	
	def SetDecimalPlaces(self, _decimal_places):
		self._decimal_places = _decimal_places
		
		if self._decimal_places == 0:
			self._rounders_string = "0"
		elif self._decimal_places == -1:
			self._rounders_string = ''
		else:
			self._rounders_string = f"0.{'0' * self._decimal_places}"
	
	def GetDecimalPlaces(self):
		return self._decimal_places
	
	@property
	def decimal_places(self):
		return self._decimal_places
	
	@decimal_places.setter
	def decimal_places(self, decimal_places):
		self.SetDecimalPlaces(decimal_places)
	
	def SetStrings(self, strings):
		self.SetValues(strings)
	
	def SetValues(self, values):
		"""
		Replaces current contents with given values.
		
		:param values: list of values
		:type values: list of int or list of float or list of decimal.Decimal
		
		:return:
		:rtype:
		"""
		
		self.m_listCtrl.DeleteAllItems()
		for i in range(len(values)):
			self.m_listCtrl.InsertItem(i, str(values[i]))
		
		self.m_listCtrl.InsertItem(len(values), '')
		self.m_listCtrl.SetItemState(0, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
	
	def GetStrings(self):
		return self.GetValues()
	
	def GetValues(self):
		"""
		Returns a list of the current contents of the control.
		
		:return:
		:rtype:
		"""
		
		values = []
		
		for i in range(self.m_listCtrl.GetItemCount()):
			val = self.m_listCtrl.GetItemText(i)
			if val:
				if self.decimal_places == -1:
					# Don't format
					values.append(Decimal(val))
				else:
					values.append(rounders(val, self._rounders_string))
		
		return values
	
	def SetupEditControl(self):
		edit_control = self.m_listCtrl.GetEditControl()
		print(edit_control)
		edit_control.SetValidator(FloatValidator(5))
		
		# Bind Events
		edit_control.Bind(wx.EVT_TEXT, self.on_value_changed)
		edit_control.Bind(wx.EVT_TEXT_ENTER, self.on_value_changed)
	
	def on_value_changed(self, event):  # wxGlade: CalibreMeasurementPanel.<event_handler>
		value = event.GetEventObject().GetValue()
		
		if value == ".":
			event.GetEventObject().ChangeValue("0.")
			wx.CallAfter(event.GetEventObject().SetInsertionPointEnd)
			
		event.Skip()
