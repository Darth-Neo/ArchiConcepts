#!/usr/bin/python
#
# Archimate Deduping
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

from al_ArchiLib.ArchiLib import ArchiLib
from al_Constants import *

def dedupArchi(fileArchimate):

    al = ArchiLib(fileArchimate)

    al.logTypeCounts()

    p, fname = os.path.split(fileArchimate)
    logger.info(u"Using : %s" % fileArchimate)

    concepts = Concepts(fname, u"Archimate")

    al.folderConcepts(concepts)

    # concepts.logConcepts()

    # Concepts.saveConcepts(concepts, fileConceptsDeDups)

    #
    # Generate Archimate from Concepts
    #
    output = al.createArchimate(fileArchimateModel, fileConceptsArch)

if __name__ == u"__main__":

    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CMS into ECM V5.archimate"

    dedupArchi(fileArchimate)
