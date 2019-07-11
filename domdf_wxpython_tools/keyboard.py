#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  keyboard.py
#
#  Copyright 2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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

import wx

def gen_keymap():
	
	
	keys = ("BACK", "TAB", "RETURN", "ESCAPE", "SPACE", "DELETE", "START",
			"LBUTTON", "RBUTTON", "CANCEL", "MBUTTON", "CLEAR", "PAUSE",
			"CAPITAL", "END", "HOME", "LEFT", "UP", "RIGHT",
			"DOWN", "SELECT", "PRINT", "EXECUTE", "SNAPSHOT", "INSERT", "HELP",
			"NUMPAD0", "NUMPAD1", "NUMPAD2", "NUMPAD3", "NUMPAD4", "NUMPAD5",
			"NUMPAD6", "NUMPAD7", "NUMPAD8", "NUMPAD9", "MULTIPLY", "ADD",
			"SEPARATOR", "SUBTRACT", "DECIMAL", "DIVIDE", "F1", "F2", "F3", "F4",
			"F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13", "F14",
			"F15", "F16", "F17", "F18", "F19", "F20", "F21", "F22", "F23", "F24",
			"NUMLOCK", "SCROLL", "PAGEUP", "PAGEDOWN", "NUMPAD_SPACE",
			"NUMPAD_TAB", "NUMPAD_ENTER", "NUMPAD_F1", "NUMPAD_F2", "NUMPAD_F3",
			"NUMPAD_F4", "NUMPAD_HOME", "NUMPAD_LEFT", "NUMPAD_UP",
			"NUMPAD_RIGHT", "NUMPAD_DOWN", "NUMPAD_PAGEUP",
			"NUMPAD_PAGEDOWN", "NUMPAD_END", "NUMPAD_BEGIN",
			"NUMPAD_INSERT", "NUMPAD_DELETE", "NUMPAD_EQUAL", "NUMPAD_MULTIPLY",
			"NUMPAD_ADD", "NUMPAD_SEPARATOR", "NUMPAD_SUBTRACT", "NUMPAD_DECIMAL",
			"NUMPAD_DIVIDE")
	
	keyMap = {}
	
	for i in keys:
		keyMap[getattr(wx, "WXK_" + i)] = i
	for i in ("SHIFT", "ALT", "CONTROL", "MENU"):
		keyMap[getattr(wx, "WXK_" + i)] = ''
	
	return keyMap



NAVKEYS = (wx.WXK_END, wx.WXK_LEFT, wx.WXK_RIGHT,
		   wx.WXK_UP, wx.WXK_DOWN, wx.WXK_PAGEUP, wx.WXK_PAGEDOWN)