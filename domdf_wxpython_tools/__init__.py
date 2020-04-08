#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  __init__.py
#
#  Copyright 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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

from domdf_wxpython_tools.border_config import border_config as BorderConfigDialog
from domdf_wxpython_tools.chartpanel import ChartPanelBase
from domdf_wxpython_tools.clearable_textctrl import ClearableTextCtrl
from . import ColourPickerPanel  # TODO: ColourPickerPanel
from domdf_wxpython_tools.dialogs import (
	file_dialog_wildcard, file_dialog_multiple, file_dialog, FloatEntryDialog, IntEntryDialog, Wildcards,
	)
from domdf_wxpython_tools.editable_listbox import EditableListBox, CleverListCtrl, EditableNumericalListBox
from domdf_wxpython_tools.events import PayloadEvent, SimpleEvent
from domdf_wxpython_tools.filebrowsectrl import FileBrowseCtrl, FileBrowseCtrlWithHistory, DirBrowseCtrl
from domdf_wxpython_tools.icons import get_button_icon, get_toolbar_icon, GetStockBitmap, GetStockToolbarBitmap
from domdf_wxpython_tools.imagepanel import (
	ID_ImagePanel_Copy_Image, ID_ImagePanel_Delete_Image, ID_ImagePanel_Load_Image,
	ID_ImagePanel_Paste_Image, ID_ImagePanel_Reset_View, ID_ImagePanel_Save_Image,
	EVT_IMAGE_PANEL_CHANGED, ImagePanel,
	)
from domdf_wxpython_tools.keyboard import gen_keymap, NAVKEYS
from . import list_dialog  # TODO: list_dialog
from domdf_wxpython_tools.logctrl import LogCtrl
from . import panel_listctrl
from . import picker  # TODO: picker
from domdf_wxpython_tools.projections import XPanAxes, XPanAxes_NoZoom, NoZoom
from domdf_wxpython_tools.style_picker import style_picker as StylePickerDialog
from domdf_wxpython_tools.style_picker import colour_picker as ColourPickerDialog
from . import StylePickerPanel  # TODO: StylePickerPanel
from domdf_wxpython_tools.tabbable_textctrl import TabbableTextCtrl
from domdf_wxpython_tools.timer_thread import Timer
from domdf_wxpython_tools.utils import toggle, coming_soon, collapse_label, generate_faces
from domdf_wxpython_tools.validators import ValidatorBase, FloatValidator, CharValidator
# TODO: WebView


__all__ = [
		"BorderConfigDialog",
		"ChartPanelBase",
		"ClearableTextCtrl",
		"ColourPickerPanel",
		"file_dialog_wildcard",
		"file_dialog_multiple",
		"file_dialog",
		"FloatEntryDialog",
		"IntEntryDialog",
		"Wildcards",
		"PayloadEvent",
		"SimpleEvent",
		"FileBrowseCtrl",
		"FileBrowseCtrlWithHistory",
		"DirBrowseCtrl",
		"get_button_icon",
		"get_toolbar_icon",
		"GetStockBitmap",
		"GetStockToolbarBitmap",
		"ID_ImagePanel_Copy_Image",
		"ID_ImagePanel_Delete_Image",
		"ID_ImagePanel_Load_Image",
		"ID_ImagePanel_Paste_Image",
		"ID_ImagePanel_Reset_View",
		"ID_ImagePanel_Save_Image",
		"EVT_IMAGE_PANEL_CHANGED",
		"ImagePanel",
		"gen_keymap",
		"NAVKEYS",
		"list_dialog",
		"LogCtrl",
		"picker",
		"panel_listctrl",
		"XPanAxes",
		"XPanAxes_NoZoom",
		"NoZoom",
		"style_picker",
		"StylePickerPanel",
		"TabbableTextCtrl",
		"Timer",
		"toggle",
		"coming_soon",
		"collapse_label",
		"generate_faces",
		"ValidatorBase",
		"FloatValidator",
		"CharValidator",
		"WebView",
		"list_dialog",
		"picker",
		"style_picker",
		"StylePickerPanel",
		"EditableListBox",
		"CleverListCtrl",
		"EditableNumericalListBox",
		"StylePickerDialog",
		"ColourPickerDialog",
		"__author__",
		"__version__",
		"__copyright__"
]

__author__ = "Dominic Davis-Foster"
__copyright__ = "Copyright 2019-2020 Dominic Davis-Foster"

__license__ = "LGPL"
__version__ = "0.2.4"
__email__ = "dominic@davis-foster.co.uk"

