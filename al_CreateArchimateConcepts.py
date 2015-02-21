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

from al_ArchiLib.ArchiLib import ArchiLib
from al_Constants import *

def al_ArchimateConcepts():

    logger.info("Using : %s" % fileArchimate)

    concepts = Concepts(fileArchConcepts, "Archimate")

    al = ArchiLib(fileArchimate)

    al.logTypeCounts()

    #
    # Create Concepts from Archimate
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