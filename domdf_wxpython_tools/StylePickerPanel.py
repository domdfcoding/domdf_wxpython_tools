#!/usr/bin/env python
#
#  StylePickerPanel.py
#
#  Copyright 2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
# generated by wxGlade 0.9.3 on Tue Apr  9 18:07:58 2019
#

# stdlib
from typing import List

# 3rd party
import wx  # type: ignore
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas  # type: ignore
from matplotlib.figure import Figure  # type: ignore

__all__ = ["StylePickerPanel"]

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

default_styles = ['o', 'v', '^', '<', '>', 's', 'h', 'X', 'D', 'd']


class StylePickerPanel(wx.Panel):
	"""
	Based on StylePickerPanel, a Panel for selecting a list of colours, and their order.

	:param parent: The parent window.
	:param id: An identifier for the panel. wx.ID_ANY is taken to mean a default.
	:param pos: The panel position. The value ``wx.DefaultPosition`` indicates a default position, chosen by either the windowing system or wxWidgets, depending on platform.
	:param size: The panel size. The value ``wx.DefaultSize`` indicates a default size, chosen by either the windowing system or wxWidgets, depending on platform.
	:param style: The window style. See wxPanel.
	:param name: The window name.
	:param label: Label for the panel
	:param selection_choices: A list of hex value choices to populate the 'selection' side of the panel with
	"""

	def __init__(
			self,
			parent: wx.Window,
			id=wx.ID_ANY,  # noqa: A002  # pylint: disable=redefined-builtin
			pos=wx.DefaultPosition,
			size=wx.DefaultSize,
			style=wx.TAB_TRAVERSAL,
			name=wx.PanelNameStr,
			label="Choose Styles: ",
			selection_choices: List[str] = None,
			):
		if selection_choices is None:
			selection_choices = default_styles[:]
		self.label = label
		self.selection_choices = selection_choices

		args = (parent, id, pos, size)
		kwds = {"style": style, "name": name}

		# begin wxGlade: StylePickerPanel.__init__
		kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.main_panel = wx.Panel(self, wx.ID_ANY)
		self.move_panel = wx.Panel(self.main_panel, wx.ID_ANY)
		self.picker_list_box = wx.ListBox(self.main_panel, wx.ID_ANY, choices=[])

		self.picker_figure = Figure()

		self.picker_canvas = FigureCanvas(self.main_panel, wx.ID_ANY, self.picker_figure)
		self.add_btn = wx.Button(self.main_panel, wx.ID_ANY, "Add 🡲")
		self.remove_btn = wx.Button(self.main_panel, wx.ID_ANY, "🡰 Remove")
		self.selection_list_box = wx.ListBox(self.main_panel, wx.ID_ANY, choices=[])
		self.up_btn = wx.Button(self.main_panel, wx.ID_ANY, "🡱 Up")
		self.down_btn = wx.Button(self.main_panel, wx.ID_ANY, "🡳 Down")

		self.selection_figure = Figure()

		self.selection_canvas = FigureCanvas(self.main_panel, wx.ID_ANY, self.selection_figure)

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_LISTBOX, self.update_picker_preview, self.picker_list_box)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.add, self.picker_list_box)
		self.Bind(wx.EVT_BUTTON, self.add, self.add_btn)
		self.Bind(wx.EVT_BUTTON, self.remove, self.remove_btn)
		self.Bind(wx.EVT_LISTBOX, self.update_selection_preview, self.selection_list_box)
		self.Bind(wx.EVT_BUTTON, self.move_up, self.up_btn)
		self.Bind(wx.EVT_BUTTON, self.move_down, self.down_btn)
		# end wxGlade

		self.Bind(wx.EVT_LISTBOX_DCLICK, self.remove, self.selection_list_box)

		self.markers = {
				"point": '.',
				"pixel": ',',
				"circle": 'o',
				"triangle_down": 'v',
				"triangle_up": '^',
				"triangle_left": '<',
				"triangle_right": '>',
				"tri_down": '1',
				"tri_up": '2',
				"tri_left": '3',
				"tri_right": '4',
				"octagon": '8',
				"square": 's',
				"pentagon": 'p',
				"plus (filled)": 'P',
				"star": '*',
				"hexagon1": 'h',
				"hexagon2": 'H',
				"plus": '+',
				'x': 'x',
				"x (filled)": 'X',
				"diamond": 'D',
				"thin_diamond": 'd',
				"caretleft": 4,
				"caretright": 5,
				"caretup": 6,
				"caretdown": 7,
				}

		for marker in self.selection_choices:
			for key in self.markers.keys():
				if marker == self.markers[key]:
					self.selection_list_box.Append(key)
		if not self.selection_list_box.IsEmpty():
			self.selection_list_box.SetSelection(0)

		for mark in filter(lambda x: x not in self.selection_choices, [self.markers[y] for y in self.markers]):
			for key in self.markers.keys():
				if mark == self.markers[key]:
					self.picker_list_box.Append(key)
		self.picker_list_box.SetSelection(0)

		self.picker_axes = self.picker_figure.add_subplot(111)
		self.selection_axes = self.selection_figure.add_subplot(111)
		self.update_picker_preview()
		self.update_selection_preview()

	def __set_properties(self):
		# begin wxGlade: StylePickerPanel.__set_properties
		self.move_panel.SetMinSize((170, -1))
		self.picker_list_box.SetMinSize((170, 256))
		self.picker_canvas.SetMinSize((64, 64))
		self.selection_list_box.SetMinSize((170, 256))
		self.up_btn.SetMinSize((80, -1))
		self.down_btn.SetMinSize((80, -1))
		self.selection_canvas.SetMinSize((64, 64))
		self.main_panel.SetMinSize((450, -1))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: StylePickerPanel.__do_layout
		parent_sizer = wx.BoxSizer(wx.HORIZONTAL)
		main_sizer = wx.BoxSizer(wx.VERTICAL)
		list_grid_sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer_4 = wx.BoxSizer(wx.VERTICAL)
		selection_preview_sizer = wx.BoxSizer(wx.HORIZONTAL)
		move_grid = wx.GridSizer(1, 2, 0, 5)
		sizer_3 = wx.BoxSizer(wx.VERTICAL)
		sizer_2 = wx.BoxSizer(wx.VERTICAL)
		picker_preview_sizer = wx.BoxSizer(wx.HORIZONTAL)
		grid_sizer = wx.GridSizer(1, 3, 10, 10)
		borders_label = wx.StaticText(self.main_panel, wx.ID_ANY, "Choose Styles: ")
		borders_label.SetMinSize((128, 20))
		borders_label.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ''))
		grid_sizer.Add(borders_label, 0, wx.BOTTOM, 7)
		grid_sizer.Add(self.move_panel, 1, wx.ALIGN_CENTER | wx.EXPAND, 0)
		main_sizer.Add(grid_sizer, 0, 0, 0)
		sizer_2.Add(self.picker_list_box, 5, wx.EXPAND, 0)
		sizer_2.Add((0, 0), 0, 0, 0)
		preview_label = wx.StaticText(self.main_panel, wx.ID_ANY, "Preview: ")
		picker_preview_sizer.Add(preview_label, 0, 0, 0)
		picker_preview_sizer.Add(self.picker_canvas, 1, wx.EXPAND, 0)
		sizer_2.Add(picker_preview_sizer, 0, wx.EXPAND | wx.TOP, 5)
		list_grid_sizer.Add(sizer_2, 1, wx.EXPAND, 0)
		sizer_3.Add(self.add_btn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
		sizer_3.Add(self.remove_btn, 0, wx.ALIGN_CENTER, 0)
		list_grid_sizer.Add(sizer_3, 5, wx.ALIGN_CENTER | wx.BOTTOM, 64)
		sizer_4.Add(self.selection_list_box, 5, wx.EXPAND, 0)
		move_grid.Add(self.up_btn, 0, wx.ALIGN_CENTER, 0)
		move_grid.Add(self.down_btn, 0, wx.ALIGN_CENTER, 0)
		sizer_4.Add(move_grid, 0, wx.EXPAND, 0)
		preview_label_1 = wx.StaticText(self.main_panel, wx.ID_ANY, "Preview: ")
		selection_preview_sizer.Add(preview_label_1, 0, 0, 0)
		selection_preview_sizer.Add(self.selection_canvas, 1, wx.EXPAND, 0)
		sizer_4.Add(selection_preview_sizer, 0, wx.EXPAND | wx.TOP, 5)
		list_grid_sizer.Add(sizer_4, 1, wx.EXPAND, 0)
		main_sizer.Add(list_grid_sizer, 0, 0, 0)
		static_line_11 = wx.StaticLine(self.main_panel, wx.ID_ANY)
		main_sizer.Add(static_line_11, 0, wx.BOTTOM | wx.EXPAND | wx.TOP, 5)
		self.main_panel.SetSizer(main_sizer)
		parent_sizer.Add(self.main_panel, 0, wx.ALL, 10)
		self.SetSizer(parent_sizer)
		parent_sizer.Fit(self)
		self.Layout()
		# end wxGlade
		borders_label.SetLabel(self.label)

	def move_up(self, event):  # wxGlade: StylePickerPanel.<event_handler>
		self.move(-1)
		event.Skip()

	def move_down(self, event):  # wxGlade: StylePickerPanel.<event_handler>
		self.move(1)
		event.Skip()

	def move(self, direction=1):
		selection = self.selection_list_box.GetSelection()
		selection_string = self.selection_list_box.GetString(selection)
		if self.selection_list_box.GetCount() == selection + direction or selection + direction < 0:
			return

		self.selection_list_box.Delete(selection)
		self.selection_list_box.InsertItems([selection_string], selection + direction)
		self.selection_list_box.SetSelection(selection + direction)

	def add(self, event):  # wxGlade: StylePickerPanel.<event_handler>
		selection = self.picker_list_box.GetSelection()
		if selection == -1:
			return

		selection_string = self.picker_list_box.GetString(selection)
		if selection_string == '':
			return

		self.selection_list_box.Append(selection_string)
		self.picker_list_box.Delete(selection)

		self.update_picker_preview()
		event.Skip()

	def remove(self, event):  # wxGlade: StylePickerPanel.<event_handler>
		selection = self.selection_list_box.GetSelection()
		if selection == -1:
			return

		selection_string = self.selection_list_box.GetString(selection)
		if selection_string == '':
			return

		self.picker_list_box.Append(selection_string)
		self.selection_list_box.Delete(self.selection_list_box.GetSelection())

		self.update_selection_preview()
		event.Skip()

	def update_picker_preview(self, *_):  # wxGlade: StylePickerPanel.<event_handler>
		self.update_preview(self.picker_list_box, self.picker_axes)
		self.picker_canvas.draw_idle()

	def update_selection_preview(self, *_):  # wxGlade: StylePickerPanel.<event_handler>
		self.update_preview(self.selection_list_box, self.selection_axes)
		self.selection_canvas.draw_idle()

	def update_preview(self, list_obj, axes):
		axes.clear()
		axes.axis("off")
		selection_string = list_obj.GetStringSelection()
		if selection_string == '':
			return

		axes.scatter(1, 1, s=200, color="red", marker=self.markers[selection_string])

	do_layout = __do_layout
	set_properties = __set_properties

	def get_selection(self):
		return [
				self.markers[self.selection_list_box.GetString(item)]
				for item in range(self.selection_list_box.GetCount())
				]

	def _do_layout(self):
		return self.__do_layout()

	def _set_properties(self):
		return self.__set_properties()


# end of class StylePickerPanel
