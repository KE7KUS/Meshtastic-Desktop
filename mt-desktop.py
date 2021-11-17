#!/usr/bin/python3

# Meshtastic-Desktop
# by Kurt Kochendarfer, KE7KUS
# Python GUI client for use with Meshtastic project hardware

import meshtastic, platform

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.  You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

# -----GLOBALS----- #
# Determine the system platform to ensure the correct SerialInterface syntax is used.

def setupSerialInterface():
  if platform.system() == 'Windows':
    # TODO: Read Windows USB device list, identify COM port associated with Meshtastic VendorID/ProductID, update devPath accordingly
    i = meshtastic.SerialInterface(devPath='COM3')
  elif platform.system() == 'Linux':
    i = mesthastic.SerialInterface()
  elif platform.system == 'macOS':
    i = meshtastic.SerialInterface()
  else
    print(f'Platform system type requires manual SerialInterface configuration.')
    # EDIT THE LINE BELOW TO POINT YOUR OS TO THE CORRECT devPath FOR YOUR MESHTASTIC HARDWARE
    i = meshtastic.SerialInterface()
  return i

