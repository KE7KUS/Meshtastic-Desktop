#!/usr/bin/python3

# Meshtastic-Desktop
# by Kurt Kochendarfer, KE7KUS
# Python GUI client for use with Meshtastic project hardware

import meshtastic, platform, sys
from PySide6.QtCore import Qt, Slot, QUrl
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
  QApplication,
  QLineEdit,
  QMainWindow,
  QMenu,
  QMenuBar,
  QPushButton,
  QStatusBar,
  QTabWidget,
  QTextEdit,
  QVBoxLayout,
  QWidget
)

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.  You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

class App(QMainWindow):
  """Defines the GUI interface for the application."""

  def __init__(self):
    """Class instantiation.  Inherits attributes from QMainWindow."""
    super().__init__()

    self.title = "Meshtastic Desktop"
    self.left = 50
    self.top = 50
    self.width = 600
    self.height = 400
    
    self.setWindowTitle(self.title)
    self.setGeometry(self.left, self.top, self.width, self.height)

    self._createActions()
    self._createMenuBar()
    self._createStatusBar()

    self.tab_widget = TabWidget(self)
    self.setCentralWidget(self.tab_widget)

    self.show()

  def _createActions(self):
    """Define menu actions for the application."""

    # -----FILE MENU----- #

    # Clear the current radio configuration and set the radio to wait for new configuration to be loaded
    self.newAction = QAction(QIcon("./icons/document.png"), "&New", self)
    self.newAction.setShortcut(QKeySequence.New)

    # Open an existing radio configuration file
    self.openAction = QAction(QIcon("./icons/blue-folder-open-document-text.png"), "&Open...", self)
    self.openAction.setShortcut(QKeySequence.Open)

    # Save the current configuration to the current save file - if no save file exists, open the Save As dialog
    self.saveAction = QAction(QIcon("./icons/disk.png"), "&Save", self)
    self.saveAction.setShortcut(QKeySequence.Save)

    # Save the current configuration to a new file - opens a Save As dialog
    self.saveAsAction = QAction(QIcon("./icons/disks.png"), "Save As...", self)
    self.saveAsAction.setShortcut(QKeySequence.SaveAs)
   
    # Exit the application
    self.exitAction = QAction(QIcon("./icons/cross.png"), "&Quit", self)
    self.exitAction.setShortcut(QKeySequence.Quit)
    self.exitAction.triggered.connect(QApplication.quit)

    # -----EDIT MENU----- #

    # Cut selected text
    self.cutAction = QAction(QIcon("./icons/scissors.png"), "C&ut", self)
    self.cutAction.setShortcut(QKeySequence.Cut)

    # Copy selected text
    self.copyAction = QAction(QIcon("./icons/blue-document-copy.png"), "&Copy", self)
    self.copyAction.setShortcut(QKeySequence.Copy)

    # Paste cut/copied text
    self.pasteAction = QAction(QIcon("./icons/application--plus.png"), "&Paste", self)
    self.pasteAction.setShortcut(QKeySequence.Paste)

    self.radioConfigAction = QAction(QIcon("./icons/wrench.png"), "&Radio Configuration...", self)

    # -----HELP MENU----- #

    # Open Help dialog
    self.helpContentAction = QAction(QIcon("./icons/lifebuoy.png"), "&Help...", self)
    self.helpContentAction.setShortcut(QKeySequence.HelpContents)

    # Open About dialog
    self.aboutAction = QAction(QIcon("./icons/question.png"), "&About...", self)

  def _createMenuBar(self):
    """Constructs the application's main menu bar."""
    menuBar = self.menuBar()

    # FILE menu setup

    # fileMenu = QMenu("&File", self)
    # menuBar.addMenu(fileMenu)

    fileMenu = menuBar.addMenu("&File")

    fileMenu.addAction(self.newAction)
    fileMenu.addAction(self.openAction)
    fileMenu.addAction(self.saveAction)
    fileMenu.addAction(self.saveAsAction)
    fileMenu.addSeparator()
    fileMenu.addAction(self.exitAction)

    # EDIT menu setup

    editMenu = menuBar.addMenu("&Edit")

    editMenu.addAction(self.cutAction)
    editMenu.addAction(self.copyAction)
    editMenu.addAction(self.pasteAction)
    editMenu.addSeparator()
    editMenu.addAction(self.radioConfigAction)

    # HELP menu setup

    helpMenu = menuBar.addMenu("&Help")

    helpMenu.addAction(self.helpContentAction)
    helpMenu.addAction(self.aboutAction)

  def _createStatusBar(self):
    """Constructs the application's status bar at the bottom of the main window."""
    self.statusbar = self.statusBar() 
    self.statusbar.showMessage("Ready", 30)   

class TabWidget(QWidget):
  """Controls and interface with the QTabWidget."""

  def __init__(self, parent):
    """Class instantiation.  Inherits attributes from QWidget."""
    super().__init__(parent)
    self.layout = QVBoxLayout(self)

    self.tabs = QTabWidget()
    self.message = QWidget()
    self.filexfr = QWidget()
    self.nodelist = QWidget()
    self.nodemap = QWidget()
    self.tabs.resize(600,400)

    self.tabs.addTab(self.message, "&Messages")
    self.tabs.addTab(self.filexfr, "&File Transfer")
    self.tabs.addTab(self.nodelist, "Node &List")
    self.tabs.addTab(self.nodemap, "Node Ma&p")

    # TODO: Change layout to QGridLayout
    self.message.layout = QVBoxLayout(self)
    
    # TODO: Create multi-line text display box w/ scrolling to display message history.
    #       QTextEdit vs. QListView (https://forum.pythonguis.com/t/cloud-around-the-text-in-qtextedit/318)
    # TODO: Alternate justification - incoming messages left, outgoing messages right.
    # TODO: Bubbles or color differentiation between incoming and outgoing messages.
    # TODO: Create message delete function.
    # TODO: Separate tabs for each possible message channel vs. color differentiate channel w/ Send channel pull-down selector
    
    # TODO:  Once QGridLayout complete, move Send button to right of QLineEdit
    self.txtInput = QLineEdit(self)
    self.sendButton = QPushButton("Send Message")
    self.message.layout.addWidget(self.txtInput)
    self.message.layout.addWidget(self.sendButton)
    self.message.setLayout(self.message.layout)

    self.layout.addWidget(self.tabs)
    self.setLayout(self.layout)
    
    # TODO:  Node list use TableLayout function vs. indigenous mt-python text table layout?
    
class configDialog(QWidget):
  """User interface to control radio configuration."""
  def super().__init__():
    """Class instantiation.  Inherits attributes from QWidget."""
  # TODO:  Message - Setting for displayed message history age
  # TODO:  Message - Channel configuration for up to 8 different channels
  # TODO:  Message - Channel-specific configuration for background color, font, size, etc.
  # TODO:  Message - Save file location input (save file should save encrypted messages only)

  @Slot()
  def on_click(self):
    self.statusbar.showMessage("Sending message...", 30)
# TODO:  Add SystemTray functionality - alert on incoming messages (special emergency alert?), minimize app to system tray

def setupSerialInterface():
  if platform.system() == "Windows":
    # TODO:  Read Windows USB device list, identify COM port associated with MT VID/PID, update devPath
    i = meshtastic.SerialInterface(devPath="COM3")
  elif platform.system() == "Linux":
    i = meshtastic.SerialInterface()
  elif plaform.system() == "macOS":
    i = meshtastic.SerialInterface()
  else:
    print(f'Platform system type requires manual SerialInterface configuration.')
    # EDIT THE LINE BELOW TO POINT YOUR OS TO THE CORRECT devPath FOR YOUR MESHTASTIC HARDWARE
    i = meshtastic.SerialInterface()
  return i

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = App()
  sys.exit(app.exec())
    
 
