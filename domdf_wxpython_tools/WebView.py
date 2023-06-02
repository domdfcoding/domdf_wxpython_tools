#!/usr/bin/env python

#
#  mxMSW_WebView.py
#
"""
Set the emulation level for wxWidgets WebView purely in Python.

Notes:

* The highest emulation level may be used even when the corresponding browser version is not installed.
* Using the ``*_FORCE`` options is not recommended.
* The :py:data:`~.wxWEBVIEWIE_EMU_DEFAULT` can be used to reset the emulation level to the system default.

The values of the constants were taken from
https://msdn.microsoft.com/library/ee330730.aspx#browser_emulation
and must not be changed.

---------

"""

#  Based on https://github.com/wxWidgets/wxWidgets/blob/master/include/wx/msw/webview_ie.h
#    by Marianne Gagnon
#    Copyright (c) 2010 Marianne Gagnon, 2011 Steven Lamerton
#
#  Also based on https://github.com/wxWidgets/Phoenix/blob/master/etg/webview.py
#    by Robin Dunn
#    Copyright (c) 2012-2018 by Total Control Software
#
#  Both licensed under the wxWindows Licence

# stdlib
import pathlib
import sys
import warnings
from typing import Optional, Union, no_type_check

# 3rd party
from domdf_python_tools.typing import PathLike

try:
	# stdlib
	import winreg
except ImportError:
	pass

__all__ = [
		"MSWSetEmulationLevel",
		"wxWEBVIEWIE_EMU_DEFAULT",
		"wxWEBVIEWIE_EMU_IE7",
		"wxWEBVIEWIE_EMU_IE8",
		"wxWEBVIEWIE_EMU_IE8_FORCE",
		"wxWEBVIEWIE_EMU_IE9",
		"wxWEBVIEWIE_EMU_IE9_FORCE",
		"wxWEBVIEWIE_EMU_IE10",
		"wxWEBVIEWIE_EMU_IE10_FORCE",
		"wxWEBVIEWIE_EMU_IE11",
		"wxWEBVIEWIE_EMU_IE11_FORCE",
		]

#: The system default browser emulation level.
wxWEBVIEWIE_EMU_DEFAULT = 0

#: Emulate Internet Explorer 7
wxWEBVIEWIE_EMU_IE7 = 7000

#: Emulate Internet Explorer 8
wxWEBVIEWIE_EMU_IE8 = 8000

#: Emulate Internet Explorer 8 (force)
wxWEBVIEWIE_EMU_IE8_FORCE = 8888

#: Emulate Internet Explorer 9
wxWEBVIEWIE_EMU_IE9 = 9000

#: Emulate Internet Explorer 9 (force)
wxWEBVIEWIE_EMU_IE9_FORCE = 9999

#: Emulate Internet Explorer 10
wxWEBVIEWIE_EMU_IE10 = 10000

#: Emulate Internet Explorer 10 (force)
wxWEBVIEWIE_EMU_IE10_FORCE = 10001

#: Emulate Internet Explorer 11
wxWEBVIEWIE_EMU_IE11 = 11000

#: Emulate Internet Explorer 12 (force)
wxWEBVIEWIE_EMU_IE11_FORCE = 11001


@no_type_check
def MSWSetEmulationLevel(
		level: int = wxWEBVIEWIE_EMU_DEFAULT,
		program_name: Optional[PathLike] = None,
		) -> bool:
	"""
	Sets the emulation level for wxWidgets WebView.

	:param level: The emulation level to use.
	:param program_name: The name of the program to set the emulation level for. Defaults to the Python executable.
	:no-default program_name:

	:return: Whether the operation completed successfully.
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

		for name in (program_name, program_name.name):
			winreg.SetValueEx(key, str(name), 0, 4, level)

	else:
		for name in (program_name, program_name.name):
			try:
				winreg.DeleteValue(key, str(name))
			except OSError:
				pass

	return True
