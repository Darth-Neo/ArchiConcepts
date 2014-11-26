#!/usr/bin/python
#
# Archimate to Concepts
#
__author__ = 'morrj140'

import sys
import os
import StringIO
import csv
import random

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

import al_ArchiLib as al

if __name__ == "__main__":

    # Archimate
    fileArchimate = "//Users/morrj140/Documents/SolutionEngineering/Archimate Models/CodeGen_v16.archimate"
    al.etree.QName(al.ARCHIMATE_NS, 'model')
    treeArchi = al.etree.parse(fileArchimate)

    dirWSDL = "/Users/morrj140/Documents/SolutionEngineering/Jawa/Jawa_v2_rc37"

    for root, dirs, files in os.walk(dirWSDL, topdown=True):
        for name in files:
            nameFile = os.path.join(root, name)
            logger.info("Checking File : %s" % name)

            if nameFile[-4:].lower() == "wsdl":
                nFile = name[:-5]
                logger.info("nFile : %s" % nFile)
                tree = al.etree.parse(nameFile)

                xp = "//@schemaLocation"
                txp = tree.xpath(xp)

                for x in txp:
                    method = x[4:-4]
                    logger.info("x : %s" % method)

                    al.insertTwoValues(treeArchi, "Application", "New Jawa", "archimate:ApplicationService", nFile, method)

    al.outputXML(treeArchi)