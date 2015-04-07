
#!/usr/bin/python
#
# Archimate to export a model
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.ExportModel import ExportArchiModel

from al_Constants import *

import pytest

def exportArchiModel(fileArchimate, fileConceptsExport, model, fileCSVExport):

    start_time = ArchiLib.startTimer()

    eam = ExportArchiModel(fileArchimate, fileConceptsExport, fileCSVExport)

    listMTE = list()
    #listMTE.append("5. Contract Management")
    #listMTE.append("4. Contract Prep")
    #listMTE.append("1. Inventory Management")
    #listMTE.append("1. Resort Setup")
    #listMTE.append("4. Proposal Presentation")
    #listMTE.append("5. Contract Presentation")
    #listMTE.append("6. Contract Closing")

    #listMTE.append("All Scenarios")
    #listMTE.append("Business Concepts")
    #listMTE.append("System of Record")

    listMTE.append(model)

    eam.exportArchiModel(listMTE)

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":

    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CMS into ECM V4.archimate"
    model = "As-Is - BP Grouping"

    exportArchiModel(fileArchimate, fileConceptsExport, model, fileCSVExport)