#!/usr/bin/env python
# -*- coding: utf-8 -*-

###
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
###

from elementtree.ElementTree import Element, SubElement, ElementTree, tostring, parse
from exceptions import *
import os, user

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

class Contribuyente:
    _ruc = None
    _nombre = None
    _tipo_doc_representante = None
    _doc_representante = None
    
    def __init__(self):
        self._data = Element("ruc", numero = "")
        self._nombre = SubElement(self._data, "razon_social")
        self._tipo_doc_representante = SubElement(self._data, "tipoDocRepLegal") ## C
        self._doc_representante = SubElement(self._data, "identificacionRepLegal")
    
    def load(self, data):
        self._data = data
        
        for i in self._data:
            if i.tag == "razon_social":
                self._nombre = i
            elif i.tag == "tipoDocRepLegal":
                self._tipo_doc_representante = i
            elif i.tag == "identificacionRepLegal":
                self._doc_representante = i
    
    def set_ruc(self, ruc):
        self._data.set("numero", ruc)
    
    def set_nombre(self, nombre):
        self._nombre.text = nombre

    def set_tipo_documento(self, tipo_documento):
        self._tipo_doc_representante.text = tipo_documento

    def set_documento(self, documento):
        self._doc_representante.text = documento

    def get_ruc(self):
        return self._data.get("numero")

    def get_nombre(self):
        return self._nombre.text

    def get_tipo_documento(self):
        return self._tipo_doc_representante.text

    def get_documento(self):
        return self._doc_representante.text

    def __str__(self):
        return tostring(self._data)
        
    def get_element(self):
        return self._data

class ListaContribuyentes:
    archivo = ""
    lista = []

    def __init__(self):
        self.ruta = user.home + os.sep + ".gdimm" + os.sep
        self.filename =  self.ruta + "DtsRuc.xml"
        if not os.path.isdir(self.ruta):
            os.makedirs(self.ruta, mode=0700)

    def count(self):
        return len(self.lista)

    def exists_replace(self, ruc):
        for item in self.lista:
            if item.get_ruc() == ruc :
                return self.lista.index(item)
                
        return None

    def find_by_ruc(self, ruc):
        for item in self.lista:
            if item.get_ruc() == ruc :
                return item

    def add(self, contribuyente):
        try:
            if not (contribuyente.get_ruc() and contribuyente.get_nombre() and contribuyente.get_tipo_documento() and contribuyente.get_documento()):
                raise Warning('Faltan datos en el contribuyente')
        except AttributeError:
            raise TypeError('El argumento no es un objeto tipo contribuyente')
        
        item_index = self.exists_replace(contribuyente.get_ruc())
        if item_index:
            self.lista[item_index] = contribuyente
        else:
            self.lista.append(contribuyente)

    def remove(self, contribuyente):
        if type(contribuyente)==str:
            oContribuyente = self.find_by_ruc(contribuyente)
        else:
            oContribuyente = contribuyente
        
        if oContribuyente:
            self.lista.remove(oContribuyente)

    def save(self):
        list_size = len(self.lista)
        if list_size > 0:
            data = Element("datos_ruc")
            
            for item in self.lista:
                data.insert(list_size, item.get_element())

            indent(data)

            file = open(self.filename, "w")
            file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file.write(tostring(data))
            file.close()
            #~ ElementTree(data).write(self.filename, encoding="utf-8")
    
    def load(self):
        if os.path.exists(self.filename):
            data = ElementTree(file=self.filename)
            root = data.getroot()
            self.lista = []
            for item in root:
                contrib = Contribuyente()
                contrib.load(item)
                
                self.lista.append(contrib)

    def get_elements(self):
        return self.lista
        