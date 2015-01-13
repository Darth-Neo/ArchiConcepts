__author__ = 'morrj140'
#!/usr/bin/python
#
# Archimate to Dependancy Analysis
#
import sys
import os
import StringIO
import time
import hashlib
import logging

from nl_lib import Logger
logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

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

def findConcept(concepts, name, n=0):
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

def al_ExportArchi():
    logger.info("Archimate File : %s" % fileArchimate)
    logger.info("Export File    : %s" % fileExport)

    p, fname = os.path.split(fileArchimate)

    m = hashlib.md5()

    logger.info("Using : %s" % fileArchimate)

    al = ArchiLib()

    al.logTypeCounts()

    concepts = Concepts("Node", "Nodes")

    logger.info("Found %d Nodes" % len(al.dictNodes))
    logger.info("Found %d Edges" % len(al.dictEdges))

    count = 0
    listTSort = list()
    for x in al.dictEdges.keys():
        logger.debug("[%s]=%s" % (al.dictEdges[x]["id"], x))

        if al.dictEdges[x].has_key("source"):
            typeEdge   = al.dictEdges[x][ARCHI_TYPE]
            source = al.dictEdges[x]["source"]
            target = al.dictEdges[x]["target"]

            logger.debug("  Rel    : %s" % (al.dictEdges[x][ARCHI_TYPE]))

            sourceName = al.getNodeName(source)
            targetName = al.getNodeName(target)

            logger.debug(" %s--%s--%s" % (sourceName, al.dictEdges[x][ARCHI_TYPE][10:], targetName))

            l = list()
            sc = concepts.addConceptKeyType(sourceName, al.dictNodes[source][ARCHI_TYPE][10:])
            #getWords(sourceName, sc)

            nameEdge = "(" + sourceName + "," + targetName + ")"
            nh = typeEdge[10:] + "-" + hashlib.sha224(nameEdge).hexdigest()

            rc = sc.addConceptKeyType(nh, typeEdge[10:])

            tc = rc.addConceptKeyType(targetName, al.dictNodes[target][ARCHI_TYPE][10:])
            #getWords(sourceName, tc)

    Concepts.saveConcepts(concepts, fileExport)
    logger.info("Concepts Saved : %s" % fileExport)

    return concepts

if __name__ == "__main__":

    al_ExportArchi()