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

from al_ArchiLib import *

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v15.archimate"
    fileExport="report" + time.strftime("%Y%d%m_%H%M%S") +".csv"

    al = ArchiLib(fileArchimate, fileExport)

    al.logTypeCounts()

    f = open(fileExport,'w')

    outText = "\"%s\",\"%s\",\"%s\",\"%s\"\n" % ("Source Name", "Source type", "Target Name", "Target Type")

    f.write(outText)

    count = 0
    for x in al.dictEdges.keys():
        logger.debug("[%s]=%s" % (al.dictEdges[x]["id"], x))

        if al.dictEdges[x].has_key("source"):
            source = al.dictEdges[x]["source"]
            target = al.dictEdges[x]["target"]

            sourceType = al.dictNodes[source][ARCHI_TYPE]
            targetType = al.dictNodes[target][ARCHI_TYPE]

            if True:
                if sourceType in al.entities:

                    logger.info("  Source : %s[%s]" % (al.dictNodes[source]["name"], al.dictNodes[source][ARCHI_TYPE]))
                    logger.info("    Target : %s[%s]" % (al.dictNodes[target]["name"], al.dictNodes[target][ARCHI_TYPE]))

                    outText = "\"%s\",\"%s\",\"%s\",\"%s\"\n" % (al.dictNodes[source]["name"], al.dictNodes[source][ARCHI_TYPE],
                                                                 al.dictNodes[target]["name"], al.dictNodes[target][ARCHI_TYPE])
                    f.write(outText)
            else: #except:
                logger.warn("ops")

        count += 1

    logger.info("Report Saved : %s" % fileExport)

    f.close()