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

def al_ArchimateConcepts():
    fileArchiP = "archi.p"
    fileArchiModel = 'archi.archimate'

    logger.info("Using : %s" % fileArchimate)

    concepts = Concepts(fileArchiP, "Archimate")

    al = ArchiLib()

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

if __name__ == "__main__":
    al_ArchimateConcepts()