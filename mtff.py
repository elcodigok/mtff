#!/usr/bin/env python
"""
mtff.py

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

from optparse import OptionParser,OptionGroup
from lib.yaml import load,dump
from lib.inputFile import inputFile
from lib.processYaml import processYaml
from lib.createFirewall import createFirewall
import os
import sys


def main():
    usage = "usage: %prog [options] arg"
    version = "MikroTik Firewall Framework version 0.1"
    parser = OptionParser(usage, version=version)
    parser.add_option(
        "-v", "--verbose", action="store_true", dest="verbose", help="active verbose mode output results.",
    )
    group1 = OptionGroup(
        parser, "Target",
        "This option must be specified to modify the package WordPress."
    )
    group1.add_option(
        "-f", "--file", dest="fileConfiguration",
        help="**REQUIRED** - File configuration YAML.", metavar="FILE",
    )
    group1.add_option(
        "-o", "--output", dest="output",
        help="Script firewall import RouterOS firewall.rsc", metavar="FILE",
    )
    parser.add_option_group(group1)

    (options, args) = parser.parse_args()

    if options.fileConfiguration is None:
        parser.print_help()
        sys.exit()
    
    asdf = inputFile(options.fileConfiguration)
    if asdf.existsFile():
        #print "buen parametro"
        qwer = processYaml(options.fileConfiguration)
        qwer.loadFile()
        if qwer.has_key('interfaces'):
            #print "seguimos bien"
            firewall = createFirewall(qwer.loadFile())
            firewall.createFirewallHeader()
            firewall.deleteRules()
            firewall.connectionTracking()
            firewall.createInput()
            firewall.createRouter()
            firewall.createPolicy()
        else:
            print "no paso la prueba"
    else:
        print "mal parametro"
        sys.exit()

if __name__ == "__main__":
    main()
