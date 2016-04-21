#!/usr/bin/python
#
# Archimate Counts
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'
import os

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.ArchiLib import ArchiLib


if __name__ == u"__main__":

    pathModel = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models"

    fileArchimateXML = u"DVC v3.17.archimate"

    fileArchimate = pathModel + os.sep + fileArchimateXML

    al = ArchiLib(fileArchimate)

    al.logTypeCounts()