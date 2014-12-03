#!/usr/bin/python
#
# Archimate to Concepts
#
import sys
import os
import StringIO
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

import al_ArchiLib as al

def folderConcepts(tree, concepts):
    r = tree.xpath('folder')

    for x in r:

        folder = str(x.get("name")).strip()

        logger.debug("folder : %s" % (folder))

        se = tree.xpath("folder[@name='%s']" % (folder))

        for element in se:
            createConcepts(concepts, element)

    #concepts.logConcepts()

def conceptAttributes(c, el, n):
    n = n + 1
    spaces = " " * n

    attrib = el.attrib

    d = c.addConceptKeyType("Attributes", "Attribute")

    attributes = el.attrib
    for atr in attributes.keys():
        logger.info("%sAttributes[%s]=%s" % (spaces, atr, attributes[atr] ))
        d.addConceptKeyType(atr, attributes[atr])

    if el.tag == 'Documentation':
        d.addConceptKeyType(el.text, "Text")

def createConcepts(concept, el, i=10, n=1):
    if i == 0:
        return

    spaces = " " * n
    i = i - 1

    id = el.get("id")
    tag = el.tag

    if id != None:
        c = concept.addConceptKeyType(id, tag)
    else:
        c = concept.addConceptKeyType(tag, tag)

    logger.info("%s%s[%s]" % (spaces, c.name, c.typeName))

    conceptAttributes(c, el, n+1)

    for elm in el:
        createConcepts(c, elm, i, n+1)

def createArchimate(fileArchiModel, fileArchiP):
    archi = Concepts.loadConcepts(fileArchiP)

    rootName = etree.QName(al.ARCHIMATE_NS, 'model')
    root = etree.Element(rootName, version="2.6.0", name=fileArchiP ,id="02cec69f", nsmap=al.NS_MAP)
    xmlSheet = etree.ElementTree(root)

    createArchimateElements(xmlSheet, archi, root)

    output = StringIO.StringIO()
    xmlSheet.write(output, pretty_print=True)

    logger.info("%s" % (output.getvalue()))

    f = open(fileArchiModel,'w')
    f.write(output.getvalue())
    f.close()

    output.close()

def createArchimateElements(xmlSheet, archi, root, n=1):

    spaces = " " * n

    cd = archi.getConcepts().values()

    for x in cd:
        logger.debug("%s%s:%s" % (spaces, x.typeName, x.name))

        if x.typeName != "Attribute":

            tag = x.typeName
            id = x.name
            attrib = x.getConcepts()["Attributes"]

            ad = dict()
            for y in attrib.getConcepts().values():
                for z in attrib.getConcepts().values():
                    ad[z.name]  = z.typeName

            element = etree.SubElement(root, tag, ad)

            createArchimateElements(xmlSheet, x, element)

if __name__ == "__main__":
    fileArchiP = "archi.p"
    fileArchiModel = 'archi.archimate'

    #fileArchimate = "/Users/morrj140/Development/GitRepository/DirCrawler/DNX Phase 2 0.9.archimate"
    #fileArchimate = "/Users/morrj140/PycharmProjects/ArchiConcepts/CodeGen_v10.archimate"
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v10.archimate"

    p, fname = os.path.split(fileArchimate)

    logger.info("Using : %s" % fileArchimate)

    concepts = Concepts(fname, "Archimate")

    tree = etree.parse(fileArchimate)

    #print_folder(tree, "Relations")
    #print_types(tree, "type")

    #
    # Create Concepts from Arhimate
    #
    folderConcepts(tree, concepts)
    Concepts.saveConcepts(concepts, "archi.p")

    #
    # Generate Archimate from Concepts
    #
    #output = createArchimate(fileArchiModel, fileArchiP)

