#!/usr/bin/python
#
# Archimate Deduping
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

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
    logger.info("Using : %s" % fileArchimate)

    concepts = Concepts(fname, "Archimate")

    al.folderConcepts(concepts)

    #concepts.logConcepts()

    #Concepts.saveConcepts(concepts, fileConceptsDeDups)

    #
    # Generate Archimate from Concepts
    #
    output = al.createArchimate(fileArchimateModel , fileConceptsArch)

if __name__ == "__main__":
    dedupArchi(fileArchimateTest)
