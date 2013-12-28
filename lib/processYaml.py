#!/usr/bin/env python
"""
processYaml.py

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
import os


class processYaml():
    def __init__(self, pathFile):
        self.pathFile = pathFile
        self.fileYaml = None

    def loadFile(self):
        yaml_file = open(os.path.abspath(self.pathFile), 'r')
        self.fileYaml = load(yaml_file)
        return self.fileYaml

    def dumpFile(self):
        return dump(self.fileYaml)

    def has_key(self, key):
        self.key = key
        return self.fileYaml.has_key(self.key)

    def getValues(self):
        return self.fileYaml.values()

    def getKeys(self):
        return self.fileYaml.keys()

    def getCopy(self):
        return self.fileYaml.copy()

    def validationInterfaces(self):
        if self.fileYaml.has_key('interfaces'):
            return True
        else:
            return False

    def validationConfigure(self):
        if self.fileYaml.has_key('configuration'):
            return True
        else:
            return False

    def validationServices(self):
        if self.fileYaml.has_key('services'):
            return True
        else:
            return False

    def isValid(self):
        if self.validationConfigure():
            if self.validationInterfaces():
                if self.validationServices():
                    return True
                else:
                    print "Error - In the file " + self.pathFile + " must especify the services."
                    return False
            else:
                print "Error - In the file " + self.pathFile + " must especify the interfaces."
                return False
        else:
            print "Error - In the file " + self.pathFile + " must especify the configuration."
            return False