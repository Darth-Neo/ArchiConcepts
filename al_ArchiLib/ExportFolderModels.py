#!/usr/bin/python
#
# Archimate Export All Models in a Folder
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

class ExportArchiFolderModels (object):

    def __init__(self, FNT=False):
        self.al = ArchiLib()
        self.al.logTypeCounts()

        if FNT == True:
            self.conceptsFile = fileEstimationConcepts + time.strftime("%Y%d%m_%H%M%S") +".p"
        else:
            self.conceptsFile = fileEstimationConcepts

    def exportArchiFolderModels(self):

        if True:
            folder = "Scenarios"

            logger.info("Exporting Folder : %s" % folder)
            listMTE = self.al.getModelsInFolder(folder)

            concepts = Concepts("Export", "Pickle")

            for ModelToExport in listMTE:
                logger.info("  Model : %s" % ModelToExport)
                d = concepts.addConceptKeyType(ModelToExport, "Model")
                self.al.recurseModel(ModelToExport, d)

            #concepts.logConcepts()
        else:
            concepts = Concepts.loadConcepts(self.conceptsFile)

        self.al.outputCSVtoFile(concepts)

        Concepts.saveConcepts(concepts, self.conceptsFile)
        logger.info("Save Concepts : %s" % self.conceptsFile)


if __name__ == "__main__":
    eafm = ExportArchiFolderModels()
    eafm.exportArchiFolderModels()



