#!/usr/bin/python
#
# Archimate to Concepts
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import csv
import random

from lxml import etree

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib

if __name__ == "__main__":

    start_time = ArchiLib.startTimer()

    etree.QName(ARCHIMATE_NS, 'model')
    treeArchi = etree.parse(fileArchimate)

    al = ArchiLib()

    dirWSDL = "/Users/morrj140/Documents/SolutionEngineering/Jawa/Jawa_v2_rc37"

    for root, dirs, files in os.walk(dirWSDL, topdown=True):
        for name in files:
            nameFile = os.path.join(root, name)
            logger.info("Checking File : %s" % name)

            if nameFile[-4:].lower() == "wsdl":
                nFile = name[:-5]
                logger.info("nFile : %s" % nFile)
                tree = etree.parse(nameFile)

                xp = "//@schemaLocation"
                txp = tree.xpath(xp)

                for x in txp:
                    method = x[4:-4]
                    logger.info("x : %s" % method)

                    al.insertTwoColumns(treeArchi, "Application", "New Jawa", "archimate:ApplicationService", nFile, method)

    al.outputXML(treeArchi)

    ArchiLib.stopTimer(start_time)