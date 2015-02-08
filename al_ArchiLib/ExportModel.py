
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

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib

class ExportArchiModel(object):

    def __init__(self, afileArchimate=None):

        self.al = ArchiLib()

        if afileArchimate == None:
            self.fileArchimate = fileArchimate
        else:
            self.fileArchimate = afileArchimate

    def exportArchiModel(self, listMTE):

        logger.info("Using : %s" % self.fileArchimate)
        concepts = Concepts("Export", "Model")

        for ModelToExport in listMTE:
            self.al.recurseModel(ModelToExport, concepts)

        Concepts.saveConcepts(concepts, fileEstimationConcepts)

        self.al.outputCSVtoFile(concepts)

if __name__ == "__main__":

    start_time = ArchiLib.startTimer()

    eam = ExportArchiModel()

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

    eam.exportArchiModel(listMTE)

    ArchiLib.stopTimer(start_time)