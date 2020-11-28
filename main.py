#!/usr/bin/python
import sys

from classes.parser import Parser

if __name__ == "__main__":
    systems = Parser.parse_file("launchpy.yml")
    systems[sys.argv[1]].start()
