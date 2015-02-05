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

import al_ArchiLib as AL

def al_ExportArchiFolderModels():
    al = AL.ArchiLib()

    al.logTypeCounts()

    #conceptsFile = "Estimation" + time.strftime("%Y%d%m_%H%M%S") +".p"
    conceptsFile = "Estimation.p"

    if True:
        folder = "Scenarios"

        logger.info("Exporting Folder : %s" % folder)
        listMTE = al.getModelsInFolder(folder)

        concepts = Concepts("Export", "Pickle")

        for ModelToExport in listMTE:
            logger.info("  Model : %s" % ModelToExport)
            d = concepts.addConceptKeyType(ModelToExport, "Model")
            al.recurseModel(ModelToExport, d)

        #concepts.logConcepts()
    else:
        conceptsFile = "Estimation.p"
        concepts = Concepts.loadConcepts(conceptsFile)

    al.outputCSVtoFile(concepts)

    Concepts.saveConcepts(concepts, conceptsFile)
    logger.info("Save Concepts : %s" % conceptsFile)


if __name__ == "__main__":
    al_ExportArchiFolderModels()



