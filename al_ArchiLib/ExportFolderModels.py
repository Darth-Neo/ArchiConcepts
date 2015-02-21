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
    fileArchimate      = None
    fileConceptsExport = None
    conceptsFile       = None

    def __init__(self, fa=None, fe=None):

        if fa != None:
            self.fileArchimate = fa
        else:
            self.fileArchimate = fileArchimate

        if fe != None:
            self.fileConceptsExport = fe
        else:
            self.fileConceptsExport = fileConceptsExport

        self.al = ArchiLib(self.fileArchimate, self.fileConceptsExport)

        self.conceptsFile = fileEstimationConcepts

    def exportArchiFolderModels(self, folder):

        logger.info("Exporting Folder : %s" % folder)

        listMTE = self.al.getModelsInFolder(folder)

        concepts = Concepts("Export", "Pickle")

        for ModelToExport in listMTE:
            logger.info("  Model : %s" % ModelToExport)
            d = concepts.addConceptKeyType(ModelToExport, "Model")
            self.al.recurseModel(ModelToExport, d)

        self.al.outputCSVtoFile(concepts)

        Concepts.saveConcepts(concepts, self.conceptsFile)

        logger.info("Save Concepts : %s" % self.conceptsFile)


if __name__ == "__main__":
    start_time = ArchiLib.startTimer()

    eafm = ExportArchiFolderModels()

    folder = "Scenarios"

    eafm.exportArchiFolderModels(folder)

    ArchiLib.stopTimer(start_time)


