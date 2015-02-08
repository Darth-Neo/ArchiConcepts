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
from al_ArchiLib.ArchiLib import ArchiLib as AL

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib


class TraverseNodes(object):

    def __init__(self, nameModel):

        self.fileArchimate = fileArchimate
        self.csvFileExport = csvFileExport

        self.al = ArchiLib(self.fileArchimate, self.csvfileExport)

        self.al.logTypeCounts()

        self.nameModel = nameModel

        self.fileOut=self.nameModel + "_" + time.strftime("%Y%d%m_%H%M%S") +" .csv"

        self.listConcepts = list()

    def cvsLists(self, lcf, f, n=0):
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
                self.cvsLists(p, f, n)

            elif isinstance(p, str):
                commas = "," * n
                text = "%s%s" % (commas, p)
                logger.info("%s" % text)
                f.write(text + "\n")

    def listNode(self, ID, n):

        node = self.al.findElementByID(ID)[0]

        spaces = " " * n

        logger.debug("%sS%d:%s[%s]" % (spaces, n, node.get("name"), node.get(ARCHI_TYPE)))

        cl = list()
        cl.append(node.get("name"))
        cl.append(node.get(ARCHI_TYPE))
        return cl

    def recurseNodes(self, childID, clc, depth = 4):

        if depth == 0:
            return
        else:
            depth -= 1

        spaces = " " * depth

        sr = self.al.findRelationsByID(childID)

        logger.debug("%slen sr : %d" % (spaces, len(sr)))

        for x in sr:
            logger.debug("%s%s" % (spaces, x.get(ARCHI_TYPE)[10:]))

            # find everything I point to
            if x.get("source") == childID:
                targetID = x.get("target")
                cl = self.listNode(targetID, depth)
                clc.append(cl)
                cl = self.recurseNodes(targetID, clc, depth)

            # find everything pointing to me
            elif False: #x.get("target") == childID:
                sourceID = x.get("source")
                cl = self.listNode(sourceID, depth)
                clc.append(cl)

        logger.debug("%s---end[%d]---" % (spaces, depth))

        return clc

    def savePickleList(self, l, cfile):
        logger.debug("Save %s" % (cfile))
        cf = open(cfile, "wb")
        pickle.dump(self.listConcepts, cf)
        cf.close()

    def traverse(self):

        self.model = self.al.findDiagramModelByName(self.nameModel)

        children = self.model.getchildren()

        for x in children:
            childID = x.get("archimateElement")
            z = self.al.findElementByID(childID)[0]

            logger.info("%s[%s]" % (z.get("name"), z.get(ARCHI_TYPE)))

            cl = list()
            cl.append(z.get("name"))
            cl.append(z.get(ARCHI_TYPE))
            self.listConcepts.append(cl)

            self.recurseNodes(childID)

        f = open(self.fileOut,'w')

        for x in self.listConcepts:
            f.write("%s," % x[0])
        f.write("\n")

        self.savePickleList(self.listConcepts, fileConceptsTraversal)

        self.cvsLists(self.listConcepts, f)

        f.close()
        logger.info("Saved CSV to %s" % self.self.csvfileExport)

if __name__ == "__main__":

    #nameModel = "All Scenarios"
    #nameModel = "Business Concepts"
    #nameModel = "Service Context - ToBe"
    #nameModel = "Business Requirement Topics"
    nameModel = "System of Record"

    tn = TraverseNodes(nameModel)

