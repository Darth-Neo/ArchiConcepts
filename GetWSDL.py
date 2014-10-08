__author__ = 'morrj140'

#!/usr/bin/python
#
# Archimate to Concepts
#
import sys
import os
import StringIO
import csv
import random
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

NS_MAP={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}
XML_NS         =  NS_MAP["xsi"]
ARCHIMATE_NS   =  NS_MAP["archimate"]

ARCHI_TYPE = "{%s}type" % NS_MAP["xsi"]

dictNode = dict()
dictRelation = dict()
dictName = dict()

def getID():
    return str(hex(random.randint(0, 16777215)))[-6:] + str(hex(random.randint(0, 16777215))[-2:])

def insertNode(tag, folder, tree, attrib):

    logger.info("attrib: %s" % (attrib))

    value = attrib["name"].lower()

    if dictName.has_key(value):
        idd = dictName[value]
        attrib["id"] = idd

        logger.debug("inFound! : %s" % idd)
    else:
        idd =  getID()
        dictName[value] = idd
        attrib["id"] = idd

        xp = "//folder[@name='" + folder + "']"
        elm = etree.Element(tag, attrib, nsmap=NS_MAP)

        txp = tree.xpath(xp)
        txp[0].insert(0, elm)
        logger.info("inNew!   : %s" % idd)

    return idd

def insertRel(tag, folder, tree, attrib):

    logger.debug("attrib: %s" % (attrib))

    value = "%s--%s" % (attrib["source"], attrib["target"])

    if dictName.has_key(value):
        idd = dictName[value]
        attrib["id"] = idd

        logger.debug("inFound! : %s" % idd)
    else:
        idd =  getID()
        dictName[value] = idd
        attrib["id"] = idd

        xp = "//folder[@name='" + folder + "']"
        elm = etree.Element(tag, attrib, nsmap=NS_MAP)
        tree.xpath(xp)[0].insert(0, elm)
        logger.info("inNew!   : %s" % idd)

    return idd


def logNode(n):

    attributes = n.attrib

    if attributes.get(ARCHI_TYPE) == "archimate:BusinessFunction":
        if attributes.get("id") != None:
            dictName[n.get("name")] = attributes["id"]

            logger.debug("logNode : %s:%s:%s:%s" % (n.tag, n.get("name"), n.get("id"), attributes.get(ARCHI_TYPE)))

    for y in n:
        logNode(y)

def logAll(tree):
    for x in tree.getroot():
        logNode(x)

def outputXML(tree, filename="import_artifacts.archimate"):
    output = StringIO.StringIO()
    tree.write(output, pretty_print=True)

    logger.debug("%s" % (output.getvalue()))

    logger.info("Saved to : %s" % filename)

    f = open(filename,'w')
    f.write(output.getvalue())
    f.close()

    output.close()

def insertTwoValues(tree, folder, subfolder, eType, v1, v2):

    #<element xsi:type="archimate:Node" id="612a9b73" name="Linux Server"/>

    xp = "//folder[@name='" + folder + "']"
    tag = "element"

    # <folder name="Process" id="e23b1e50">

    attrib = dict()
    attrib["id"] = getID()
    attrib["name"] = subfolder
    insertNode("folder", folder, tree, attrib)

    folder = subfolder

    CM1 = v1.decode(encoding='UTF-8',errors='ignore').lstrip()
    CM2 = v2.decode(encoding='UTF-8',errors='ignore').lstrip()

    C1 = CM1
    attrib = dict()
    attrib["name"] = CM1
    attrib[ARCHI_TYPE] = eType
    insertNode(tag, folder, tree, attrib)
    CM1_ID = attrib["id"]

    C2 = CM2
    attrib = dict()
    attrib["name"] = CM2
    attrib[ARCHI_TYPE] = eType
    insertNode(tag, folder, tree, attrib)
    CM2_ID = attrib["id"]

    attrib = dict()
    attrib["source"] = CM1_ID
    attrib["target"] = CM2_ID
    attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
    insertRel(tag, "Relations", tree, attrib)

if __name__ == "__main__":

    # Archimate
    fileArchimate = "//Users/morrj140/Documents/SolutionEngineering/Archimate Models/CodeGen_v16.archimate"
    etree.QName(ARCHIMATE_NS, 'model')
    treeArchi = etree.parse(fileArchimate)

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

                    insertTwoValues(treeArchi, "Application", "New Jawa", "archimate:ApplicationService", nFile, method)

    outputXML(treeArchi)