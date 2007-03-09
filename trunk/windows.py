#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#      This program is free software; you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation; either version 2 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program; if not, write to the Free Software
#      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

import sys

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

import configuration

def gtk_main_quit():
	gtk.main_quit
	sys.exit(0)

class wndBase:
	windowname = ''
	handlers = {}
	
	def __init__(self):
		self.init()
		
		if self.windowname:
			self.wTree = gtk.glade.XML(configuration.GLADE_FILE, self.windowname)
			self.win = self.wTree.get_widget(self.windowname)
			
			#~ self.win.set_modal(True)
		
			#~ if self.handlers:
			self.wTree.signal_autoconnect(self)

	def init(self):
		"Función virtual que debe ser sobreescrita para especificar los valores de arranque del formulario"
		pass
		
	def post_init(self):
		pass

	def show(self):
		if self.win:
			self.win.show()

	def hide(self):
		if self.win:
			self.win.hide()

	def idle_events(self):
		while gtk.events_pending():
			gtk.main_iteration()
			
	def set_modal(self, bool = False):
		self.win.set_modal(bool)
			
	def set_name(self, name):
		if name:
			self.windowname = name
			return True
		else:
			return False

	def setParent(self, parent):
		if parent:
			self.back_page = parent
			
	def goto_home(self, widget, *args):
		self.hide()
	

class wndContribuyentes(wndBase):

	def init(self):
		self.set_name('wndContribuyente')
		self.handlers = {
			"on_btnHome_clicked" : self.on_btnCancel_clicked,
			}

	def on_btnCancel_clicked(self, *args):
		self.win.destroy()

	def on_btnOk_clicked(self, *args):
		self.win.destroy()

class wndAbout(wndBase):
	def init(self):
		self.set_name("wndAcerca")
		
	def on_wndAcerca_close(self, *args):
		self.back_page.show()

class gDIMM:
	
	def __init__(self):
		pass
		
	def start(self):
		mainWindow = wndIntro()
		mainWindow.show()
		gtk.main()
	
class wndIntro(wndBase):
	def init( self ):
		self.set_name("wndIntro")
		#~ self.handlers = {"gtk_main_quit" : gtk.main_quit,
			#~ }

	def on_btnAbout_clicked(self, *args):
		vAcercaDe = wndAbout()
		vAcercaDe.setParent(self)
		vAcercaDe.set_modal(True)
		#~ self.hide()
		vAcercaDe.show()
	
	def on_btnClose_clicked(self, *args):
		gtk_main_quit()
		
	def on_btnNuevaDeclaracion_clicked(self, *args):
		vContribuyentes = wndContribuyentes()
		self.hide()
		vContribuyentes.show()
