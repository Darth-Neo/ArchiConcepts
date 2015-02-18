#!/usr/bin/python
#
# Named Entity Analysis
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import logging
import time
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree
import nltk

from al_Constants import *
from al_ArchiLib.ArchiLib import ArchiLib

logger.setLevel(logging.INFO)

if __name__ == "__main__":
    fileConcepts = "req.p"

    al = ArchiLib(fa="/Users/morrj140/Documents/SolutionEngineering/Archimate Models/FOS V4.archimate")

    al.logTypeCounts()

    rels = ("archimate:AccessRelationship", "archimate:SpecialisationRelationship",
                    "archimate:CompositionRelationship", "archimate:AggregationRelationship")

    listType = ("archimate:Requirement",)
    dictEntities = al.getTypeNodes(listType)

    concepts = Concepts("Entities", "BusinessObject")

    for x in al.dictEdges.keys():
        try:
            logger.debug("[%s]=%s" % (x, al.dictEdges[x][ARCHI_TYPE]))

            source = al.dictEdges[x]["source"]
            target = al.dictEdges[x]["target"]

            logger.debug("  Source : %s" % source)
            logger.debug("  Target : %s" % target)
        except:
            logger.warn("[%s] ARCH_TYPE Exception" % (x))
            continue

        if al.dictEdges[x][ARCHI_TYPE] in rels:
            logger.info("%s   ->  [ %s ]  ->   %s" % (al.dictNodes[source]["name"][:20],
                                                      al.dictEdges[x][ARCHI_TYPE],
                                                      al.dictNodes[target]["name"][:20]))

            listNodes = al.getEdgesForNode(source, rels)
            for x in listNodes:
                logger.debug("    %s" % (x))

    if False:
        al.logTypeCounts()

    Concepts.saveConcepts(concepts, fileRelationsConcepts)