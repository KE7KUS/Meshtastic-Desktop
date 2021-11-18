#!/usr/bin/python3

# Meshtastic-Desktop
# by Kurt Kochendarfer, KE7KUS
# Python GUI client for use with Meshtastic project hardware

import meshtastic, platform, sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QIcon, QKeySequence, QTabWidget
from PySide6.QtWidgets import (
  QApplication,
  QMainWindow,
  QMenu,
  QMenuBar,
  QWidget
)

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.  You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

class MainWindow(QMainWindow):
  """Defines the GUI interface for the application."""
  def __init__(self, parent = None):
    """Class instantiation.  Inherits attributes from QMainWindow."""
    super().__init__()
    self.setWindowTitle("Meshtastic Desktop")
    self._createActions() 
    self._createMenuBar()
    self._createStatusBar()
    self._createTabs()

  def _createActions(self):
    """Define menu actions for the application."""
    self.newAction = QAction(QIcon("./icons/document.png"), "&New", self)
    self.newAction.setShortcut(QKeySequence.New)

    self.openAction = QAction(QIcon("./icons/blue-folder-open-document-text.png"), "&Open...", self)
    self.openAction.setShortcut(QKeySequence.Open)

    self.saveAction = QAction(QIcon("./icons/disk.png"), "&Save", self)
    self.saveAction.setShortcut(QKeySequence.Save)

    self.saveAsAction = QAction(QIcon("./icons/disks.png"), "Save As...", self)
    self.saveAsAction.setShortcut(QKeySequence.SaveAs)

    self.exitAction = QAction(QIcon("./icons/cross.png"), "&Quit", self)
    self.exitAction.setShortcut(QKeySequence.Quit)

    self.cutAction = QAction(QIcon("./icons/scissors.png"), "C&ut", self)
    self.cutAction.setShortcut(QKeySequence.Cut)

    self.copyAction = QAction(QIcon("./icons/blue-document-copy.png"), "&Copy", self)
    self.copyAction.setShortcut(QKeySequence.Copy)

    self.pasteAction = QAction(QIcon("./icons/application--plus.png"), "&Paste", self)
    self.pasteAction.setShortcut(QKeySequence.Paste)

    self.radioConfigAction = QAction(QIcon("./icons/wrench.png"), "&Radio Configuration...", self)

    self.helpContentAction = QAction(QIcon("./icons/lifebuoy.png"), "&Help...", self)
    self.helpContentAction.setShortcut(QKeySequence.HelpContents)

    self.aboutAction = QAction(QIcon("./icons/question.png"), "&About...", self)

  def _createMenuBar(self):
    """Constructs the application main menu bar."""
    menuBar = self.menuBar()

    # File Menu
    fileMenu = QMenu("&File", self)
    menuBar.addMenu(fileMenu)
    fileMenu.addAction(self.newAction)
    fileMenu.addAction(self.openAction)
    fileMenu.addAction(self.saveAction)
    fileMenu.addAction(self.saveAsAction)
    fileMenu.addSeparator()
    fileMenu.addAction(self.exitAction)

    # Edit Menu
    editMenu = menuBar.addMenu("&Edit")
    editMenu.addAction(self.cutAction)
    editMenu.addAction(self.copyAction)
    editMenu.addAction(self.pasteAction)
    editMenu.addSeparator()
    editMenu.addAction(self.radioConfigAction)

    # Help Menu
    helpMenu = menuBar.addMenu("&Help")
    helpMenu.addAction(self.helpContentAction)
    helpMenu.addAction(self.aboutAction)

  def _createStatusBar(self):
    self.statusbar = self.statusBar()
    
  def _createTabs(self):
    self.tabs = self.QtTabWidget()
    self.tabs.addTab(nodemap, "Node &Map")
    messages = # QtWidget type goes here
    
    nodes = # QtWidget type goes here
    
    nodemap = QtWebEngineView()
    nodemap.setUrl((QUrl("./map.html"))

def setupSerialInterface():
  if platform.system() == 'Windows':
    # TODO: Read Windows USB device list, identify COM port associated with Meshtastic VendorID/ProductID, update devPath accordingly
    i = meshtastic.SerialInterface(devPath='COM3')
  elif platform.system() == 'Linux':
    i = mesthastic.SerialInterface()
  elif platform.system == 'macOS':
    i = meshtastic.SerialInterface()
  else:
    print(f'Platform system type requires manual SerialInterface configuration.')
    # EDIT THE LINE BELOW TO POINT YOUR OS TO THE CORRECT devPath FOR YOUR MESHTASTIC HARDWARE
    i = meshtastic.SerialInterface()
  return i

# TODO:  Built QtWidget UI with multi-tab interface
#        - Text Messages:  send/receive, timestamp, message delete options, archive, multi-channel (up to 8) texts
#        - Data:  2-way file transfer, image compression/resizing
#        - Node List:  Display heard nodes table  
#        - Node Map (using Folium):  Display interactive map of heard stations (Folium outputs HTML page)
#        - Node Configuration:  Bandwidth/waveform, encryption key management, QR code display

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  app.exec()
