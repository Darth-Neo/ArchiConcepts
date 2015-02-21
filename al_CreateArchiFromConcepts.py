#!/usr/bin/python
#
# Create Archimate XML from Concepts
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.ConceptsImportArchi import ConceptsImportArchi

from al_Constants import *

import pytest

def createArchiFromConcepts(fileArchimate, fileConceptsExport):

    logger.info("Using : %s" % fileArchimate)
    logger.info("Loading :" + fileConceptsExport)

    ic = ConceptsImportArchi(fileArchimate, fileConceptsExport)

    concepts = Concepts.loadConcepts(fileConceptsExport)

    # Create Subfolder
    folder = "Implementation & Migration"
    subfolder = "Dependancy Analysis - %s" % time.strftime("%Y%d%m_%H%M%S")

    ic.importConcepts(concepts, folder, subfolder)

    ic.exportXML()

if __name__ == "__main__":
    start_time = ArchiLib.startTimer()

    createArchiFromConcepts(fileArchimateTest, fileConceptsExport)

    ArchiLib.stopTimer(start_time)


