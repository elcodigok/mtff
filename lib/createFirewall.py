#!/usr/bin/env python
"""
createFirewall.py

Copyright 2013 Daniel Maldonado

This file is part of WPHardening project.

WPHardening is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

WPHardening is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with WPHardening.  If not, see <http://www.gnu.org/licenses/>.

"""

from lib.yaml import *
from lib.processYaml import processYaml
import os

class createFirewall():
    def __init__(self, values):
        self.filter = "/ip firewall filter "
        self.nat = "/ip firewall nat "
        self.mangle = "/ip firewall mangle "
        self.values = values

    def createInput(self):
        for inet in self.values['interfaces']:
            for i in self.values['interfaces'][inet]['services']['accept']:
                for protocol in self.values['services'][i]:
                    print self.filter + "add chain=input in-interface=" + self.values['interfaces'][inet]['ip']['name'] + " src-address=" + self.values['interfaces'][inet]['ip']['network'] + "/" + self.values['interfaces'][inet]['ip']['netmask'] + " src-port=1024-65535 protocol=" + protocol + " dst-port=" + str(self.values['services'][i][protocol]) + " action=accept comment=\"Access granted to " + i + " - " + self.values['interfaces'][inet]['ip']['name'] + "\"\n"
            for i in self.values['interfaces'][inet]['services']['deny']:
                for protocol in self.values['services'][i]:
                    print self.filter + "add chain=input in-interface=" + self.values['interfaces'][inet]['ip']['name'] + " src-address=" + self.values['interfaces'][inet]['ip']['network'] + "/" + self.values['interfaces'][inet]['ip']['netmask'] + " src-port=1024-65535 protocol=" + protocol + " dst-port=" + str(self.values['services'][i][protocol]) + " action=drop comment=\"Access denied to " + i + " - " + self.values['interfaces'][inet]['ip']['name'] + "\"\n"
        