__author__ = 'morrj140'
#!/usr/bin/python
#
# Export Archimate to Concepts
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import time
import hashlib

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

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

from Constants import *
from ArchiLib import ArchiLib

import pytest

class ExportArchi(object):
    fileArchimate = None
    fileExport    = None
    al            = None

    def __init__(self, fileArchimate, fileConceptsExport):

        self.fileArchimate = fileArchimate
        self.fileConceptsExport = fileConceptsExport

        logger.info("Archimate File : %s" % self.fileArchimate)

        logger.info("Export File    : %s" % self.fileConceptsExport)

        self.al = ArchiLib(self.fileArchimate)

        self.al.logTypeCounts()

    def findConcept(self, concepts, name, n=0):
        n += 1
        c = None

        if n == 3:
            return c

        for x in concepts.getConcepts().values():
            if x.name == name:
                return x
            else:
               c = self.findConcept(x, name, n)
        return c

    def getWords(self, s, concepts):
        lemmatizer = WordNetLemmatizer()

        for word, pos in nltk.pos_tag(nltk.wordpunct_tokenize(s)):
            if len(word) > 1 and pos[0] == "N":
                lemmaWord = lemmatizer.lemmatize(word.lower())
                e = concepts.addConceptKeyType(lemmaWord, "Word")
                f = e.addConceptKeyType(pos, "POS")

    def exportArchi(self):

        m = hashlib.md5()

        concepts = Concepts("Node", "Nodes")

        logger.info("Found %d Nodes" % len(self.al.dictNodes))
        logger.info("Found %d Edges" % len(self.al.dictEdges))

        count = 0
        listTSort = list()
        for x in self.al.dictEdges.keys():
            logger.debug("Edge [%s]=%s" % (self.al.dictEdges[x], x))

            if self.al.dictEdges[x].has_key("source") and self.al.dictEdges[x].has_key("target"):

                typeEdge   = self.al.dictEdges[x][ARCHI_TYPE]
                logger.debug("Edge   : %s" % typeEdge)

                source = self.al.dictEdges[x]["source"]
                logger.debug("Source : %s" % source)

                target = self.al.dictEdges[x]["target"]
                logger.debug("Target : %s" % target)

                logger.debug("  Rel    : %s" % (self.al.dictEdges[x][ARCHI_TYPE]))

                sourceName = self.al.getNodeName(source)
                targetName = self.al.getNodeName(target)

                logger.debug(" %s--%s--%s" % (sourceName, self.al.dictEdges[x][ARCHI_TYPE][10:], targetName))

                if self.al.dictNodes.has_key(source):
                    l = list()
                    sc = concepts.addConceptKeyType(sourceName, self.al.dictNodes[source][ARCHI_TYPE][10:])
                    #getWords(sourceName, sc)

                nameEdge = "(" + sourceName + "," + targetName + ")"
                logger.debug("nameEdge : %s[%d]" % (nameEdge, len(nameEdge)))
                logger.debug("typeEdge : %s" % typeEdge[10:])

                ne = str(self.al.cleanString(nameEdge))
                hl = hashlib.sha224(str(ne)).hexdigest()

                logger.debug("hash : %s" % hl)

                nh = "%s-%s" % (typeEdge[10:], hl)

                rc = sc.addConceptKeyType(nh, typeEdge[10:])

                if self.al.dictNodes.has_key(target):
                    tc = rc.addConceptKeyType(targetName, self.al.dictNodes[target][ARCHI_TYPE][10:])
                    #getWords(sourceName, tc)

        Concepts.saveConcepts(concepts, self.fileConceptsExport)


def test_ExportArchi():

    start_time = ArchiLib.startTimer()

    ea = ExportArchi(fileArchimateTest, fileConceptsExport)

    ea.exportArchi()

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":
    test_ExportArchi()