#!/usr/bin/python
#
# Create Archimate XML from Concepts
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.ConceptsImportArchi import ConceptsImportArchi


def createArchiFromConcepts(fileArchimate, fileConceptsImport, fileArchimateImport):

    logger.info(u"Using : %s" % fileArchimate)
    logger.info(u"Loading :" + fileConceptsImport)

    ic = ConceptsImportArchi(fileArchimate, fileConceptsImport)

    concepts = Concepts.loadConcepts(fileConceptsImport)

    # Create Subfolder
    folder = u"Implementation & Migration"
    subfolder = u"Dependancy Analysis - %s" % time.strftime(u"%Y%d%m_%H%M%S")

    ic.importConcepts(concepts, folder, subfolder)

    ic.exportXML(fileArchimateImport)

if __name__ == u"__main__":
    start_time = ArchiLib.startTimer()

    createArchiFromConcepts(fileArchimateTest, fileConceptsExport, fileArchimateImport)

    ArchiLib.stopTimer(start_time)


