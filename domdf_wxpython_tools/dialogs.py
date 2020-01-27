#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dialogs.py
"""
Several dialog classes and helper functions for file/folder dialogs
"""
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
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import os

# 3rd party
import wx

# this package
from domdf_wxpython_tools.validators import CharValidator
from domdf_wxpython_tools.list_dialog import list_dialog

# style enumeration
style_uppercase = 4
style_lowercase = 8
style_hidden = 16


common_filetypes = {
		"jpeg": ("JPEG files", ["jpg", "jpeg"]),
		"png": ("PNG files", ["png"]),
		"bmp": ("BMP files", ["bmp"]),
		"tiff": ("TIFF files", ["tiff", "tif"]),
		"gif": ("GIF files", ["gif"])
		# TODO: Add more
		}


def file_dialog_wildcard(parent, title, wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT, **kwargs):
	"""
	Create a wx.FileDialog with the wildcard string given, and return a list of the files selected.
	
	:param parent:
	:type parent:
	:param wildcard:
	:type wildcard:
	:param title:
	:type title:
	:param style:
	:type style:
	:param kwargs:
	:type kwargs:

	:return: List of filenames for the selected files. If wx.FD_MULTIPLE is not in the style, the list will contain only one element
	:rtype: list of str
	"""
	
	with wx.FileDialog(
			parent, title,
			wildcard=wildcard,
			style=style, **kwargs
			) as fileDialog:
		
		if fileDialog.ShowModal() == wx.ID_CANCEL:
			return  # the user changed their mind
		
		try:
			pathnames = fileDialog.GetPaths()
		except:
			pathnames = [fileDialog.GetPath()]
		
		filter_extension_list = wildcard.split("|")[1::2]
		valid_extensions = [os.path.splitext(ext)[1] for ext in ";".join(filter_extension_list).split(";")]
		selected_filter_index = fileDialog.GetFilterIndex()
		
		selected_filter_extensions = filter_extension_list[selected_filter_index].replace("*.", ".").split(";")
		
		for index, pathname in enumerate(pathnames):
			if selected_filter_extensions[0] != ".*":
				if os.path.splitext(pathname)[-1].lower() not in selected_filter_extensions:
					pathnames[index] = pathname + f"{selected_filter_extensions[0]}"
		
		return pathnames


def file_dialog_multiple(parent, extension, title, filetypestring, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT, **kwargs):
	"""
	Create a wx.FileDialog with for the extension and filetypestring given, and return a list of the files selected.
	
	:param parent:
	:type parent:
	:param extension:
	:type extension:
	:param title:
	:type title:
	:param filetypestring:
	:type filetypestring:
	:param style:
	:type style:
	:param kwargs:
	:type kwargs:
	
	:return: List of filenames for the selected files. If wx.FD_MULTIPLE is not in the style, the list will contain only one element
	:rtype: list of str
	"""
	
	with wx.FileDialog(
			parent, title,
			wildcard=f"{filetypestring} (*.{extension.lower()})|*.{extension.lower()};*.{extension.upper()}",
			style=style, **kwargs
	) as fileDialog:
		
		if fileDialog.ShowModal() == wx.ID_CANCEL:
			return  # the user changed their mind
		
		try:
			pathnames = fileDialog.GetPaths()
		except:
			pathnames = [fileDialog.GetPath()]
		
		for index, pathname in enumerate(pathnames):
			if extension != "*":
				if os.path.splitext(pathname)[-1].lower() != f".{extension}":
					pathnames[index] = pathname + f".{extension}"
		# else:
		# 	pathnames[index] = os.path.splitext(pathname)[0]
		
		return pathnames


def file_dialog(*args, **kwargs):
	"""
	Create a wx.FileDialog with for the extension and filetypestring given, and return the filename selected.
	
	:param parent:
	:type parent:
	:param extension:
	:type extension:
	:param title:
	:type title:
	:param filetypestring:
	:type filetypestring:
	:param style:
	:type style:
	:param kwargs:
	:type kwargs:
	
	:return: The filename selected in the dialog. If wx.FD_MULTIPLE is in the style, this will be the first filename selected.
	:rtype: str
	"""
	
	paths = file_dialog_multiple(*args, **kwargs)
	
	if paths is not None:
		return paths[0]


class FloatEntryDialog(wx.TextEntryDialog):
	"""
	Alternative to wx.NumberEntryDialog that provides a TextCtrl which only allows numbers and decimal points to be entered.
	
	Based on http://wxpython-users.1045709.n5.nabble.com/Adding-Validation-to-wx-TextEntryDialog-td2371082.html
	"""
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.textctrl = self.FindWindowById(3000)
		
		self.textctrl.SetValidator(CharValidator("float-only"))
	
	def GetValue(self):
		value = self.textctrl.GetValue()
		if value == '':
			return None
		else:
			return float(value)


class IntEntryDialog(wx.TextEntryDialog):
	"""
	Alternative to wx.NumberEntryDialog that provides a TextCtrl which only allows numbers to be entered.

	Based on http://wxpython-users.1045709.n5.nabble.com/Adding-Validation-to-wx-TextEntryDialog-td2371082.html
	"""
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.textctrl = self.FindWindowById(3000)
		
		self.textctrl.SetValidator(CharValidator("int-only"))

	def GetValue(self):
		value = self.textctrl.GetValue()
		if value == '':
			return None
		else:
			return int(value)


class Wildcards:
	"""
	Class to generate glob wildcards for wx.FileDialog
	"""
	
	def __init__(self):
		self._wildcards = []
	
	def add_filetype(
			self, description, extensions=None, hint_format=style_lowercase,
			value_format=style_lowercase | style_uppercase):
		"""
		Add a filetype to the wildcards
		
		:param description: Description of the filetype
		:type description: str
		:param extensions: A list of valid file extensions for the filetype
		:type extensions: list of str
		:param hint_format: How the hints should be formatted.
		:type hint_format: int
		:param value_format: How the values should be formatted.
		:type value_format:	int
		
		Valid values for `hint_format` and `value_format` are `style_uppercase`,
		`style_lowercase` and `style_hidden`, which can be combined using the `|` operator.
		"""
		
		if extensions:
			hint = []
			value = []
			
			for extension in extensions:
				
				if not extension.startswith("*."):
					extension = f"*.{extension}"
				
				# Hint
				if not hint_format & style_hidden:
					if hint_format & style_lowercase:
						hint.append(extension.lower())
						
					if hint_format & style_uppercase:
						hint.append(extension.upper())
					
				# Value
				if value_format & style_lowercase:
					value.append(extension.lower())
						
				if value_format & style_uppercase:
					value.append(extension.upper())
			
			if hint_format & style_hidden:
				self._wildcards.append(f"{description}|{';'.join(value)}")
			else:
				self._wildcards.append(f"{description} ({';'.join(hint)})|{';'.join(value)}")
		
		else:
			self._wildcards.append(f"{description}")
	
	@property
	def wildcard(self):
		"""
		Returns a string representing the wildcards for use in wx.FileDialog or file_dialog_wildcards
		
		:rtype: str
		"""
		
		return "|".join(self._wildcards)
	
	def add_common_filetype(
			self, filetype, hint_format=style_lowercase,
			value_format=style_lowercase | style_uppercase):
		"""
		Add a common filetype.
		
		:param filetype: The name of the filetype, Possible values are in common_filetypes
		:type filetype: str
		:param hint_format: How the hints should be formatted.
		:type hint_format: int
		:param value_format: How the values should be formatted.
		:type value_format:	int
		
		Valid values for `hint_format` and `value_format` are `style_uppercase`,
		`style_lowercase` and `style_hidden`, which can be combined using the `|` operator.
		"""
		
		self.add_filetype(*common_filetypes[filetype], hint_format=hint_format, value_format=value_format)

	def add_image_wildcard(self, value_format=style_lowercase | style_uppercase):
		"""
		Add a wildcard for all image filetypes.

		:param value_format: How the values should be formatted.
		:type value_format:	int

		Valid values for `value_format` are `style_uppercase`,
		`style_lowercase` and `style_hidden`, which can be combined using the `|` operator.
		"""
		
		image_extensions = []
		for key, item in common_filetypes.items():
			if key in {"jpeg", "png", "bmp", "tiff", "gif"}:
				for extension in item[1]:
					image_extensions.append(f"*.{extension.lower()}")
					image_extensions.append(f"*.{extension.upper()}")
				
		self.add_filetype("Image files", image_extensions, hint_format=style_hidden, value_format=value_format)
	
	def add_all_files_wildcard(self, hint_format=0):
		"""
		Add a wildcard for 'All Files'.

		:param hint_format: How the hints should be formatted. Valid values are None and `style_hidden`.
		:type hint_format: int
		"""
		
		if hint_format & style_hidden:
			self._wildcards.append("All files|*.*")
		else:
			self._wildcards.append("All files (*.*)|*.*")
	
	def __repr__(self):
		return f"Wildcard = {self.wildcard}"
	
	def __str__(self):
		return self.wildcard


# legacy name
FileDialogWildcards = Wildcards