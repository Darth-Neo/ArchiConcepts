#!/usr/bin/python
#
# Archimate to Concepts
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from lxml import etree

from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib


def importWSDL():

    start_time = ArchiLib.startTimer()

    etree.QName(ArchiLib.ARCHIMATE_NS, u'model')
    treeArchi = etree.parse(fileArchimateTest)

    al = ArchiLib()

    dirWSDL = u"/Users/morrj140/Documents/SolutionEngineering/Jawa/Jawa_v2_rc37"

    for root, dirs, files in os.walk(dirWSDL, topdown=True):
        for name in files:
            nameFile = os.path.join(root, name)
            logger.info(u"Checking File : %s" % name)

            if nameFile[-4:].lower() == u"wsdl":
                nFile = name[:-5]
                logger.info(u"nFile : %s" % nFile)
                tree = etree.parse(nameFile)

                xp = u"//@schemaLocation"
                txp = tree.xpath(xp)

                for x in txp:
                    method = x[4:-4]
                    logger.info(u"x : %s" % method)

                    al.insertTwoColumns(treeArchi, u"Application", u"New Jawa", u"archimate:ApplicationService", nFile, method)

    al.outputXML(treeArchi)

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":
    importWSDL()