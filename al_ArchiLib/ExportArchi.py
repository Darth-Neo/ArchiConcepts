#!/usr/bin/python
#
# Export Archimate to Concepts
#
__author__ = u'morrj140'
__VERSION__ = u'0.1'

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

        logger.info(u"Archimate File : %s" % self.fileArchimate)

        logger.info(u"Export File    : %s" % self.fileConceptsExport)

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
            if len(word) > 1 and pos[0] == u"N":
                lemmaWord = lemmatizer.lemmatize(word.lower())
                e = concepts.addConceptKeyType(lemmaWord, u"Word")
                f = e.addConceptKeyType(pos, u"POS")

    def exportArchi(self):

        m = hashlib.md5()

        concepts = Concepts(u"Node", u"Nodes")

        logger.info(u"Found %d Nodes" % len(self.al.dictNodes))
        logger.info(u"Found %d Edges" % len(self.al.dictEdges))

        count = 0
        listTSort = list()
        for x in self.al.dictEdges.keys():
            logger.debug(u"Edge [%s]=%s" % (self.al.dictEdges[x], x))

            if self.al.dictEdges[x].has_key(u"source") and self.al.dictEdges[x].has_key(u"target"):

                typeEdge = self.al.dictEdges[x][ARCHI_TYPE]
                logger.debug(u"Edge   : %s" % typeEdge)

                source = self.al.dictEdges[x][u"source"]
                logger.debug(u"Source : %s" % source)

                target = self.al.dictEdges[x][u"target"]
                logger.debug(u"Target : %s" % target)

                logger.debug(u"  Rel    : %s" % (self.al.dictEdges[x][ARCHI_TYPE]))

                sourceName = self.al.getNodeName(source)
                targetName = self.al.getNodeName(target)

                logger.debug(u" %s--%s--%s" % (sourceName, self.al.dictEdges[x][ARCHI_TYPE][10:], targetName))

                if source in self.al.dictNodes:
                    l = list()
                    sc = concepts.addConceptKeyType(sourceName, self.al.dictNodes[source][ARCHI_TYPE][10:])
                    # getWords(sourceName, sc)

                nameEdge = u"(" + sourceName + u"," + targetName + u")"
                logger.debug(u"nameEdge : %s[%d]" % (nameEdge, len(nameEdge)))
                logger.debug(u"typeEdge : %s" % typeEdge[10:])

                ne = str(self.al.cleanString(nameEdge))
                hl = hashlib.sha224(str(ne)).hexdigest()

                logger.debug(u"hash : %s" % hl)

                nh = u"%s-%s" % (typeEdge[10:], hl)

                rc = sc.addConceptKeyType(nh, typeEdge[10:])

                if self.al.dictNodes.has_key(target):
                    tc = rc.addConceptKeyType(targetName, self.al.dictNodes[target][ARCHI_TYPE][10:])
                    # getWords(sourceName, tc)

        Concepts.saveConcepts(concepts, self.fileConceptsExport)

        return concepts


def test_ExportArchi():

    start_time = ArchiLib.startTimer()

    ea = ExportArchi(fileArchimateTest, fileConceptsExport)

    ea.exportArchi()

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":
    test_ExportArchi()