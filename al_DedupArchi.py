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
    fileArchiP = "archi.p"
    fileArchiModel = 'archi.archimate'
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v4.archimate"
    #fileArchimate = "/Users/morrj140/Development/GitRepository/DirCrawler/CodeGen_v5.archimate"

    p, fname = os.path.split(fileArchimate)

    logger.info("Using : %s" % fileArchimate)

    concepts = Concepts(fname, "Archimate")

    tree = etree.parse(fileArchimate)

    folderConcepts(tree, concepts)

    #concepts.logConcepts()

    #Concepts.saveConcepts(concepts, "dedup.p")

    #
    # Generate Archimate from Concepts
    #
    output = createArchimate(fileArchiModel, fileArchiP)

