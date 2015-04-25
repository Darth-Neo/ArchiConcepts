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

from al_ArchiLib.ArchiLib import ArchiLib
from al_Constants import *

import pytest

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
    createArchimateConcepts(fileArchimateTest, fileConceptsArch)