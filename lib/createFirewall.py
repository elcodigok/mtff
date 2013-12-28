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
import datetime


class createFirewall():

    def __init__(self, values):
        self.filter = "/ip firewall filter "
        self.nat = "/ip firewall nat "
        self.mangle = "/ip firewall mangle "
        self.values = values

    def createFirewallHeader(self):
        print("#")
        print "# " + self.values['configuration']['product']
        print "# Date: " + str(datetime.date.today())
        print "# Author: " + self.values['configuration']['author']
        print "# Comment: " + self.values['configuration']['comment']
        print "#\n"

    def deleteRules(self):
        print "# Deleting all in NAT Rules."
        print self.nat + "remove [" + self.nat + "find]\n"
        print "# Deleting all in MANGLE Rules."
        print self.mangle + "remove [" + self.mangle + "find]\n"
        print "# Deleting all in FILTER Rules."
        print self.filter + "remove [" + self.filter + "find]\n"

    def connectionTracking(self):
        print "# Connection Tracking"
        print "/ip firewall connection tracking"
        print "set enabled=yes generic-timeout=10s icmp-timeout=10s tcp-close-timeout=10s tcp-close-wait-timeout=10s tcp-established-timeout=1d tcp-fin-wait-timeout=10s tcp-last-ack-timeout=10s tcp-syn-received-timeout=5s tcp-syn-sent-timeout=5s tcp-syncookie=no tcp-time-wait-timeout=10s udp-stream-timeout=3m udp-timeout=10s\n"

    def createInput(self):
        for inet in self.values['interfaces']:
            for i in self.values['interfaces'][inet]['services']['accept']:
                for protocol in self.values['services'][i]:
                    print self.filter + "add chain=input in-interface=" + self.values['interfaces'][inet]['ip']['name'] + " src-address=" + self.values['interfaces'][inet]['ip']['network'] + "/" + self.values['interfaces'][inet]['ip']['netmask'] + " src-port=1024-65535 protocol=" + protocol + " dst-port=" + str(self.values['services'][i][protocol]) + " action=accept comment=\"Access granted to " + i + " - " + self.values['interfaces'][inet]['ip']['name'] + "\"\n"
            for i in self.values['interfaces'][inet]['services']['deny']:
                for protocol in self.values['services'][i]:
                    print self.filter + "add chain=input in-interface=" + self.values['interfaces'][inet]['ip']['name'] + " src-address=" + self.values['interfaces'][inet]['ip']['network'] + "/" + self.values['interfaces'][inet]['ip']['netmask'] + " src-port=1024-65535 protocol=" + protocol + " dst-port=" + str(self.values['services'][i][protocol]) + " action=drop comment=\"Access denied to " + i + " - " + self.values['interfaces'][inet]['ip']['name'] + "\"\n"

    def createRouter(self):
        for router in self.values['router']:
            print "# " + router
            for i in self.values['router'][router]['services']['accept']:
                for protocol in self.values['services'][i]:
                    print self.filter + "add chain=forward in-interface=" + self.values['interfaces'][self.values['router'][router]['inface']]['ip']['name'] + " src-address=" + self.values['interfaces'][self.values['router'][router]['inface']]['ip']['network'] + "/" + self.values['interfaces'][self.values['router'][router]['inface']]['ip']['netmask'] + " out-interface=" + self.values['interfaces'][self.values['router'][router]['outface']]['ip']['name'] + " dst-address=" + self.values['interfaces'][self.values['router'][router]['outface']]['ip']['network'] + "/" + self.values['interfaces'][self.values['router'][router]['outface']]['ip']['netmask'] + " src-port=1024-65535 protocol=" + protocol + " dst-port=" + str(self.values['services'][i][protocol]) +  " action=accept comment=\"" + router + " - " + i + "\"\n"
            for i in self.values['router'][router]['services']['deny']:
                for protocol in self.values['services'][i]:
                    print self.filter + "add chain=forward in-interface=" + self.values['interfaces'][self.values['router'][router]['inface']]['ip']['name'] + " src-address=" + self.values['interfaces'][self.values['router'][router]['inface']]['ip']['network'] + "/" + self.values['interfaces'][self.values['router'][router]['inface']]['ip']['netmask'] + " out-interface=" + self.values['interfaces'][self.values['router'][router]['outface']]['ip']['name'] + " dst-address=" + self.values['interfaces'][self.values['router'][router]['outface']]['ip']['network'] + "/" + self.values['interfaces'][self.values['router'][router]['outface']]['ip']['netmask'] + " src-port=1024-65535 protocol=" + protocol + " dst-port=" + str(self.values['services'][i][protocol]) +  " action=drop comment=\"" + router + " - " + i + "\"\n"

            if 'options' in self.values['router'][router]:
                print self.nat + "add chain=srcnat out-interface=" + self.values['interfaces'][self.values['router'][router]['outface']]['ip']['name'] + " action=" + self.values['router'][router]['options'] + " src-address=" + self.values['interfaces'][self.values['router'][router]['inface']]['ip']['network'] + "/" + self.values['interfaces'][self.values['router'][router]['inface']]['ip']['netmask'] + " comment=\"Configuration NAT for " + router + "\"\n"

    def createPolicy(self):
        for inet in self.values['interfaces']:
            print self.filter + "add chain=input in-interface=" + self.values['interfaces'][inet]['ip']['name'] + " action=" + self.values['interfaces'][inet]['policy'] + " comment=\"Default Policy to " + self.values['interfaces'][inet]['ip']['name'] + " - INPUT\"\n"
            print self.filter + "add chain=forward in-interface=" + self.values['interfaces'][inet]['ip']['name'] + " action=" + self.values['interfaces'][inet]['policy'] + " comment=\"Default Policy to " + self.values['interfaces'][inet]['ip']['name'] + " - FORWARD\"\n"
            print self.filter + "add chain=forward out-interface=" + self.values['interfaces'][inet]['ip']['name'] + " action=" + self.values['interfaces'][inet]['policy'] + " comment=\"Default Policy to " + self.values['interfaces'][inet]['ip']['name'] + " - FORWARD\"\n"
            print self.filter + "add chain=output out-interface=" + self.values['interfaces'][inet]['ip']['name'] + " action=" + self.values['interfaces'][inet]['policy'] + " comment=\"Default Policy to " + self.values['interfaces'][inet]['ip']['name'] + " - OUTPUT\"\n"