#!/usr/bin/python
#
# Archimate to Concepts
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib

def createArchimateConcepts(fileArchimate, fileConceptsArch):

    logger.info(u"Using : %s" % fileArchimate)

    concepts = Concepts(fileArchimateModel, u"Archimate")

    al = ArchiLib(fileArchimate)

    al.logTypeCounts()

    #
    # Create Concepts from Archimate
    #
    al.folderConcepts(concepts)
    Concepts.saveConcepts(concepts, fileConceptsArch)
    logger.info(u"Saved concepts to : %s" % fileConceptsArch)

    #
    # Generate Archimate from Concepts
    #
    #al.createArchimate(fileArchimate, fileConceptsArch)

if __name__ == u"__main__":

    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v40.archimate"

    createArchimateConcepts(fileArchimate, fileConceptsArch)