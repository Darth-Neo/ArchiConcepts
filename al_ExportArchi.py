#!/usr/bin/python
#
# Export Archimate to Concepts
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.ArchiLib import ArchiLib
from al_lib.ExportArchi import ExportArchi

from al_Constants import *

def exportArchi(fileArchimate, fileConceptsExport):

    start_time = ArchiLib.startTimer()

    ea = ExportArchi(fileArchimate, fileConceptsExport)

    ea.exportArchi()

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":
    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v3.16.archimate"

    exportArchi(fileArchimate, fileConceptsExport)