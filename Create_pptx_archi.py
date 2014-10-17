__author__ = 'morrj140'

import sys
import os
import StringIO
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches

SLD_LAYOUT_TITLE_AND_CONTENT = 1
TITLE_ONLY_SLIDE_LAYOUT = 5

import import_artifacts as ia

namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}

XML_NS         =  "http://www.w3.org/2001/XMLSchema-instance"
ARCHIMATE_NS   =  "http://www.archimatetool.com/archimate"
NS_MAP = {"xsi": XML_NS, "archimate" : ARCHIMATE_NS}

ARCHI_TYPE = "{http://www.w3.org/2001/XMLSchema-instance}type"

DIAGRAM_MODEL = "archimate:ArchimateDiagramModel"

listModels = list()

def getNode(n, type):

    attributes = n.attrib

    if attributes.get(ARCHI_TYPE) == type:
        if attributes.get("id") != None:
            listModels.append((n, attributes))

            logger.info("%s : %s:%s:%s:%s" % (DIAGRAM_MODEL, n.tag, n.get("name"), n.get("id"), attributes.get(ARCHI_TYPE)))

    for y in n:
        getNode(y, type)

def getAll(tree, type=DIAGRAM_MODEL):
    for x in tree.getroot():
        getNode(x, type)

def findChild(tree, id):
    logger.debug("id = %s" % id)
    xp = "//element[@id='%s']" % id
    stp = tree.xpath(xp)

    if len(stp) > 0:
        return stp[0]

    return stp

if __name__ == "__main__":
    filePPTX = "Archimate.pptx"
    fileArchimateIn = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CodeGen_v23.archimate"
    etree.QName(ARCHIMATE_NS, 'model')
    tree = etree.parse(fileArchimateIn)

    ia.logAll(tree, "archimate:ApplicationComponent")

    getAll(tree)

    for x in listModels:
        logger.info("%s[%s]" % (x[0].get("name"), x[0].get("id")))

        p = "//element[@id=\"%s\"]" % (x[0].get("id"))
        r = tree.xpath(p, namespaces=namespaces)
        xc = r[0].getchildren()

        for y in xc:
            child = y.get("archimateElement")
            logger.info("  %s[%s]: child:%s" % (y.get(ARCHI_TYPE), y.get("id"), child))

            if child != None:
                n = findChild(tree, child)

                if n != None:
                    logger.info("  name = %s" % n.get("name"))

            for z in y:
                logger.debug("    attrib: %s" % (z))

            z = y.getchildren()
            for w in z:
                logger.debug("    %s[%s]" % (w.get(ARCHI_TYPE), w.get("id")))
                if w.get("x") != None:
                    logger.info("    x=%s, y=%s" % (w.get("x"), w.get("y")))











