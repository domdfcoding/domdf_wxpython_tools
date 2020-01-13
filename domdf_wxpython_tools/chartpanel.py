#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  chartpanel.py
#
#  Copyright 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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


# stdlib
import types

# 3rd party
import matplotlib
import numpy
import wx.html2
from matplotlib.backends.backend_wxagg import (
	FigureCanvasWxAgg as FigureCanvas,
	NavigationToolbar2WxAgg as NavigationToolbar,
	)

# this package
from domdf_wxpython_tools.border_config import border_config
from domdf_wxpython_tools.projections import XPanAxes

matplotlib.projections.register_projection(XPanAxes)


class ChartPanelBase(wx.Panel):
	def __init__(
			self, parent, fig, ax, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
			style=0, name=wx.PanelNameStr
			):
		
		wx.Panel.__init__(self, parent, id, pos, size, style | wx.TAB_TRAVERSAL, name)
		
		self.fig = fig
		self.ax = ax
		
		self.canvas = FigureCanvas(self, wx.ID_ANY, self.fig)
		self._do_layout()
		
		self.toolbar = NavigationToolbar(self.canvas)
		self.toolbar.Hide()
		
		self.Bind(wx.EVT_SIZE, self.on_size_change, self)
		self.Bind(wx.EVT_MAXIMIZE, self.on_size_change)
	
	def setup_ylim_refresher(self, y_data, x_data):
		
		# def on_xlims_change(ax):
		def update_ylim(*args):
			# print(*args)
			# print(str(*args).startswith("MPL MouseEvent")) # Pan
			if (str(*args).startswith("XPanAxesSubplot") and self.canvas.toolbar._active != "PAN") or (
					str(*args).startswith("MPL MouseEvent") and self.canvas.toolbar._active != "ZOOM"):  # Zoom, Pan
				# print("updated xlims: ", axes.get_xlim())
				min_x_index = (numpy.abs(x_data - self.ax.get_xlim()[0])).argmin()
				max_x_index = (numpy.abs(x_data - self.ax.get_xlim()[1])).argmin()
				# print(min_x_index, max_x_index)
				
				y_vals_for_range = numpy.take(y_data, [idx for idx in range(min_x_index, max_x_index)])
				# print(max(y_vals_for_range))
				self.ax.set_ylim(bottom=0, top=max(y_vals_for_range) * 1.1)
				self.fig.canvas.draw()
				# print("x-val: {}, y-val:{}
				self.size_change()
		
		self.ax.callbacks.connect('xlim_changed', update_ylim)
		self.fig.canvas.callbacks.connect("button_release_event", update_ylim)
	
	def _do_layout(self):
		# begin wxGlade: ChromatogramPanel.__do_layout
		sizer = wx.FlexGridSizer(1, 2, 0, 0)
		sizer.Add(self.canvas, 1, wx.EXPAND, 0)
		self.SetSizer(sizer)
		sizer.Fit(self)
		self.Layout()
	
	def reset_view(self, *_):
		self.canvas.toolbar.home()
		self.canvas.draw_idle()
	
	def previous_view(self, *_):
		self.canvas.toolbar.back()
	
	def zoom(self, enable=True):
		if enable or (not enable and self.canvas.toolbar._active == "ZOOM"):
			self.canvas.toolbar.zoom()
		self.canvas.Refresh()
	
	def pan(self, enable=True):
		if enable or (not enable and self.canvas.toolbar._active == "PAN"):
			self.canvas.toolbar.pan()
		self.canvas.Refresh()
	
	def configure_borders(self, event):
		self.border_config = border_config(self, self.fig)
		self.border_config.Show()
	
	def constrain_zoom(self, key="x"):
		# Constrain zoom to x axis only
		# From https://stackoverflow.com/questions/16705452/matplotlib-forcing-pan-zoom-to-constrain-to-x-axes
		def press_zoom(self, event):
			event.key = key
			NavigationToolbar.press_zoom(self, event)
		
		self.fig.canvas.toolbar.press_zoom = types.MethodType(
				press_zoom,
				self.fig.canvas.toolbar
				)
	
	# Other Toolbar Options
	# Save chromatogram as image: save_figure(self, *args)
	# set_cursor(self, cursor)
	# Set the current cursor to one of the :class:`Cursors` enums values.
	
	# If required by the backend, this method should trigger an update in
	# the backend event loop after the cursor is set, as this method may be
	# called e.g. before a long-running task during which the GUI is not
	# updated.
	# set_history_buttons(self)
	# Enable or disable the back/forward button.
	# forward(self, *args)
	# move forward in the view lim stack.
	# print(axes.get_ylim())
	# end of class ChromatogramPanel
	
	def size_change(self):
		# code to run whenever window resized
		# self.canvas.SetMinSize(self.GetSize())
		self.canvas.SetSize(self.GetSize())
		self.Refresh()
		self.canvas.draw()
		self.canvas.Refresh()
	
	# if event.ClassName == "wxSizeEvent":
	# 	event.Skip()
	
	def on_size_change(self, event):
		self.size_change()
	
	# event.Skip()
	
	def setup_scrollwheel_zooming(self, scale=1.5):
		# https://stackoverflow.com/a/11562898/3092681
		def zoom_factory(ax, base_scale=2.):
			def zoom_fun(event):
				# get the current x and y limits
				cur_xlim = ax.get_xlim()
				cur_ylim = ax.get_ylim()
				cur_xrange = (cur_xlim[1] - cur_xlim[0]) * .5
				cur_yrange = (cur_ylim[1] - cur_ylim[0]) * .5
				xdata = event.xdata  # get event x location
				ydata = event.ydata  # get event y location
				if event.button == 'up':
					# deal with zoom in
					scale_factor = 1 / base_scale
				elif event.button == 'down':
					# deal with zoom out
					scale_factor = base_scale
				else:
					# deal with something that should never happen
					scale_factor = 1
					print(event.button)
				# set new limits
				ax.set_xlim([
						xdata - cur_xrange * scale_factor,
						xdata + cur_xrange * scale_factor
						])
				ax.set_ylim([
						ydata - cur_yrange * scale_factor,
						ydata + cur_yrange * scale_factor
						])
				self.canvas.draw()  # force re-draw
			
			fig = ax.get_figure()  # get the figure of interest
			# attach the call back
			fig.canvas.mpl_connect('scroll_event', zoom_fun)
			
			# return the function
			return zoom_fun
		
		self.__zoom_factory = zoom_factory(self.ax, base_scale=scale)