#!/usr/bin/python
#
# Archimate to Dependancy Analysis
#
import sys
import os
import StringIO
import time
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

import al_ArchiLib as al

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v10.archimate"
    fileOut="report" + time.strftime("%Y%d%m_%H%M%S") +" .csv"

    p, fname = os.path.split(fileArchimate)
    logger.info("Using : %s" % fname)

    etree.QName(al.ARCHIMATE_NS, 'model')
    tree = etree.parse(fileArchimate)

    dictNodes = dict()
    dictEdges = dict()

    listFolders = al.getFolders(tree)

    # Get all Nodes
    for x in listFolders:
        if x != "Views" and x != "Relations":
            logger.info("  Checking : %s" % (x))
            al.getEdges(tree, x, dictNodes)

    # Get all Relations
    al.getEdges(tree, "Relations", dictEdges)

    f = open(fileOut,'w')

    outText = "\"%s\",\"%s\",\"%s\",\"%s\"\n" % ("Source Name", "Source type", "Target Name", "Target Type")

    f.write(outText)

    count = 0
    for x in dictEdges.keys():
        logger.debug("[%s]=%s" % (dictEdges[x]["id"], x))

        if dictEdges[x].has_key("source"):
            source = dictEdges[x]["source"]
            target = dictEdges[x]["target"]

            sourceType = dictNodes[source][al.ARCHI_TYPE]
            targetType = dictNodes[target][al.ARCHI_TYPE]

            #if dictEdges[x][ARCHI_TYPE] in ("archimate:UsedByRelationship","archimate:AssociationRelationship"):
            #if dictEdges[x][ARCHI_TYPE] in ("archimate:AssociationRelationship"):
            try:
                if sourceType in ("archimate:BusinessEvent", "archimate:BusinessObject", "archimate:BusinessProcess",
                                  "archimate:ApplicationService", "archimate:ApplicationComponent",
                                  "archimate:ApplicationData", "archimate:Requirement"):

                    logger.debug("  Source : %s[%s]" % (dictNodes[source]["name"], dictNodes[source][al.ARCHI_TYPE]))
                    logger.debug("    Target : %s[%s]" % (dictNodes[target]["name"], dictNodes[target][al.ARCHI_TYPE]))

                    outText = "\"%s\",\"%s\",\"%s\",\"%s\"\n" % (dictNodes[source]["name"], dictNodes[source][al.ARCHI_TYPE],
                                                                 dictNodes[target]["name"], dictNodes[target][al.ARCHI_TYPE])
                    f.write(outText)
            except:
                logger.warn("ops")

        count += 1


    logger.info("Report Saved : %s" % fileOut)

    f.close()