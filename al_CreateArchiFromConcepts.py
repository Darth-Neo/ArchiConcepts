#!/usr/bin/python
#
# Create Archimate XML from Concepts
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
from al_ArchiLib.ConceptsImportArchi import ConceptsImportArchi

from al_Constants import *

if __name__ == "__main__":

    start_time = ArchiLib.startTimer()

    logger.info("Using : %s" % fileArchimate)
    logger.info("Loading :" + fileConceptsBatches)

    ic = ConceptsImportArchi(fileArchimate, fileConceptsBatches)

    concepts = Concepts.loadConcepts(fileConceptsBatches)

    # Create Subfolder
    folder = "Implementation & Migration"
    subfolder = "Dependancy Analysis - %s" % time.strftime("%Y%d%m_%H%M%S")


    ic.importConcepts(concepts, folder, subfolder)

    ic.exportXML()

    ArchiLib.stopTimer(start_time)


