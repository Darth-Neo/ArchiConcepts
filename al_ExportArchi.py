__author__ = 'morrj140'
#!/usr/bin/python
#
# Archimate to Dependancy Analysis
#
import sys
import os
import StringIO
import time
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

import nltk
from nltk import tokenize, tag, chunk
from nltk.corpus import webtext
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer, WordNetLemmatizer

import al_ArchiLib as al

namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}

XML_NS         =  "http://www.w3.org/2001/XMLSchema-instance"
ARCHIMATE_NS   =  "http://www.archimatetool.com/archimate"
NS_MAP = {"xsi": XML_NS, "archimate" : ARCHIMATE_NS}

ARCHI_TYPE = "{http://www.w3.org/2001/XMLSchema-instance}type"

import al_GraphConcepts as GC
dictCount = dict()

def getEdgesForNode(nodeName, searchType, dictNodes, dictEdges, n=0):
    listNodes = list()

    if n == 4:
        return listNodes
    else:
        n += 1

    for x in dictNodes.keys():
        try:
            if dictNodes[x]["name"] == nodeName:
                source = x
                break
        except:
            source = None

    for x in dictEdges.keys():
        if dictEdges[x].has_key("source"):
            if dictEdges[x]["source"] == source:
                sourceNE = dictEdges[x]["source"]
                targetNE = dictEdges[x]["target"]

                if dictNodes[targetNE][ARCHI_TYPE] in searchType:
                    spaces = " " * n
                    nodeName = getNodeName(targetNE)
                    if nodeName != "NA":
                        nn = "%s%s" % (spaces, nodeName)
                        listNodes.append(nn)

                        ln = getEdgesForNode(nodeName, searchType, dictNodes, dictEdges, n)
                        for y in ln:
                            listNodes.append(y)

    return listNodes

def countNodeType(type):
    if dictCount.has_key(type):
        dictCount[type] += 1
    else:
        dictCount[type] = 1

def getNodeName(node):
    name = " "

    try:
        logger.debug("  Node : %s" % (dictNodes[node]["name"]))
        name = dictNodes[node]["name"]
    except:
        logger.debug("Node not Found")

    return name

def getNode(el, dictAttrib):
    logger.debug("%s" % (el.tag))

    attributes = el.attrib

    # Not every node will have a type
    try:
        countNodeType(attributes["type"])
    except:
        pass

    nl = dict()
    for atr in attributes:
        nl[atr] = attributes[atr]
        logger.debug("%s = %s" % (atr, attributes[atr]))

    if nl.has_key("id"):
        dictAttrib[nl["id"]] = nl

    for elm in el:
        getNode(elm, dictAttrib)

def getEdges(tree, folder, dictAttrib):
    se = tree.xpath("folder[@name='%s']" % (folder))

    for x in se:
        getNode(x, dictAttrib)

def getFolders(tree):
    r = tree.xpath('folder')

    l = list()

    for x in r:
        l.append(x.get("name"))
        logger.debug("%s" % (x.get("name")))

    return l

def logTypeCounts():
    logger.info("Type Counts")
    listCounts = dictCount.items()
    for x in sorted(listCounts, key=lambda c: abs(c[1]), reverse=False):
        if x[1] > 1:
            logger.info("  %d - %s" % (x[1], x[0]))

    logger.info(" ")

def findConcept(concept, name, n=0):
    n += 1
    c = None

    if n == 3:
        return c

    for x in concepts.getConcepts().values():
        if x.name == name:
            return x
        else:
           c = findConcept(x, name, n)
    return c

def addToNodeDict(name, d):
    if d.has_key(name):
        d[name] += 1
    else:
        d[name] = 1

def getWords(s, concepts):
    lemmatizer = WordNetLemmatizer()

    for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(s)):
        if len(word) > 1 and pos[0] == "N":
            lemmaWord = lemmatizer.lemmatize(word.lower())
            e = concepts.addConceptKeyType(lemmaWord, "Word")
            f = e.addConceptKeyType(pos, "POS")

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CodeGen_v31.archimate"
    p, fname = os.path.split(fileArchimate)

    logger.info("Using : %s" % fileArchimate)

    tree = etree.parse(fileArchimate)

    concepts = Concepts("Node", "Nodes")

    dictNodes = dict()
    dictEdges = dict()

    listFolders = getFolders(tree)

    # Get all Nodes
    for x in listFolders:
        if x != "Views" and x != "Relations":
            logger.info("Checking Folder : %s" % (x))
            getEdges(tree, x, dictNodes)

    # Get all Edges
    getEdges(tree, "Relations", dictEdges)

    logger.info("Found %d Nodes" % len(dictNodes))
    logger.info("Found %d Edges" % len(dictEdges))

    count = 0
    listTSort = list()
    for x in dictEdges.keys():
        logger.debug("[%s]=%s" % (dictEdges[x]["id"], x))

        if dictEdges[x].has_key("source"):
            source = dictEdges[x]["source"]
            target = dictEdges[x]["target"]

            logger.debug("  Rel    : %s" % (dictEdges[x][ARCHI_TYPE]))

            countNodeType(dictNodes[source][ARCHI_TYPE])
            countNodeType(dictNodes[target][ARCHI_TYPE])
            countNodeType(dictEdges[x][ARCHI_TYPE])

            sourceName = getNodeName(source)
            targetName = getNodeName(target)

            logger.debug(" %s--%s--%s" % (sourceName, dictEdges[x][ARCHI_TYPE][10:], targetName))

            l = list()
            sc = concepts.addConceptKeyType(sourceName, dictNodes[source][ARCHI_TYPE][10:])
            #getWords(sourceName, sc)

            tc = sc.addConceptKeyType(targetName, dictNodes[target][ARCHI_TYPE][10:])
            #getWords(sourceName, tc)

    Concepts.saveConcepts(concepts, "export.p")

    if False:
        GC.graphConcepts(concepts, filename="Export.png")

    logTypeCounts()

    #concepts.logConcepts()
