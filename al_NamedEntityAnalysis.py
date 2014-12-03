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

import al_ArchiLib as al
import al_DependancyAnalysisFromArchi as dafa

logger.setLevel(logging.INFO)

if __name__ == "__main__":
    fileArchimateIn = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC V10.archimate"
    fileOut="report" + time.strftime("%Y%d%m_%H%M%S") +" .csv"
    fileConcepts = "req.p"

    etree.QName(al.ARCHIMATE_NS, 'model')
    tree = etree.parse(fileArchimateIn)

    dictNodes = dict()
    dictEdges = dict()

    listFolders = dafa.getFolders(tree)

    # Get all Nodes
    for x in listFolders:
        if x != "Views" and x != "Relations":
            logger.info("Checking Folder : %s" % (x))
            dafa.getEdges(tree, x, dictNodes)

    # Get all Edges
    dafa.getEdges(tree, "Relations", dictEdges)

    logger.info("Found %d Nodes" % len(dictNodes))
    logger.info("Found %d Edges" % len(dictEdges))

    al.logAll(tree, type="archimate:BusinessObject")

    concepts = Concepts("Entities", "BusinessObject")

    for x in dictEdges.keys():
        logger.debug("[%s]=%s" % (dictEdges[x]["id"], x))

        try:
            source = dictEdges[x]["source"]
            target = dictEdges[x]["target"]

            dafa.countNodeType(dictNodes[source][al.ARCHI_TYPE])
            dafa.countNodeType(dictNodes[target][al.ARCHI_TYPE])
            dafa.countNodeType(dictEdges[x][al.ARCHI_TYPE])

            rels = ("archimate:AccessRelationship", "archimate:SpecialisationRelationship",
                    "archimate:CompositionRelationship", "archimate:AggregationRelationship")

            if dictEdges[x][al.ARCHI_TYPE] in rels:
                logger.info("%s   ->  [ %s ]  ->   %s" % (dictNodes[source]["name"], dictEdges[x][al.ARCHI_TYPE], dictNodes[target]["name"]))

                searchType = ("archimate:BusinessObject")
                listNodes = dafa.getEdgesForNode(dictNodes[source]["name"], searchType, dictNodes, dictEdges)
                for x in listNodes:
                    logger.debug("    %s" % (x))

        except:
            pass
            #logger.warn("Source or Target Name lookup error %s" % dictEdges[x])


    if False:
        dafa.logTypeCounts()