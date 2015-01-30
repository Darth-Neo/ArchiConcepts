#!/usr/bin/python
#
# Archimate to Concepts
#
__author__ = 'morrj140'
__VERSION__ = '0.1'
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
    fileArchConcepts = "archi.p"
    fileArchiModel = 'archi.archimate'

    logger.info("Using : %s" % fileArchimate)

    concepts = Concepts(fileArchConcepts, "Archimate")

    al = ArchiLib()

    al.logTypeCounts()

    #
    # Create Concepts from Arhimate
    #
    al.folderConcepts(concepts)
    Concepts.saveConcepts(concepts, fileArchConcepts)
    logger.info("Saved concepts to : %s" % fileArchConcepts)

    #
    # Generate Archimate from Concepts
    #
    #al.createArchimate(fileArchiModel, fileArchConcepts)

if __name__ == "__main__":
    al_ArchimateConcepts()