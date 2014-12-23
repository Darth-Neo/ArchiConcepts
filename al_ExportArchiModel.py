
#!/usr/bin/python
#
# Archimate to export a model
#
__author__ = 'morrj140'
import sys
import os
import StringIO
import time
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from al_ArchiLib import *

if __name__ == "__main__":

    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v16.archimate"
    fileExport="export" + time.strftime("%Y%d%m_%H%M%S") +" .csv"

    al = ArchiLib(fileArchimate, fileExport)

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
    listMTE.append("System of Record")

    concepts = Concepts("Export", "Model")

    for ModelToExport in listMTE:
        al.recurseModel(ModelToExport, concepts)

    Concepts.saveConcepts(concepts, "Estimation.p")

    al.outputCSVtoFile(concepts)
