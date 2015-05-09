#!/usr/bin/python
#
#  Concepts to Archimate Elements
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import csv
import random
import time

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from ArchiLib import ArchiLib
from Constants import *

import pytest

class ConceptsImportArchi(object):
    dictConcepts       = None
    fileArchimate      = None
    fileImportConcepts = None
    al                 = None

    def __init__(self, fileArchimate, fileConceptsImport):
        self.dictConcepts = dict()

        self.fileArchimate      = fileArchimate
        self.fileConceptsImport = fileConceptsImport
        self.al = ArchiLib(self.fileArchimate)

    def insertConceptRelation(self, concepts, n=0):
        tag = u"element"

        n += 1
        spaces = u" " * n

        logger.info(u"%sParent:%s" % (spaces, concepts.name))

        for concept in concepts.getConcepts().values():

            logger.info(u"%sChild:%s" % (spaces, concepts.name))

            if not self.dictConcepts.has_key(concepts.name):
                continue
            if not self.dictConcepts.has_key(concept.name):
                continue

            sourceID = self.dictConcepts[concepts.name]
            targetID = self.dictConcepts[concept.name]

            logger.info(u"%s%s[%s]->%s[%s]" % (spaces, concepts.name, sourceID, concept.name, targetID))

            attrib = dict()
            attrib[u"source"] = sourceID
            attrib[u"target"] = targetID
            attrib[ARCHI_TYPE] = u"archimate:AssociationRelationship"
            self.al.insertRel(tag, u"Relations", attrib)

            self.insertConceptRelation(concept, n)

    def insertConceptNode(self, concepts, subfolder, n=0):
        tag = u"element"
        folder = subfolder

        if n == 0:
            attrib = dict()
            attrib[u"name"] = concepts.name
            attrib[ARCHI_TYPE] = concepts.typeName
            self.al.insertNode(tag, folder, attrib)
            C_ID = attrib[u"id"]

            if not self.dictConcepts.has_key(concepts.name):
                self.dictConcepts[concepts.name] = C_ID

        n += 1
        spaces = u" " * n

        for concept in concepts.getConcepts().values():
            attrib = dict()
            attrib[u"name"] = concept.name
            attrib[ARCHI_TYPE] = concept.typeName
            self.al.insertNode(tag, folder, attrib)
            C_ID = attrib[u"id"]

            if not self.dictConcepts.has_key(concept.name):
                self.dictConcepts[concept.name] = C_ID

            logger.info(u"%s%s[%s].id[%s]" % (spaces, concept.name, concept.typeName, C_ID))

            self.insertConceptNode(concept, subfolder, n)

    def importConcepts(self, concepts, folder, subfolder):

        attrib = dict()
        attrib[u"id"] = self.al.getID()
        attrib[u"name"] = subfolder
        self.al.insertNode(u"folder", folder, attrib)

        logger.info(u"--- Insert Nodes ---")
        self.insertConceptNode(concepts, subfolder)

        logger.info(u"--- Insert Relations ---")
        self.insertConceptRelation(concepts)

    def exportXML(self, fileArchimateImport):

         self.al.outputXMLtoFile(filename=fileArchimateImport)


def test_ConceptsImportArchi():

    start_time = ArchiLib.startTimer()

    logger.info(u"Using : %s" % fileArchimateTest)

    logger.info(u"Loading :" + fileConceptsExport)

    ic = ConceptsImportArchi(fileArchimateTest, fileConceptsExport)

    concepts = Concepts.loadConcepts(fileConceptsExport)

    # Create Subfolder
    folder = u"Implementation & Migration"
    subfolder = u"Dependancy Analysis - %s" % time.strftime(u"%Y%d%m_%H%M%S")

    ic.importConcepts(concepts, folder, subfolder)

    ic.exportXML()

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":
    test_ConceptsImportArchi()
