#!/usr/bin/env python

from optparse import OptionParser,OptionGroup
from lib.yaml import load,dump
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
        help="**REQUIRED** - File configuration YAML.", metavar="FILE"
    )
    parser.add_option_group(group1)

    (options, args) = parser.parse_args()

    if options.fileConfiguration is None:
        parser.print_help()
        sys.exit()

if __name__ == "__main__":
    main()
