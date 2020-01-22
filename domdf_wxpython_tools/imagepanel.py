#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  imagepanel.py
"""
Based on ChartPanelBase, a canvas for displaying an image using PIL and matplotlib,
with a right click menu with some basic options
"""
#
#  Copyright 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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

# 3rd party
import matplotlib
import wx
from matplotlib.figure import Figure
from PIL import Image

# this package
from domdf_wxpython_tools.chartpanel import ChartPanelBase
from domdf_wxpython_tools.dialogs import file_dialog_wildcard, Wildcards
from domdf_wxpython_tools.projections import NoZoom

matplotlib.projections.register_projection(NoZoom)

images_wildcard = Wildcards()
images_wildcard.add_image_wildcard()
images_wildcard.add_common_filetype("jpeg")
images_wildcard.add_common_filetype("png")
images_wildcard.add_common_filetype("bmp")
images_wildcard.add_common_filetype("tiff")
images_wildcard.add_common_filetype("gif")
images_wildcard.add_all_files_wildcard()


# Events
ImgPanelChangedEvent = wx.NewEventType()
EVT_IMAGE_PANEL_CHANGED = wx.PyEventBinder(ImgPanelChangedEvent, 0)


class EvtImgPanelChanged(wx.PyCommandEvent):
	eventType = ImgPanelChangedEvent

	def __init__(self, windowID, obj):
		wx.PyCommandEvent.__init__(self, self.eventType, windowID)
		self.SetEventObject(obj)




class ImagePanel(ChartPanelBase):
	default_image = ("RGB", (640, 480), (0, 0, 0))
	
	def __init__(
			self, parent, image=None, id=wx.ID_ANY, pos=wx.DefaultPosition,
			size=wx.DefaultSize, style=0, name=wx.PanelNameStr):
		
		fig = Figure()
		ax = fig.add_subplot(111, frameon=False, projection="NoZoom")  # 1x1 grid, first subplot
		
		ChartPanelBase.__init__(self, parent, fig, ax, id, pos, size, style, name)
		
		if isinstance(image, Image.Image):
			# PIL Image object, load directly
			self._image = image
		elif image is None:
			self._image = Image.new(*self.default_image)
		else:
			# Filename, load from file
			# self._image = mpimg.imread(image)
			self._image = Image.open(image)
			
		self.editable = True
		
		self._setup_context_menu()
		
		self._load_image()
		wx.CallAfter(self.reset_view)
	
	def _setup_context_menu(self):
		self.context_menu = wx.Menu()
		
		self.context_menu.Append(ID_ImagePanel_Reset_View, "Reset View")
		self.Bind(wx.EVT_MENU, self.reset_view, id=ID_ImagePanel_Reset_View)
		
		self.context_menu.AppendSeparator()
		
		self.context_menu.Append(ID_ImagePanel_Copy_Image, "Copy Image")
		self.Bind(wx.EVT_MENU, self.copy, id=ID_ImagePanel_Copy_Image)
		self.context_menu.Append(ID_ImagePanel_Paste_Image, "Paste Image")
		self.Bind(wx.EVT_MENU, self.paste, id=ID_ImagePanel_Paste_Image)
		
		self.context_menu.Append(ID_ImagePanel_Save_Image, "Save Image")
		self.Bind(wx.EVT_MENU, self.on_save, id=ID_ImagePanel_Save_Image)
		
		self.context_menu.AppendSeparator()
		
		self.context_menu.Append(ID_ImagePanel_Load_Image, "Load Image")
		self.Bind(wx.EVT_MENU, self.on_load, id=ID_ImagePanel_Load_Image)
		
		self.context_menu.Append(ID_ImagePanel_Delete_Image, "Delete Image")
		self.Bind(wx.EVT_MENU, self.clear, id=ID_ImagePanel_Delete_Image)
	
	def load_image(self, new_image, suppress_event=False):
		"""
		
		:param new_image:
		:type new_image:
		:param suppress_event: Whether the event that the image has changed should be suppressed
		:type suppress_event:
		:return:
		:rtype:
		"""
		self.ax.clear()
		self._image = None
		self._image = None
		
		# if not new_image:
		# 	return
		
		if isinstance(new_image, Image.Image):
			# PIL Image object, load directly
			self._image = new_image
		elif new_image is None:
			self._image = Image.new(*self.default_image)
		else:
			# Filename, load from file
			# self._image = mpimg.imread(image)
			self._image = Image.open(new_image)
		
		#self._image = Image.open(new_image)
		self._load_image()
		self.pan(True)
		
		if not suppress_event:
			wx.PostEvent(self.GetEventHandler(), EvtImgPanelChanged(self.GetId(), self))
	
	def _load_image(self):
		# self.ax = self.fig.add_subplot(111, projection="XPanAxes_NoZoom")  # 1x1 grid, first subplot
		
		# self._image = mpimg.imread(image)
		# self._image = Image.open(image)
		#
		self.ax.clear()
		self.ax.imshow(self._image)
		
		self.ax.axes.get_xaxis().set_visible(False)
		self.ax.axes.get_yaxis().set_visible(False)
		self.fig.tight_layout()
		# self.fig.subplots_adjust(left=0.1, bottom=0.125, top=0.9, right=0.97)
		
		self.canvas.draw()
		
		self.pan(True)
		self.ax.autoscale(tight=True)
		self.setup_scrollwheel_zooming()
		self.canvas.mpl_connect('button_press_event', self.on_context_menu)
		
	def on_context_menu(self, event):
		if event.button == matplotlib.backend_bases.MouseButton.RIGHT:
			event.guiEvent.GetEventObject().ReleaseMouse()
			print('in context_menu callback: clicked at (%g, %g)' % (event.x, event.y))
			self.PopupMenu(self.context_menu)
	
	# UIActionSimulator().MouseClick(wx.MOUSE_BTN_RIGHT)
	
	def copy(self, event):
		width, height = self._image.size
		bmp = wx.Bitmap.FromBuffer(width, height, self._image.tobytes())
		
		# Create BitmapDataObject
		bmp_data = wx.BitmapDataObject(bmp)
		
		# Write image from clipboard
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(bmp_data)
			wx.TheClipboard.Flush()
		wx.TheClipboard.Close()
	
	def paste(self, event):
		# Create empty BitmapDataObject
		bmp_data = wx.BitmapDataObject()
		
		# Read image from clipboard
		wx.TheClipboard.Open()
		if wx.TheClipboard.GetData(bmp_data):
			wx.TheClipboard.Close()
			
			# https://stackoverflow.com/a/46606553/3092681
			# Get bitmap and convert to PIL Image
			bmp = bmp_data.GetBitmap()
			size = tuple(bmp.GetSize())
			buf = size[0] * size[1] * 3 * b"\x00"
			bmp.CopyToBuffer(buf)
			self._image = Image.frombuffer("RGB", size, buf, "raw", "RGB", 0, 1)
			self._load_image()
			self.pan(True)
			event.Skip()
			
			wx.PostEvent(self.GetEventHandler(), EvtImgPanelChanged(self.GetId(), self))
		
		else:
			# No image on clipboard
			wx.TheClipboard.Close()
	
	def on_save(self, event):
		save_location = file_dialog_wildcard(
				self, "Save Image",
				images_wildcard.wildcard,
				style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
				)
		
		if not save_location:
			return
		
		self._image.save(save_location[0])
	
	def on_load(self, event):
		new_image = file_dialog_wildcard(
				self, "Choose an Image",
				images_wildcard.wildcard,
				style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
				)
		
		if not new_image:
			return
		
		self._image = Image.open(new_image[0])
		self._load_image()
		self.pan(True)
		event.Skip()
		
		wx.PostEvent(self.GetEventHandler(), EvtImgPanelChanged(self.GetId(), self))
	
	def clear(self, event=None):
		self.ax.clear()
		self._image = None
		self._image = None
		if event:
			event.Skip()
		
		wx.PostEvent(self.GetEventHandler(), EvtImgPanelChanged(self.GetId(), self))
		
	def reset_view(self, *_):
		self._load_image()
		self.fig.tight_layout()
		self.canvas.SetSize(self.GetSize())
		self.Refresh()
		self.canvas.draw()
		self.canvas.Refresh()
		self.pan(True)
		# wx.CallAfter(self.pan)
	
	@property
	def image(self):
		return self._image
	#
	# @image.setter
	# def image(self, new_image):
	#
	# 	if isinstance(new_image, Image.Image):
	# 		# PIL Image object, load directly
	# 		self._image = new_image
	# 	elif new_image is None:
	# 		self._image = Image.new("RGB", (640, 480), (73, 109, 137))
	# 	else:
	# 		# Filename, load from file
	# 		# self._image = mpimg.imread(image)
	# 		self._image = Image.open(new_image)
	#
	# 	self.load_image()
	# 	#self.reset_view()
	# 	wx.CallAfter(self.reset_view)
		

ID_ImagePanel_Reset_View = wx.NewIdRef()
ID_ImagePanel_Copy_Image = wx.NewIdRef()
ID_ImagePanel_Paste_Image = wx.NewIdRef()
ID_ImagePanel_Save_Image = wx.NewIdRef()
ID_ImagePanel_Load_Image = wx.NewIdRef()
ID_ImagePanel_Delete_Image = wx.NewIdRef()
