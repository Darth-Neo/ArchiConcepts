#!/usr/bin/python
#
#  Clean Archimate Relationships
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.ArchiLib import ArchiLib
from al_Constants import *

from lxml import etree


def cleanArchimateRelationships():

    # fileArchimate is defined in al_Constants
    al = ArchiLib(fileArchimate)

    al.logTypeCounts()

    n = 0

    for x in al.tree.getroot().iter():
        n += 1

        if x.attrib.has_key(ARCHI_TYPE) and x.attrib[ARCHI_TYPE] in relations.values():
            logger.debug("EL : %s[%s]" % (x.get("name"), x.get(ARCHI_TYPE)))

            sid = x.get("source")
            srcElm = al.findElementByID(sid)[0]

            tid = x.get("target")
            tgtElm  = al.findElementByID(tid)[0]

            if srcElm == None or tgtElm == None:

                logger.warn("Invalid Relationship : %s[%s]" % (x.get("id"), x.get(ARCHI_TYPE)))

    logger.info("Validateds %d Elements" % n)

if __name__ == "__main__":
    cleanArchimateRelationships()
