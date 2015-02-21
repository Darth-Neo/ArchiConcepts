#!/usr/bin/python
#
# Archimate to Concepts
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from lxml import etree

from al_ArchiLib.ArchiLib import ArchiLib
from al_Constants import *

import pytest

def importWSDL():

    start_time = ArchiLib.startTimer()


    etree.QName(ArchiLib.ARCHIMATE_NS, 'model')
    treeArchi = etree.parse(fileArchimateTest)

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

if __name__ == "__main__":
    importWSDL()