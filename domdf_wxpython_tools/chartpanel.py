#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  chartpanel.py
"""
A canvas for displaying a chart within a wxPython window
"""
#
#  Copyright 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Method ``constrain_zoom`` based on https://stackoverflow.com/a/16709952/3092681
#  Copyright 2013 simonb
#  https://stackoverflow.com/users/456805/simonb
#
#  Method ``setup_scrollwheel_zooming`` based on https://stackoverflow.com/a/11562898/3092681
#  Copyright 2012 Thomas A Caswell
#  https://stackoverflow.com/users/380231/tacaswell
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


# Constrain zoom to X axis
matplotlib.projections.register_projection(XPanAxes)


class ChartPanelBase(wx.Panel):
	"""
	Panel that contains a matplotlib plotting window, used for displaying an image.
	The image can be right clicked to bring up a context menu allowing copying, pasting and saving of the image.
	The image can be panned by holding the left mouse button and moving the mouse,
	and zoomed in and out using the scrollwheel on the mouse.
	"""
	
	def __init__(
			self, parent, fig, ax, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
			style=0, name=wx.PanelNameStr
			):
		"""
		:param parent: The parent window.
		:type parent: wx.Window
		:param fig:
		:type fig:
		:param ax:
		:type ax:
		:param id: An identifier for the panel. wx.ID_ANY is taken to mean a default.
		:type id: wx.WindowID, optional
		:param pos: The panel position. The value ::wxDefaultPosition indicates a default position,
		:type pos: wx.Point, optional
			chosen by either the windowing system or wxWidgets, depending on platform.
		:param size: The panel size. The value ::wxDefaultSize indicates a default size, chosen by
		:type size: wx.Size, optional
			either the windowing system or wxWidgets, depending on platform.
		:param style: The window style. See wxPanel.
		:type style: int, optional
		:param name: Window name.
		:type name: str, optional
		"""
		
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
		"""
		Setup the function for updating the ylim whenever the xlim changes.s
		
		:param y_data:
		:type y_data:
		:param x_data:
		:type x_data:
		"""
		
		def update_ylim(*args):
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
		"""
		Reset the view of the chart
		"""
		
		self.canvas.toolbar.home()
		self.canvas.draw_idle()
	
	def previous_view(self, *_):
		"""
		Go to the previous view of the chart
		"""
		
		self.canvas.toolbar.back()
	
	def zoom(self, enable=True):
		"""
		Enable the Zoom tool
		"""
		
		if enable or (not enable and self.canvas.toolbar._active == "ZOOM"):
			self.canvas.toolbar.zoom()
		self.canvas.Refresh()
	
	def pan(self, enable=True):
		"""
		Enable the Pan tool
		"""
		
		if enable or (not enable and self.canvas.toolbar._active == "PAN"):
			self.canvas.toolbar.pan()
		self.canvas.Refresh()
	
	def configure_borders(self, event=None):
		"""
		Open the 'Configure Borders' dialog
		"""
		
		self.border_config = border_config(self, self.fig)
		self.border_config.Show()
		
		if event:
			event.Skip()
	
	def constrain_zoom(self, key="x"):
		"""
		Constrain zoom to the x axis only

		:param key:
		:type key:
		:return:
		:rtype:
		"""
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
		"""
		Internal function that runs whenever the window is resized
		"""
		
		# self.canvas.SetMinSize(self.GetSize())
		self.canvas.SetSize(self.GetSize())
		self.Refresh()
		self.canvas.draw()
		self.canvas.Refresh()
	
		# if event.ClassName == "wxSizeEvent":
		# 	event.Skip()
	
	def on_size_change(self, event):
		"""
		Event handler for size change events
		"""
		
		self.size_change()
		# event.Skip()
	
	def setup_scrollwheel_zooming(self, scale=1.1):
		"""
		Allow zooming of the chart with the scrollwheel
		
		:param scale:
		:type scale:
		"""
		
		def zoom_factory(ax, base_scale=1.1):
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
