__author__ = 'morrj140'
#!/usr/bin/python
#
# Export Archimate to Concepts
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.ExportArchi import ExportArchi

from al_Constants import *

def exportArchi(fileArchimate, fileConceptsExport):

    start_time = ArchiLib.startTimer()

    ea = ExportArchi(fileArchimate, fileConceptsExport)

    ea.exportArchi()

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":
    exportArchi(fileArchimateTest, fileConceptsExport)