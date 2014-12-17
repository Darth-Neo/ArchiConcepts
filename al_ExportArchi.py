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

from al_ArchiLib import *

import al_GraphConcepts as GC

dictCount = dict()


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
