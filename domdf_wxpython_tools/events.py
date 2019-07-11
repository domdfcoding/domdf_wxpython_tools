#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  events.py
"""
Reusable code for simple events


Usage:

>>> from domdf_wxpython_tools import events

>>> myEVT = events.Event(self)

>>> Event.bind(self.handler)


To Trigger:

>>> Event.trigger()

"""
#
#  Copyright (c) 2019.  Dominic Davis-Foster <dominic@davis-foster.co.uk>
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

from collections import OrderedDict
from builtins import property as _property

import wx

class SimpleEvent(object):
	"""
	SimpleEvent(receiver, name, event, binder)
	"""
	
	_fields = ("receiver", "name", "event", "binder")
	
	def __init__(self, receiver=None, name="Event"):
		"""
		
		:param receiver:
		:param name:
		"""
		
		self.receiver = receiver
		self.name = name
		self.event = wx.NewEventType()
		self.binder = wx.PyEventBinder(self.event, 1)
		

	def __repr__(self):
		'Return a nicely formatted representation string'
		return 'SimpleEvent(name=%r)' % self.name

	def _asdict(self):
		'Return a new OrderedDict which maps field names to their values'
		return OrderedDict(zip(self._fields, self))

	__dict__ = _property(_asdict)
	
	def set_receiver(self, receiver):
		self.receiver = receiver
	
	def Bind(self, handler, **kwargs):
		self.receiver.Bind(self.binder, handler, **kwargs)
	
	def Unbind(self, **kwargs):
		self.receiver.Unind(self.binder, **kwargs)
	
	def trigger(self):
		wx.PostEvent(self.receiver, wx.PyCommandEvent(self.event, -1))

