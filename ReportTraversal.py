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

namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}

XML_NS         =  "http://www.w3.org/2001/XMLSchema-instance"
ARCHIMATE_NS   =  "http://www.archimatetool.com/archimate"
NS_MAP = {"xsi": XML_NS, "archimate" : ARCHIMATE_NS}
ARCHI_TYPE = "{http://www.w3.org/2001/XMLSchema-instance}type"


def getNode(el, dictAttrib):
    logger.debug("%s" % (el.tag))

    attributes = el.attrib

    #if attributes[ARCHI_TYPE] == "archimate:UsedByRealtionship":
    nl = dict()
    for atr in attributes:
        nl[atr] = attributes[atr]
        logger.debug("%s = %s" % (atr, attributes[atr]))

    if nl.has_key("id"):
        dictAttrib[nl["id"]] = nl

    for elm in el:
        getNode(elm, dictAttrib)

def getEdges(tree, folder, dictAttrib):
    se = tree.xpath("folder[@name='%s']" % (folder))

    for x in se:
        getNode(x, dictAttrib)

def getFolders(tree):
    r = tree.xpath('folder')

    l = list()

    for x in r:
        l.append(x.get("name"))
        logger.debug("%s" % (x.get("name")))

    return l

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CodeGen_v31.archimate"
    fileOut="report" + time.strftime("%Y%d%m_%H%M%S") +" .csv"

    p, fname = os.path.split(fileArchimate)
    logger.info("Using : %s" % fname)

    etree.QName(ARCHIMATE_NS, 'model')
    tree = etree.parse(fileArchimate)

    dictNodes = dict()
    dictEdges = dict()

    listFolders = getFolders(tree)

    # Get all Nodes
    for x in listFolders:
        if x != "Views" and x != "Relations":
            logger.info("  Checking : %s" % (x))
            getEdges(tree, x, dictNodes)

    # Get all Relations
    getEdges(tree, "Relations", dictEdges)

    f = open(fileOut,'w')

    outText = "\"%s\",\"%s\",\"%s\",\"%s\"\n" % ("Source Name", "Source type", "Target Name", "Target Type")

    f.write(outText)

    count = 0
    for x in dictEdges.keys():
        logger.debug("[%s]=%s" % (dictEdges[x]["id"], x))

        if dictEdges[x].has_key("source"):
            source = dictEdges[x]["source"]
            target = dictEdges[x]["target"]

            sourceType = dictNodes[source][ARCHI_TYPE]
            targetType = dictNodes[target][ARCHI_TYPE]

            #if dictEdges[x][ARCHI_TYPE] in ("archimate:UsedByRelationship","archimate:AssociationRelationship"):
            if dictEdges[x][ARCHI_TYPE] in ("archimate:AssociationRelationship"):
                try:
                    if sourceType in ("archimate:ApplicationService", "archimate:BusinessProcess",
                                      "archimate:ApplicationService", "archimate:ApplicationComponent",
                                      "archimate:ApplicationInterface", "archimate:Requirement"):
                        #logger.info("  Rel    : %s" % (dictEdges[x][ARCHI_TYPE]))
                        logger.info("  Source : %s[%s]" % (dictNodes[source]["name"], dictNodes[source][ARCHI_TYPE]))
                        logger.info("    Target : %s[%s]" % (dictNodes[target]["name"], dictNodes[target][ARCHI_TYPE]))

                        outText = "\"%s\",\"%s\",\"%s\",\"%s\"\n" % (dictNodes[source]["name"], dictNodes[source][ARCHI_TYPE],
                                                                     dictNodes[target]["name"], dictNodes[target][ARCHI_TYPE])
                        f.write(outText)
                except:
                    pass

        count += 1


    logger.info("Report Saved : %s" % fileOut)

    f.close()