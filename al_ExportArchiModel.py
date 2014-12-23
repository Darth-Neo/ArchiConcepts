
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
from lxml import etree

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v16.archimate"
    fileExport="export" + time.strftime("%Y%d%m_%H%M%S") +" .csv"

    p, fname = os.path.split(fileArchimate)
    logger.info("Using : %s" % fileArchimate)
    etree.QName(ARCHIMATE_NS, 'model')

    tree = etree.parse(fileArchimate)

    f = open(fileExport,'w')
    f.write("Model, Source, Type, Relationship, Target, Type\n")

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
        getModel(ModelToExport, concepts, f, tree)

    Concepts.saveConcepts(concepts, "Estimation.p")

    f.close()
    logger.info("Save Model : %s" % fileExport)