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

namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}

XML_NS         =  "http://www.w3.org/2001/XMLSchema-instance"
ARCHIMATE_NS   =  "http://www.archimatetool.com/archimate"
NS_MAP = {"xsi": XML_NS, "archimate" : ARCHIMATE_NS}

ARCHI_TYPE = "{http://www.w3.org/2001/XMLSchema-instance}type"

def print_xml(el, i=3, n=0):
    if i==0:
        return

    spaces = " " * n
    n = n + 1

    #print("%se.%d.%s - %s" % (spaces, i, el.tag, el.text))
    print("%se.%d.%s" % (spaces, i, el.tag))

    spaces = " " * n
    n = n + 1

    #nm = el.nsmap
    #for n in nm:
    #    print("--%s = %s" % (n, nm[n]))

    attributes = el.attrib
    for atr in attributes:
        print("%sa.%d.%s = %s" % (spaces, i, atr, attributes[atr]))

    i = i - 1
    for elm in el:
        print_xml(elm, i, n)

def print_folders(tree):
    r = tree.xpath('folder')

    for x in r:
        print("%s" % (x.get("name")))

def print_folder(tree, folder):

    se = tree.xpath("folder[@name='%s']" % (folder))

    for x in se:
        print_xml(x, i=6)

def print_elements(tree):
    r = tree.getroot()

    r = tree.xpath('folder/element')

    for x in r:
        print x.get("name")

def print_id(tree, id):
    a = "id"
    p = "//child[@%s=\"%s\"]" % (a, id)
    r = tree.xpath("//@id=\"%s\"" % id, namespaces=namespaces)

    try:
        print_xml(r[0], i=1)
    except:
        print("Fail - %s" % p)

def print_types(tree, a):

    dictTypes = dict()

    r = tree.xpath("//@%s" % a, namespaces=namespaces)

    for x in r:
        if dictTypes.has_key(x):
            dictTypes[x] += 1
        else:
            dictTypes[x] = 1

    for x in dictTypes:
        logger.info("Parent - %s:ID - %s" % (x.getparent().get("name"),x.getparent().get("id")))

        p = "//element[@%s=\"%s\"]" % (a, x)
        r = tree.xpath(p, namespaces=namespaces)

        if len(r) > 0:
            print_xml(r[0], i=1)

def log_node(n):
    logger.info("%s:%s:%s" % (n.tag, n.get("name"), n.get("id")))

    for y in n:
        log_node(y)

def log_all(tree):
    #r = tree.xpath('/')

    for x in tree.getroot():
        log_node(x)

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

    rootName = etree.QName(ARCHIMATE_NS, 'model')
    root = etree.Element(rootName, version="2.6.0", name=fileArchiP ,id="02cec69f", nsmap=NS_MAP)
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

    fileArchimate = "/Users/morrj140/PycharmProjects/ArchiConcepts/CodeGen_v10.archimate"

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

