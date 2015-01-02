#!/usr/bin/python
#
# Named Entity Analysis
#
__author__ = 'morrj140'

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

from al_ArchiLib import *

logger.setLevel(logging.INFO)

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v16.archimate"
    #fileExport="report" + time.strftime("%Y%d%m_%H%M%S") +".csv"
    fileExport="report.csv"
    fileConcepts = "req.p"

    al = ArchiLib(fileArchimate, fileExport)

    al.logTypeCounts()

    rels = ("archimate:AccessRelationship", "archimate:SpecialisationRelationship",
                    "archimate:CompositionRelationship", "archimate:AggregationRelationship")

    listType = ("archimate:BusinessObject", "archimate:BusinessObject")
    dictEntities = al.getTypeNodes(listType)

    concepts = Concepts("Entities", "BusinessObject")

    for x in al.dictEdges.keys():
        try:
            logger.debug("[%s]=%s" % (x, al.dictEdges[x][ARCHI_TYPE]))
        except:
            logger.warn("[%s]-%s ARCH_TYPE Exception" % (x, al.dictNodes[x]))

        source = al.dictEdges[x]["source"]
        target = al.dictEdges[x]["target"]

        logger.debug("  Source : %s" % source)
        logger.debug("  Target : %s" % target)

        if al.dictEdges[x][ARCHI_TYPE] in al.relations:
            logger.info("%s   ->  [ %s ]  ->   %s" % (al.dictNodes[source]["name"][:20],
                                                      al.dictEdges[x][ARCHI_TYPE],
                                                      al.dictNodes[target]["name"][:20]))

            listNodes = al.getEdgesForNode(source, rels)
            for x in listNodes:
                logger.debug("    %s" % (x))

    if False:
        al.logTypeCounts()