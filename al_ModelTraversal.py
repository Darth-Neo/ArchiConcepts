#!/usr/bin/python
#
# Archimate Model to Concepts
#
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

from al_ArchiLib import *

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

def cvsLists(lc, dictArchimate, f, n=0):
    n += 1

    logger.info("%s[%s]" % (lc, type(lc)))

    for p in lc:
        if n== 20:
            logger.warn("recursion too long")
            return

        elif len(p) == 2 and isinstance(p[0], str) and isinstance(p[1], str):
            n = getColumn(p[1], dictArchimate)
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

def getColumn(s, dictArchimate):
    if dictArchimate.has_key(s):
        n = dictArchimate[s]
    else:
        n = 0
    return n

def listNode(tree, ID, n):

    node = findElementByID(tree, ID)[0]

    spaces = " " * n

    logger.debug("%sS%d:%s[%s]" % (spaces, n, node.get("name"), node.get(ARCHI_TYPE)))

    cl = list()
    cl.append(node.get("name"))
    cl.append(node.get(ARCHI_TYPE))
    return cl

def recurseNodes(tree, childID, clc, depth = 4):

    if depth == 0:
        return
    else:
        depth -= 1

    spaces = " " * depth

    sr = findRelationsByID(tree, childID)

    logger.debug("%slen sr : %d" % (spaces, len(sr)))

    for x in sr:
        logger.debug("%s%s" % (spaces, x.get(ARCHI_TYPE)[10:]))

        # find everything I point to
        if x.get("source") == childID:
            targetID = x.get("target")
            cl = listNode(tree, targetID, depth)
            clc.append(cl)
            cl = recurseNodes(tree, targetID, clc, depth)

        # find everything pointing to me
        elif False: #x.get("target") == childID:
            sourceID = x.get("source")
            cl = listNode(tree, sourceID, depth)
            clc.append(cl)

    logger.debug("%s---end[%d]---" % (spaces, depth))

    return clc

def savePickleList(l, cfile):
    logger.debug("Save %s" % (cfile))
    cf = open(cfile, "wb")
    pickle.dump(listConcepts, cf)
    cf.close()

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v15.archimate"
    p, fname = os.path.split(fileArchimate)
    logger.info("Using : %s" % fname)

    etree.QName(ARCHIMATE_NS, 'model')
    tree = etree.parse(fileArchimate)

    dictArchimate = {"archimate:BusinessObject" : 1,
                     "archimate:BusinessEvent" : 2,
                     "archimate:BusinessProcess" : 3,
                     "archimate:ApplicationService" : 4,
                     "archimate:DataObject" : 5,
                     "archimate:Requirement" : 6,
                     "archimate:ApplicationComponent" : 7,
                     "archimate:ApplicationFunction" : 8,
                     "archimate:BusinessActor" : 9,
                     "archimate:BusinessInterface" : 10}

    #nameModel = "All Scenarios"
    #nameModel = "Business Concepts"
    #nameModel = "Service Context - ToBe"
    #nameModel = "Business Requirement Topics"
    nameModel = "System of Record"

    fileOut=nameModel + "_" + time.strftime("%Y%d%m_%H%M%S") +" .csv"

    model = findDiagramModelByName(tree, nameModel)

    listConcepts = list()

    children = model.getchildren()

    for x in children:
        childID = x.get("archimateElement")
        z = findElementByID(tree, childID)[0]

        logger.info("%s[%s]" % (z.get("name"), z.get(ARCHI_TYPE)))

        cl = list()
        cl.append(z.get("name"))
        cl.append(z.get(ARCHI_TYPE))
        listConcepts.append(cl)

        recurseNodes(tree, childID, listConcepts)

    listTitle = dictArchimate.items()
    lt = sorted(listTitle, key=lambda x : x[1])

    f = open(fileOut,'w')

    for x in lt:
        f.write("%s," % x[0])
    f.write("\n")

    cfile = "ModelTraversal.p"
    savePickleList(listConcepts, cfile)

    cvsLists(listConcepts, dictArchimate, f)

    f.close()
    logger.info("Saved CSV to %s" % fileOut)


