#!/usr/bin/python
#
# Archimate Deduping
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.DedupArchimateXML import *
from al_lib.ArchiLib import ArchiLib
from al_lib.Constants import *

def dedupArchi(fileArchimate, fileOutput=u"deduped.archimate"):

    al = ArchiLib(fileArchimate)

    ae = al.findElements()

    logger.info(u"Length : %d" % len(ae))

    dupElements = findDups(ae)

    tde = logDupElements(dupElements)

    replaceDuplicateElements(al, tde)

    replaceDuplicateProperties(al)

    al.outputXMLtoFile(fileOutput)

if __name__ == u"__main__":

    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v50.archimate"

    fileOutput = u"deduped.archimate"

    dedupArchi(fileArchimate, fileOutput=u"deduped.archimate")