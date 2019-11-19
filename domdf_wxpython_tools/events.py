#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  events.py
"""
Reusable code for simple events

Usage:

>>> from domdf_wxpython_tools import events

>>> # Create the event outside of the class
>>> myEVT = events.SimpleEvent()

>>> # Set the receiver to the class you want.
>>> # This is usually done from within the receiver class
>>> class MyClass(object):
... 	def __init__(self):
... 		myEVT.set_receiver(self)
...
... 		# Then bind the event to a handler
... 		myEVT.Bind(self.handler)
...
... 	def handler(self):
... 		'''Handler for myEVT'''
... 		pass

>>> # From within the thread, trigger the event with the following syntax:

>>> myEVT.trigger()

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
		"""
		Return a nicely formatted representation string
		"""
		
		return f'SimpleEvent(name={self.name})'

	def __dict__(self):
		"""
		Return a new OrderedDict which maps field names to their values
		
		:return:
		:rtype: OrderedDict
		"""
		
		return OrderedDict(zip(self._fields, self))
	
	def set_receiver(self, receiver):
		"""
		Set the class that is to receive the event trigger
		
		:param receiver:
		"""
		
		self.receiver = receiver
	
	def Bind(self, handler, **kwargs):
		"""
		Bind the event to the handler
		
		:param handler: handler to bind the event to
		:param kwargs: keyword arguments to pass through to receiver's Bind method
		"""
		
		self.receiver.Bind(self.binder, handler, **kwargs)
	
	def Unbind(self, **kwargs):
		"""
		Unbind the event from the handler
		
		:param kwargs: keyword arguments to pass through to receiver's Unbind method
		"""
		
		self.receiver.Unind(self.binder, **kwargs)
	
	def trigger(self):
		"""
		Trigger the event
		"""
		wx.PostEvent(self.receiver, wx.PyCommandEvent(self.event, -1))

