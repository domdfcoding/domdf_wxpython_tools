#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mxMSW_WebView.py
#
"""
Set the emulation level for wxWidgets WebView purely in Python

Based on https://github.com/wxWidgets/wxWidgets/blob/master/include/wx/msw/webview_ie.h
by Marianne Gagnon
Copyright (c) 2010 Marianne Gagnon, 2011 Steven Lamerton

and also based on https://github.com/wxWidgets/Phoenix/blob/master/etg/webview.py
by Robin Dunn
Copyright (c) 2012-2018 by Total Control Software

Both licensed under the wxWindows Licence

"""

import sys
import winreg
import warnings
import pathlib

"""
Note that the highest emulation level may be used even when the
corresponding browser version is not installed.

Using FORCE options is not recommended, DEFAULT can be used to reset level
to the system default.

The value of the constants were taken from

	https://msdn.microsoft.com/library/ee330730.aspx#browser_emulation

and must not be changed.
"""
wxWEBVIEWIE_EMU_DEFAULT = 0,
wxWEBVIEWIE_EMU_IE7 = 7000,
wxWEBVIEWIE_EMU_IE8 = 8000,
wxWEBVIEWIE_EMU_IE8_FORCE = 8888,
wxWEBVIEWIE_EMU_IE9 = 9000,
wxWEBVIEWIE_EMU_IE9_FORCE = 9999,
wxWEBVIEWIE_EMU_IE10 = 10000,
wxWEBVIEWIE_EMU_IE10_FORCE = 10001,
wxWEBVIEWIE_EMU_IE11 = 11000,
wxWEBVIEWIE_EMU_IE11_FORCE = 11001


def MSWSetEmulationLevel(level=wxWEBVIEWIE_EMU_DEFAULT, program_name=None):
	"""
	
	:param level: The emulation level to use, one of the constants specified above
	:type level: int
	:param program_name: The name of the program to set the emulation level for. Defaults to the Python executable
	:type program_name: str or pathlib.Path object
	
	:return: Whether the operation completed successfully
	:rtype: bool
	"""
	
	if not program_name:
		program_name = sys.executable
	
	if not isinstance(program_name, pathlib.Path):
		program_name = pathlib.Path(program_name)
	
	# Registry key where emulation level for programs are set
	IE_EMULATION_KEY = "SOFTWARE\\Microsoft\\Internet Explorer\\Main\\FeatureControl\\FEATURE_BROWSER_EMULATION"
	
	try:
		key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, IE_EMULATION_KEY, access=winreg.KEY_ALL_ACCESS)
	except OSError:
		warnings.warn("Failed to find web view emulation level in the registry")
		return False
	
	if level != wxWEBVIEWIE_EMU_DEFAULT:
		
		winreg.SetValueEx(key, program_name, 0, 4, level)
		winreg.SetValueEx(key, str(program_name.name), 0, 4, level)
	
	else:
		try:
			winreg.DeleteValue(key, program_name)
		except OSError:
			pass
		
		try:
			winreg.DeleteValue(key, str(program_name.name))
		except OSError:
			pass
	
	return True
