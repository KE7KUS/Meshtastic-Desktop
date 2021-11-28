#!/usr/bin/python3

# Meshtastic-Desktop
# by Kurt Kochendarfer, KE7KUS
# Python GUI client for use with Meshtastic project hardware

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.  You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.


import meshtastic, platform, sys, os, folium, icons

from PySide6.QtCore import Qt, QObject, Signal, Slot, QUrl
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QLabel,
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

class MainWindow(QMainWindow):
    """Defines the Main Window GUI for the application."""
    def __init__(self):
        """Class instantiation.  Inherits attributes from QMainWindow."""
        super().__init__()
        
        self.title = "Meshtastic Desktop"
        self.left = 50
        self.top = 50
        self.width = 600
        self.height = 600
        
        self.setWindowIcon(QIcon(":/icons/mt-logo-2.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self._createActions()
        self._createMenuBar()
        self._createStatusBar()
        
        self.tab_widget = TabWidget(self)
        self.setCentralWidget(self.tab_widget)
        
        self.show()
        
    def _createActions(self):
        """Define MainWindow menu actions."""
        
        #---FILE MENU---#
        
        # New - clear the current radio configuration and set the radio to wait for a new configuration to be loaded.
        self.newAction = QAction(QIcon(":/icons/document.png"), "&New", self)
        self.newAction.setShortcut(QKeySequence.New)
        self.newAction.setStatusTip("Create a new Meshtastic node configuration file.")
        
        # Open - open an existing radio configuration file, but do not load it.
        self.openAction = QAction(QIcon(":icons/blue-folder-open-document-text.png"), "&Open...", self)
        self.openAction.setShortcut(QKeySequence.Open)
        self.openAction.setStatusTip("Open an existing Meshtastic node configuration file.")
        
        # Save - save the current configuration to the current save file - if no save file exists, open the Save As dialog
        self.saveAction = QAction(QIcon(":/icons/disk.png"), "&Save", self)
        self.saveAction.setShortcut(QKeySequence.Save)
        self.saveAction.setStatusTip("Save the configuration to the current Save file.")
        
        # Save As - save the current configuration to a new file.
        self.saveAsAction = QAction(QIcon(":/icons/disks.png"), "Save As...", self)
        self.saveAsAction.setShortcut(QKeySequence.SaveAs)
        self.saveAsAction.setStatusTip("Save the configuration to a new file...")
        
        # Exit - quit the program
        self.exitAction = QAction(QIcon(":/icons/cross.png"), "&Exit", self)
        self.exitAction.setShortcut(QKeySequence.Quit)
        self.exitAction.setStatusTip("Quit the program.")
        self.exitAction.triggered.connect(QApplication.quit)
        
        #---EDIT MENU---#
        
        # Cut
        self.cutAction = QAction(QIcon(":/icons/scissors.png"), "C&ut", self)
        self.cutAction.setShortcut(QKeySequence.Cut)
        self.cutAction.setStatusTip("Cut the selected text and save to clipboard.")
        
        # Copy
        self.copyAction = QAction(QIcon(":/icons/blue-document-copy.png"), "&Copy", self)
        self.copyAction.setShortcut(QKeySequence.Copy)
        self.copyAction.setStatusTip("Copy the selected text to the clipboard.")
        
        # Paste
        self.pasteAction = QAction(QIcon(":/icons/application--plus.png"), "&Paste", self)
        self.pasteAction.setShortcut(QKeySequence.Paste)
        self.pasteAction.setStatusTip("Paste the contents of the clipboard.")
        
        # Radio Configuration - configure the Meshtastic radio hardware
        self.radioConfigAction = QAction(QIcon(":/icons/wrench.png"), "&Radio Configuration...", self)
        self.radioConfigAction.setStatusTip("Change configuration settings for the connected Meshtastic radio.")
        
        #---HELP MENU---#
        
        # Help - open the Help dialog
        self.helpContentAction = QAction(QIcon(":/icons/lifebuoy.png"), "&Help", self)
        self.helpContentAction.setShortcut(QKeySequence.HelpContents)
        self.helpContentAction.setStatusTip("Open the embedded software documentation.")
        
        # About - open the About dialog
        self.aboutAction = QAction(QIcon(":/icons/question.png"), "&About", self)
        self.aboutAction.setStatusTip("Get information about the Meshtastic-Desktop program.")
    
    def _createMenuBar(self):
        """Constructs the program's main menu bar."""
        
        self.menuBar = self.menuBar()
        
        #---FILE MENU---#
        fileMenu = self.menuBar.addMenu("&File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)
        
        #---EDIT MENU---#
        editMenu = self.menuBar.addMenu("&Edit")
        editMenu.addAction(self.cutAction)
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addSeparator()
        editMenu.addAction(self.radioConfigAction)
        
        #---HELP MENU---#
        helpMenu = self.menuBar.addMenu("&Help")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)
        
    def _createStatusBar(self):
        """Constructs the program's status bar at the bottom of the main window."""
        
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready.", 10)

class TabWidget(QWidget):
    """Controls and interfaces for the tabbed portion of the user interface."""
    
    @Slot()
    def send_text(self, msgtxt):
        """Send Meshtastic text message."""
        print(f"Message sent: {msgtxt}")

    def __init__(self, parent):
        """Class instatiation.  Inherits attributes from QWidget."""
        super().__init__(parent)
        
        self.layout = QVBoxLayout(self)
        self.message = QWidget()
        self.filexfr = QWidget()
        self.nodelist = QWidget()
        self.nodemap = QWidget()
        
        self.tabs = QTabWidget()
        self.tabs.resize(600,600)
        
        #---MESSAGES TAB---#
        self.tabs.addTab(self.message, "&Messages")
        self.message.layout = QGridLayout()
        self.message.layout.setHorizontalSpacing(10)
        self.message.layout.setVerticalSpacing(10)
        
        self.txtWindow = QListView(self)
        # TODO:  Listen for incoming messages and display in this ListView
        # TODO:  Alternating justification (RX msgs - left justified / TX msgs - right justified)
        # TODO:  Color-differentiated bubbles for incoming text on each configured channel
        # TODO:  Display color-coding legend with configured channels below the txtInput line.
        # TODO:  Create message delete function (i.e. remove one item from ListView)
        
        self.txtInput = QLineEdit(self)
        # TODO:  Use entered text in txtInput window as text to be send when "Send Message" is clicked.
        # TODO:  Clear field and update txtWindow with sent text on "Send Message" click.
        
        self.chList = QComboBox(self)
        self.chList.isEditable = False
        self.chList.insertItems(0,"01234567")
        # TODO:  Change chList.insertItems to enumerate all configured channel names in human-readable format
        # TODO:  On selection of a channel in chList, utilize the correct PSK for that channel to send the text message
        # TODO:  Make channel selection sticky...once it's selected, use that channel until changed by the user
        
        self.sendBtn = QPushButton(QIcon(":/icons/mail--arrow.png"), "Send Message", self)
        #TODO:  On sendBtn click, send a Meshtastic text message
        self.sendBtn.clicked.connect(self.send_text("Hello World."))
        
        self.message.layout.addWidget(self.txtWindow, 1, 1, 3, 12)
        self.message.layout.addWidget(self.txtInput, 5, 1, 1, 9)
        self.message.layout.addWidget(self.chList, 5, 10, 1, 1)
        self.message.layout.addWidget(self.sendBtn, 5, 11, 1, 2)
        
        self.message.setLayout(self.message.layout)
        
        #---FILE TRANSFER TAB---#        
        self.tabs.addTab(self.filexfr, "&File Transfer")
        self.tabs.addTab(self.nodelist, "Node &List")
        self.tabs.addTab(self.nodemap, "Node Ma&p")
        
        self.layout.addWidget(self.tabs)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
        