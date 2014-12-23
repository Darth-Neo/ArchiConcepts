#!/usr/bin/python
#
# Archimate Export All Models in a Folder
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
from lxml import etree

def outputCSV(fileExport, listOutput):

    colDict = dict()

    f = open(fileExport,'w')

    relations = ("TriggeringRelationship",
                    "UsedByRelationship",
                    "AccessRelationship",
                    "FlowRelationship",
                    "AssignmentRelationship",
                    "AssociationRelationship")
    m = 0
    for x in listOutput:
        m += 1
        n = 0
        strLine = ""
        logger.info("listOutput[%d] = %s" % (n, x))


        for y in x.split(","):
            n += 1

            logger.info("y : %s[%d]" % (y, len(y)))

            if len(y) == 0:
                if colDict.has_key(n):
                    y = colDict[n]
            else:
                colDict[n] = y

            strLine = "%s%s," % (strLine, y)

        nl = strLine[:-1]

        logger.info("%s" % nl)
        f.write(nl + "\n")

    f.close()
    logger.info("Save Model : %s" % fileExport)


if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v16.archimate"
    #fileExport="export" + time.strftime("%Y%d%m_%H%M%S") +".csv"
    fileExport="export.csv"
    #conceptsFile = "Estimation" + time.strftime("%Y%d%m_%H%M%S") +".p"
    conceptsFile = "Estimation.p"

    if True:
        p, fname = os.path.split(fileArchimate)
        logger.info("Using : %s" % fileArchimate)
        etree.QName(ARCHIMATE_NS, 'model')

        tree = etree.parse(fileArchimate)

        folder = "Scenarios"

        logger.info("Exporting Folder : %s" % folder)
        listMTE = getModelsInFolder(tree, folder)

        concepts = Concepts("Export", "Pickle")

        for ModelToExport in listMTE:
            logger.info("  Model : %s" % ModelToExport)
            d = concepts.addConceptKeyType(ModelToExport, "Model")
            getModel(ModelToExport, d, tree)

        #concepts.logConcepts()
    else:
        conceptsFile = "Estimation.p"
        concepts = Concepts.loadConcepts(conceptsFile)

    listOutput = concepts.listCSVConcepts()

    outputCSV(fileExport, listOutput)

    Concepts.saveConcepts(concepts, conceptsFile)
    logger.info("Save Concepts : %s" % conceptsFile)



