#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

class wndBase:
	windowname = ''
	handlers = {}
	
	def __init__(self):
		self.init()
		
		if self.windowname:
			self.wTree = gtk.glade.XML(configuration.GLADE_FILE, self.windowname)
			self.win = self.wTree.get_widget(self.windowname)
			
			#~ self.win.set_modal(True)
		
			if self.handlers:
				self.wTree.signal_autoconnect(self.handlers)

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
			
	def set_name(self, name):
		if name:
			self.windowname = name
			return True
		else:
			return False

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

class gDIMM(wndBase):
	def init( self ):
		self.set_name("wndIntro")
		self.handlers = {"gtk_main_quit" : gtk.main_quit,
			"on_btnAbout_clicked" : self.help_about,
			"on_btnNuevaDeclaracion_clicked": self.nueva_declaracion,
			}

	def help_about(self, menuItem):
		vAcercaDe = wndAbout()
		#~ vAcercaDe.set_modal(True)
		self.hide()
		vAcercaDe.show()
		
		
	def nueva_declaracion(self, *args):
		vContribuyentes = wndContribuyentes()
		self.hide()
		vContribuyentes.show()
