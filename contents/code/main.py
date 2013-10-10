# -*- coding: utf-8 -*-
#########################################################################
# Copyright 2013 Torsten Grote <t ät grobox.de>
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QGraphicsLinearLayout
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

import time
import dbus
from dbus.mainloop.qt import DBusQtMainLoop

# TODO make the resource configurable
RES = 'akonadi_imap_resource_6'

class IMAPresourceStatus(plasmascript.Applet):
  def __init__(self,parent,args=None):
    plasmascript.Applet.__init__(self,parent)

  def init(self):
    self.setHasConfigurationInterface(False)
    self.setAspectRatioMode(Plasma.Square)

    # Theme
    self.theme = Plasma.Svg(self)
    self.theme.setImagePath("widgets/background")
    self.theme.setContainsMultipleImages(False)
    self.setBackgroundHints(Plasma.Applet.DefaultBackground)

    # DBus
    loop = DBusQtMainLoop()
    dbus.set_default_main_loop(loop)
    self.sessionBus = dbus.SessionBus()

    i = 0

    while i < 10:
      # ugly hack to wait for service to be available
      i = i + 1
      try:
        self.imap_res = self.sessionBus.get_object('org.freedesktop.Akonadi.Agent.' + RES, '/')
        self.imap_res.connect_to_signal("onlineChanged", self.onlineChanged)
      except dbus.exceptions.DBusException as e:
        if(e.get_dbus_name() == "org.freedesktop.DBus.Error.ServiceUnknown"):
          # Service is not yet ready
          print "Waiting for 'org.freedesktop.Akonadi.Agent.%s/' to become available..." % RES
          time.sleep(0.2)
        else:
          break
      else:
        break

    # Icon
    self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
    self.icon = Plasma.IconWidget()
    self.icon.mousePressEvent = self.mousePressEvent
    self.icon.mouseReleaseEvent = self.mouseReleaseEvent
    if self.isOnline():
      self.onlineChanged(True)
    else:
      self.onlineChanged(False)

    self.layout.addItem(self.icon)
    self.applet.setLayout(self.layout)


  def isOnline(self):
    return self.imap_res.isOnline(dbus_interface='org.freedesktop.Akonadi.Agent.Status')


  def onlineChanged(self, status):
    if status:
      self.icon.setIcon(self.package().path() + "contents/icons/network-server-on.png")
    else:
      self.icon.setIcon(self.package().path() + "contents/icons/network-server-off.png")


  def mouseReleaseEvent(self,event):
    if self.isOnline():
      state = False
    else:
      state = True

    self.imap_res.setOnline(state, dbus_interface='org.freedesktop.Akonadi.Agent.Status')


  def mousePressEvent(self, event):
    if event.buttons() == Qt.LeftButton:
      self.clicked = self.scenePos().toPoint()
      event.setAccepted(True)


def CreateApplet(parent):
  return IMAPresourceStatus(parent)

