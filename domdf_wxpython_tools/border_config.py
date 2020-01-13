#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  border_config.py
"""Dialog for configuring borders for charts"""
#
#  Copyright (c) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This file was originally part of GunShotMatch
#  Copyright (c) 2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  GunShotMatch is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  GunShotMatch is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class border_config(wx.Dialog):
	def __init__(self, parent, chromatogram_figure, *args, **kwds):
		self.chromatogram_figure = chromatogram_figure
		args = (parent,) + args
		# begin wxGlade: border_config.__init__
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		self.main_panel = wx.Panel(self, wx.ID_ANY)
		self.top_border_value = wx.SpinCtrlDouble(self.main_panel, wx.ID_ANY, "0.9", min=0.0, max=2.0)
		self.top_border_value.SetDigits(3)
		self.bottom_border_value = wx.SpinCtrlDouble(self.main_panel, wx.ID_ANY, "0.125", min=0.0, max=2.0)
		self.bottom_border_value.SetDigits(3)
		self.left_border_value = wx.SpinCtrlDouble(self.main_panel, wx.ID_ANY, "0.1", min=0.0, max=2.0)
		self.left_border_value.SetDigits(3)
		self.right_border_value = wx.SpinCtrlDouble(self.main_panel, wx.ID_ANY, "0.97", min=0.0, max=2.0)
		self.right_border_value.SetDigits(3)
		self.tight_layout_button = wx.Button(self.main_panel, wx.ID_ANY, "Tight Layout")
		self.close_btn = wx.Button(self.main_panel, wx.ID_ANY, "Close")

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_SPINCTRLDOUBLE, self.update_borders, self.top_border_value)
		self.Bind(wx.EVT_TEXT, self.update_borders, self.top_border_value)
		self.Bind(wx.EVT_TEXT_ENTER, self.update_borders, self.top_border_value)
		self.Bind(wx.EVT_SPINCTRLDOUBLE, self.update_borders, self.bottom_border_value)
		self.Bind(wx.EVT_TEXT, self.update_borders, self.bottom_border_value)
		self.Bind(wx.EVT_TEXT_ENTER, self.update_borders, self.bottom_border_value)
		self.Bind(wx.EVT_SPINCTRLDOUBLE, self.update_borders, self.left_border_value)
		self.Bind(wx.EVT_TEXT, self.update_borders, self.left_border_value)
		self.Bind(wx.EVT_TEXT_ENTER, self.update_borders, self.left_border_value)
		self.Bind(wx.EVT_SPINCTRLDOUBLE, self.update_borders, self.right_border_value)
		self.Bind(wx.EVT_TEXT, self.update_borders, self.right_border_value)
		self.Bind(wx.EVT_TEXT_ENTER, self.update_borders, self.right_border_value)
		self.Bind(wx.EVT_BUTTON, self.apply_tight_layout, self.tight_layout_button)
		self.Bind(wx.EVT_BUTTON, self.close_dialog, self.close_btn)
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: border_config.__set_properties
		self.SetTitle("Configure Borders")
		self.top_border_value.SetMinSize((120, -1))
		self.top_border_value.SetIncrement(0.005)
		self.bottom_border_value.SetMinSize((120, -1))
		self.bottom_border_value.SetIncrement(0.005)
		self.left_border_value.SetMinSize((120, -1))
		self.left_border_value.SetIncrement(0.005)
		self.right_border_value.SetMinSize((120, -1))
		self.right_border_value.SetIncrement(0.005)
		self.tight_layout_button.SetMinSize((120, -1))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: border_config.__do_layout
		parent_sizer = wx.BoxSizer(wx.VERTICAL)
		main_sizer = wx.BoxSizer(wx.VERTICAL)
		spinner_grid = wx.FlexGridSizer(4, 2, 4, 7)
		borders_label = wx.StaticText(self.main_panel, wx.ID_ANY, "Configure Borders")
		borders_label.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
		main_sizer.Add(borders_label, 0, wx.BOTTOM, 7)
		top_border_label = wx.StaticText(self.main_panel, wx.ID_ANY, "Top: ")
		spinner_grid.Add(top_border_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		spinner_grid.Add(self.top_border_value, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		bottom_border_label = wx.StaticText(self.main_panel, wx.ID_ANY, "Bottom: ")
		spinner_grid.Add(bottom_border_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		spinner_grid.Add(self.bottom_border_value, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		left_border_label = wx.StaticText(self.main_panel, wx.ID_ANY, "Left: ")
		spinner_grid.Add(left_border_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		spinner_grid.Add(self.left_border_value, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		right_border_label = wx.StaticText(self.main_panel, wx.ID_ANY, "Right: ")
		spinner_grid.Add(right_border_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		spinner_grid.Add(self.right_border_value, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		main_sizer.Add(spinner_grid, 0, 0, 0)
		main_sizer.Add(self.tight_layout_button, 0, wx.ALIGN_CENTER | wx.TOP, 5)
		static_line_9 = wx.StaticLine(self.main_panel, wx.ID_ANY)
		main_sizer.Add(static_line_9, 0, wx.BOTTOM | wx.EXPAND | wx.TOP, 5)
		main_sizer.Add(self.close_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)
		self.main_panel.SetSizer(main_sizer)
		parent_sizer.Add(self.main_panel, 1, wx.ALL | wx.EXPAND, 10)
		self.SetSizer(parent_sizer)
		parent_sizer.Fit(self)
		self.Layout()
		# end wxGlade
	
	def update_borders(self, event):  # wxGlade: border_config.<event_handler>
		self.chromatogram_figure.subplots_adjust(
			self.left_border_value.GetValue(),
			self.bottom_border_value.GetValue(),
			self.right_border_value.GetValue(),
			self.top_border_value.GetValue()
		)
		self.chromatogram_figure.canvas.draw_idle()
	
	def apply_tight_layout(self, event):  # wxGlade: border_config.<event_handler>
		self.chromatogram_figure.tight_layout()
		self.chromatogram_figure.canvas.draw_idle()
		
		# set SpinCtrls to new values
		self.right_border_value.SetValue(self.chromatogram_figure.subplotpars.right)
		self.left_border_value.SetValue(self.chromatogram_figure.subplotpars.left)
		self.bottom_border_value.SetValue(self.chromatogram_figure.subplotpars.bottom)
		self.top_border_value.SetValue(self.chromatogram_figure.subplotpars.top)
	
	def close_dialog(self, event):  # wxGlade: border_config.<event_handler>
		self.Destroy()

# end of class border_config
