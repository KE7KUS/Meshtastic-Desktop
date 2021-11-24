#!/usr/bin/python3

# Meshtastic-Desktop
# by Kurt Kochendarfer, KE7KUS
# Python GUI client for use with Meshtastic project hardware

import meshtastic, platform, sys, os, folium
from PySide6.QtCore import Qt, Slot, QUrl
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
  QApplication,
  QGridLayout,
  QLineEdit,
  QListView,
  QListWidget,
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
    self.width = 800
    self.height = 600
    
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
    self.newAction.setStatusTip("Create a new Meshtastic node configuration file")

    # Open an existing radio configuration file
    self.openAction = QAction(QIcon("./icons/blue-folder-open-document-text.png"), "&Open...", self)
    self.openAction.setShortcut(QKeySequence.Open)
    self.openAction.setStatusTip("Open an existing Meshtastic node configuration file...")    

    # Save the current configuration to the current save file - if no save file exists, open the Save As dialog
    self.saveAction = QAction(QIcon("./icons/disk.png"), "&Save", self)
    self.saveAction.setShortcut(QKeySequence.Save)
    self.saveAction.setStatusTip("Save the configuration to the current Save file")

    # Save the current configuration to a new file - opens a Save As dialog
    self.saveAsAction = QAction(QIcon("./icons/disks.png"), "Save As...", self)
    self.saveAsAction.setShortcut(QKeySequence.SaveAs)
    self.saveAsAction.setStatusTip("Save the configuration to a new file...")
   
    # Exit the application
    self.exitAction = QAction(QIcon("./icons/cross.png"), "&Quit", self)
    self.exitAction.setShortcut(QKeySequence.Quit)
    self.exitAction.triggered.connect(QApplication.quit)
    self.exitAction.setStatusTip("Exit the program")

    # -----EDIT MENU----- #

    # Cut selected text
    self.cutAction = QAction(QIcon("./icons/scissors.png"), "C&ut", self)
    self.cutAction.setShortcut(QKeySequence.Cut)
    self.cutAction.setStatusTip("Cut the selected text to the clipboard")

    # Copy selected text
    self.copyAction = QAction(QIcon("./icons/blue-document-copy.png"), "&Copy", self)
    self.copyAction.setShortcut(QKeySequence.Copy)
    self.copyAction.setStatusTip("Copy the selected text to the clipboard")

    # Paste cut/copied text
    self.pasteAction = QAction(QIcon("./icons/application--plus.png"), "&Paste", self)
    self.pasteAction.setShortcut(QKeySequence.Paste)
    self.pasteAction.setStatusTip("Paste the contents of the clipboard")

    self.radioConfigAction = QAction(QIcon("./icons/wrench.png"), "&Radio Configuration...", self)
    self.radioConfigAction.setStatusTip("Change configuration settings for the connected Meshtastic radio...")

    # -----HELP MENU----- #

    # Open Help dialog
    self.helpContentAction = QAction(QIcon("./icons/lifebuoy.png"), "&Help...", self)
    self.helpContentAction.setShortcut(QKeySequence.HelpContents)
    self.helpContentAction.setStatusTip("Open the internal help file...")

    # Open About dialog
    self.aboutAction = QAction(QIcon("./icons/question.png"), "&About...", self)
    self.aboutAction.setStatusTip("Get information about the Meshtastic-Desktop program...")

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
    self.statusbar = QStatusBar()
    self.setStatusBar(self.statusbar) 
    self.statusbar.showMessage("Ready", 30)   

class TabWidget(QWidget):
  """Controls and interfaces with the QTabWidget."""

  def __init__(self, parent):
    """Class instantiation.  Inherits attributes from QWidget."""
    super().__init__(parent)
    self.layout = QVBoxLayout(self)

    self.tabs = QTabWidget()
    self.message = QWidget()
    self.filexfr = QWidget()
    self.nodelist = QWidget()
    self.nodemap = QWidget()
    self.tabs.resize(800,600)

    self.tabs.addTab(self.message, "&Messages")
    self.tabs.addTab(self.filexfr, "&File Transfer")
    self.tabs.addTab(self.nodelist, "Node &List")
    self.tabs.addTab(self.nodemap, "Node Ma&p")

    # ---Messages Tab--- #
    self.message.layout = QGridLayout()
    self.message.layout.setHorizontalSpacing(10)
    self.message.layout.setVerticalSpacing(10)
    self.textWindow = QListView(self)
    self.txtInput = QLineEdit(self)
    self.sendButton = QPushButton("Send Message")
    self.message.layout.addWidget(self.textWindow, 1, 1, 3, 4)
    self.message.layout.addWidget(self.txtInput, 4, 1, 1, 3)
    self.message.layout.addWidget(self.sendButton, 4, 4, 1, 1)     

    # QListView (https://forum.pythonguis.com/t/cloud-around-the-text-in-qtextedit/318)
    # TODO: Alternate justification - incoming messages left, outgoing messages right.
    # TODO: Bubbles or color differentiation between incoming and outgoing messages.
    # TODO: Create message delete function.
    # TODO: Separate tabs for each possible message channel vs. color differentiate channel w/ Send channel pull-down selector

    self.message.setLayout(self.message.layout)

    # ---File Transfer Tab--- #
    self.filexfr.layout = QGridLayout()
    self.filexfr.layout.setHorizontalSpacing(10)
    self.filexfr.layout.setVerticalSpacing(10)
    self.fileXfrList = QListWidget(self)
    self.fileXfrRcvr = QListWidget(self)
    self.fileXfrBtn = QPushButton(QIcon("./icons/arrow-000-medium.png"), "File Transfer", self)

    self.filexfr.layout.addWidget(self.fileXfrList, 1, 1, 3, 2)
    self.filexfr.layout.addWidget(self.fileXfrBtn, 2, 4, 1, 1)
    self.filexfr.layout.addWidget(self.fileXfrRcvr, 1, 5, 3, 2)
    # TODO:  List of CWD files (with change directory functions...up, back, etc.)
    # TODO:  Ability to transfer multiple files by selecting (multi-select)
    # TODO:  File transfer size checker / time estimator for sanity check
    # TODO:  "Transfer File" button with right arrow icon
    # TODO:  List of available nodes to transfer file to
    # TODO:  Error dialog if no file/node selected
    # TODO:  One-to-many file transfer
    # TODO:  Right-click menu functionality for file transfer
    # TODO:  File transfer progress bar in status bar at bottom of window
    # TODO:  Frame with inset label on both ListWidgets
    self.filexfr.setLayout(self.filexfr.layout)

    # ---Node List Tab--- #
    self.nodelist.layout = QGridLayout()
    self.nodelist.layout.setHorizontalSpacing(10)
    self.nodelist.layout.setVerticalSpacing(10)
    self.nodes = QListWidget(self)
    self.nodelist.layout.addWidget(self.nodes, 1, 1, 5, 5)    
    # TODO:  Node list use TableLayout function vs. indigenous mt-python text table layout?
    self.nodelist.setLayout(self.nodelist.layout)

    # ---Node Map Tab--- #
    map_page = QWebEngineView()
    map_page.setUrl(QUrl.fromLocalFile("map.html"))

    # ---Set Tab Layout--- #
    self.layout.addWidget(self.tabs)

    # ---Tab Actions--- #
  def sendMsg(self, msgtxt):
    """Send a text message to another user."""
        

class configDialog(QWidget):
  """User interface to control radio configuration."""
  def __init__(self):
    super().__init__()
    """Class instantiation.  Inherits attributes from QWidget."""
  # TODO:  Message - Setting for displayed message history age
  # TODO:  Message - Channel configuration for up to 8 different channels
  # TODO:  Message - Channel-specific configuration for background color, font, size, etc.
  # TODO:  Message - Save file location input (save file should save encrypted messages only)

  @Slot()
  def on_click(self):
    self.statusbar.showMessage("Sending message...", 30)
# TODO:  Add SystemTray functionality - alert on incoming messages (special emergency alert?), minimize app to system tray

class Meshtastic():
  """Class instantiation."""

  def setupSerialInterface():
    """Configures the hardware device serial interface."""
    if platform.system() == "Windows":
      # TODO:  Read Windows USB device list, identify COM port associated with MT VID/PID, update devPath
      self.i = meshtastic.SerialInterface(devPath="COM3")
      print(f'Found WindowsOS.  Meshtastic serial interface set.')
    elif platform.system() == "Linux":
      self.i = meshtastic.SerialInterface()
      print(f'Found LinuxOS.  Meshtastic serial interface set.')
    elif plaform.system() == "macOS":
      self.i = meshtastic.SerialInterface()
      print(f'Found macOS. Meshtastic serial interface set.')
    else:
      print(f'Platform system type requires manual SerialInterface configuration.')
      # EDIT THE LINE BELOW TO POINT YOUR OS TO THE CORRECT devPath FOR YOUR MESHTASTIC HARDWARE
      self.i = meshtastic.SerialInterface()
    return self.i

    def sendText(msgtxt):
      """Send a plain text message."""
      self.i.sendText(msgtxt)
      self.i.close()   

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = App()
  m = Meshtastic()
  sys.exit(app.exec())
    
 
