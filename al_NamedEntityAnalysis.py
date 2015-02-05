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

import al_ArchiLib as AL

logger.setLevel(logging.INFO)

if __name__ == "__main__":
    fileConcepts = "req.p"

    al = AL.ArchiLib()

    al.logTypeCounts()

    rels = ("archimate:AccessRelationship", "archimate:SpecialisationRelationship",
                    "archimate:CompositionRelationship", "archimate:AggregationRelationship")

    listType = ("archimate:BusinessObject", "archimate:BusinessObject")
    dictEntities = al.getTypeNodes(listType)

    concepts = Concepts("Entities", "BusinessObject")

    for x in al.dictEdges.keys():
        try:
            logger.debug("[%s]=%s" % (x, al.dictEdges[x][AL.ARCHI_TYPE]))
        except:
            logger.warn("[%s]-%s ARCH_TYPE Exception" % (x, al.dictNodes[x]))

        source = al.dictEdges[x]["source"]
        target = al.dictEdges[x]["target"]

        logger.debug("  Source : %s" % source)
        logger.debug("  Target : %s" % target)

        if al.dictEdges[x][AL.ARCHI_TYPE] in al.relations:
            logger.info("%s   ->  [ %s ]  ->   %s" % (al.dictNodes[source]["name"][:20],
                                                      al.dictEdges[x][AL.ARCHI_TYPE],
                                                      al.dictNodes[target]["name"][:20]))

            listNodes = al.getEdgesForNode(source, rels)
            for x in listNodes:
                logger.debug("    %s" % (x))

    if False:
        al.logTypeCounts()