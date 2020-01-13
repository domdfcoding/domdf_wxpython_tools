#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  projections.py
#
#  Copyright 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Based on https://stackoverflow.com/a/16709952/3092681
#  Copyright 2013 simonb
#  Licensed under CC-BY-SA
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import matplotlib
from matplotlib import axes


class XPanAxes(matplotlib.axes.Axes):
	"""Constrain pan to x-axis"""
	
	name = "XPanAxes"
	
	def drag_pan(self, button, key, x, y):
		# pretend key=='x'
		matplotlib.axes.Axes.drag_pan(self, button, 'x', x, y)


class XPanAxes_NoZoom(matplotlib.axes.Axes):
	"""Constrain pan to x-axis and prevent zooming"""
	
	name = "XPanAxes_NoZoom"
	
	def drag_pan(self, button, key, x, y):
		# pretend key=='x'
		if button != 1:
			return
		matplotlib.axes.Axes.drag_pan(self, button, 'x', x, y)


class NoZoom(matplotlib.axes.Axes):
	"""Prevent zooming in pan mode"""
	
	name = "NoZoom"
	
	def drag_pan(self, button, key, x, y):
		# pretend key=='x'
		if button != 1:
			return
		matplotlib.axes.Axes.drag_pan(self, button, key, x, y)

#
# matplotlib.projections.register_projection(NoZoom)
# matplotlib.projections.register_projection(XPanAxes_NoZoom)
# matplotlib.projections.register_projection(XPanAxes)
