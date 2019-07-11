#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  timer_thread.py
"""
Background thread that sends an event after the specified interval.
Useful for timeouts or updating timers, clocks etc.


Includes code from https://gist.github.com/samarthbhargav/5a515a399f7113137331
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

import time

from threading import Thread, Event

from domdf_wxpython_tools.events import SimpleEvent

timer_event = SimpleEvent("Timer")

class Timer(Thread):
	"""
	Background Timer Class
	"""
	
	def __init__(self, parent, interval=1.0):
		"""
		Init Timer Thread Class

		:param parent: Class to send event updates to
		:param interval: Interval to trigger events at, in seconds. Default 1.0
		:type interval: float
		"""
		
		self._stopevent = Event()
		Thread.__init__(self, name="TimerThread")
		self._parent = parent
		self._interval = interval
	
	def run(self):
		"""
		Run Timer Thread
		"""
		
		wait_time = 0 + self._interval
		while not self._stopevent.isSet():
			time.sleep(0.1)
			wait_time -= 0.1
			if wait_time < 0.0:
				timer_event.trigger()
				wait_time = 0 + self._interval
	
	def join(self, timeout=None):
		"""
		Stop the thread and wait for it to end

		:param timeout:
		:type:
		"""
		
		self._stopevent.set()
		Thread.join(self, timeout)