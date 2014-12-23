#!/usr/bin/python
#
# Archimate to Concepts
#
import sys
import os
import StringIO
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

from al_ArchiLib import *

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v16.archimate"
    fileArchiP = "archi.p"
    fileArchiModel = 'archi.archimate'

    logger.info("Using : %s" % fileArchimate)

    concepts = Concepts(fileArchiP, "Archimate")

    al = ArchiLib(fileArchimate)

    al.logTypeCounts()

    #
    # Create Concepts from Arhimate
    #
    al.folderConcepts(concepts)
    Concepts.saveConcepts(concepts, fileArchiP)
    logger.info("Saved concepts to : %s" % fileArchiP)

    #
    # Generate Archimate from Concepts
    #
    #al.createArchimate(fileArchiModel, fileArchiP)

