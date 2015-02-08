#!/usr/bin/python
#
# Archimate Model to Concepts
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import time
import logging
import logging
import pickle

from nl_lib import Logger
from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from lxml import etree

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

def cvsLists(lcf, f, n=0):
    n += 1

    logger.info("%s[%s]" % (lcf, type(lcf)))

    for p in lcf:
        if n== 20:
            logger.warn("recursion too long")
            return

        elif len(p) == 2 and isinstance(p[0], str) and isinstance(p[1], str):
            commas = "," * n
            text = "%s%s" % (commas, p[0])
            logger.info("%s" % text)
            f.write(text + "\n")

        elif isinstance(p, list):
            cvsLists(p, f, n)

        elif isinstance(p, str):
            commas = "," * n
            text = "%s%s" % (commas, p)
            logger.info("%s" % text)
            f.write(text + "\n")

def listNode(al, ID, n):

    node = al.findElementByID(ID)[0]

    spaces = " " * n

    logger.debug("%sS%d:%s[%s]" % (spaces, n, node.get("name"), node.get(ARCHI_TYPE)))

    cl = list()
    cl.append(node.get("name"))
    cl.append(node.get(ARCHI_TYPE))
    return cl

def recurseNodes(al, childID, clc, depth = 4):

    if depth == 0:
        return
    else:
        depth -= 1

    spaces = " " * depth

    sr = al.findRelationsByID(childID)

    logger.debug("%slen sr : %d" % (spaces, len(sr)))

    for x in sr:
        logger.debug("%s%s" % (spaces, x.get(ARCHI_TYPE)[10:]))

        # find everything I point to
        if x.get("source") == childID:
            targetID = x.get("target")
            cl = listNode(al, targetID, depth)
            clc.append(cl)
            cl = recurseNodes(al, targetID, clc, depth)

        # find everything pointing to me
        elif False: #x.get("target") == childID:
            sourceID = x.get("source")
            cl = listNode(al, sourceID, depth)
            clc.append(cl)

    logger.debug("%s---end[%d]---" % (spaces, depth))

    return clc

def savePickleList(l, cfile):
    logger.debug("Save %s" % (cfile))
    cf = open(cfile, "wb")
    pickle.dump(listConcepts, cf)
    cf.close()

if __name__ == "__main__":

    al = ArchiLib(fileArchimate, fileReportExport)

    al.logTypeCounts()

    #nameModel = "All Scenarios"
    #nameModel = "Business Concepts"
    #nameModel = "Service Context - ToBe"
    #nameModel = "Business Requirement Topics"
    nameModel = "System of Record"

    fileOut=nameModel + "_" + time.strftime("%Y%d%m_%H%M%S") +" .csv"

    model = al.findDiagramModelByName(nameModel)

    listConcepts = list()

    children = model.getchildren()

    for x in children:
        childID = x.get("archimateElement")
        z = al.findElementByID(childID)[0]

        logger.info("%s[%s]" % (z.get("name"), z.get(ARCHI_TYPE)))

        cl = list()
        cl.append(z.get("name"))
        cl.append(z.get(ARCHI_TYPE))
        listConcepts.append(cl)

        recurseNodes(al, childID, listConcepts)

    f = open(fileOut,'w')

    for x in listConcepts:
        f.write("%s," % x[0])
    f.write("\n")

    cfile = "ModelTraversal.p"
    savePickleList(listConcepts, cfile)

    cvsLists(listConcepts, f)

    f.close()
    logger.info("Saved CSV to %s" % fileOut)


