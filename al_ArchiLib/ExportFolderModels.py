#!/usr/bin/python
#
# Archimate Export All Models in a Folder
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

from Constants import *
from ArchiLib import ArchiLib

import pytest

class ExportArchiFolderModels (object):
    fileArchimate      = None
    fileConceptsExport = None
    conceptsFile       = None

    def __init__(self, fileArchimate, fileConceptsExport):

        self.fileArchimate = fileArchimate
        self.fileConceptsExport = fileConceptsExport

        self.al = ArchiLib(self.fileArchimate)

        self.conceptsFile = fileConceptsEstimation

    def exportArchiFolderModels(self, folder):

        logger.info("Exporting Folder : %s" % folder)

        listMTE = self.al.getModelsInFolder(folder)

        concepts = Concepts("Export", "Pickle")

        for ModelToExport in listMTE:
            logger.info("  Model : %s" % ModelToExport)
            d = concepts.addConceptKeyType(ModelToExport, "Model")
            self.al.recurseModel(ModelToExport, d)

        self.al.outputCSVtoFile(concepts, fileCSVExport)

        Concepts.saveConcepts(concepts, self.conceptsFile)

        logger.info("Save Concepts : %s" % self.conceptsFile)

def test_ExportFolderModels(fileArchimate, fileConceptsExport):

    start_time = ArchiLib.startTimer()

    logger.info("Using : %s" % fileArchimate)

    eafm = ExportArchiFolderModels(fileArchimate, fileConceptsExport)

    folder = "Scenarios"

    eafm.exportArchiFolderModels(folder)

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":
    test_ExportFolderModels(fileArchimateTest, fileConceptsExport)

