
#!/usr/bin/python
#
# Archimate to export a model
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import time
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from al_ArchiLib import *

def al_ExportArchiModel():

    al = ArchiLib()

    logger.info("Using : %s" % fileArchimate)

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

    listMTE.append("To-Be DAM Functional Reference Architecture")
    concepts = Concepts("Export", "Model")

    for ModelToExport in listMTE:
        al.recurseModel(ModelToExport, concepts)

    Concepts.saveConcepts(concepts, "Estimation.p")

    al.outputCSVtoFile(concepts)

if __name__ == "__main__":
    al_ExportArchiModel()