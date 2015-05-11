#!/usr/bin/python
#
# Archimate Counts
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.ArchiLib import ArchiLib


if __name__ == u"__main__":

    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v40.archimate"

    al = ArchiLib(fileArchimate)

    al.logTypeCounts()