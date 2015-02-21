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
        tag = "element"

        n += 1
        spaces = " " * n

        logger.info("%sParent:%s" % (spaces, concepts.name))

        for concept in concepts.getConcepts().values():

            logger.info("%sChild:%s" % (spaces, concepts.name))

            if not self.dictConcepts.has_key(concepts.name):
                continue
            if not self.dictConcepts.has_key(concept.name):
                continue

            sourceID = self.dictConcepts[concepts.name]
            targetID = self.dictConcepts[concept.name]

            logger.info("%s%s[%s]->%s[%s]" % (spaces, concepts.name, sourceID, concept.name, targetID))

            attrib = dict()
            attrib["source"] = sourceID
            attrib["target"] = targetID
            attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
            self.al.insertRel(tag, "Relations", attrib)

            self.insertConceptRelation(concept, n)

    def insertConceptNode(self, concepts, subfolder, n=0):
        tag = "element"
        folder = subfolder

        if n == 0:
            attrib = dict()
            attrib["name"] = concepts.name
            attrib[ARCHI_TYPE] = concepts.typeName
            self.al.insertNode(tag, folder, attrib)
            C_ID = attrib["id"]

            if not self.dictConcepts.has_key(concepts.name):
                self.dictConcepts[concepts.name] = C_ID

        n += 1
        spaces = " " * n

        for concept in concepts.getConcepts().values():
            attrib = dict()
            attrib["name"] = concept.name
            attrib[ARCHI_TYPE] = concept.typeName
            self.al.insertNode(tag, folder, attrib)
            C_ID = attrib["id"]

            if not self.dictConcepts.has_key(concept.name):
                self.dictConcepts[concept.name] = C_ID

            logger.info("%s%s[%s].id[%s]" % (spaces, concept.name, concept.typeName, C_ID))

            self.insertConceptNode(concept, subfolder, n)

    def importConcepts(self, concepts, folder, subfolder):

        attrib = dict()
        attrib["id"] = self.al.getID()
        attrib["name"] = subfolder
        self.al.insertNode("folder", folder, attrib)

        logger.info("--- Insert Nodes ---")
        self.insertConceptNode(concepts, subfolder)

        logger.info("--- Insert Relations ---")
        self.insertConceptRelation(concepts)

    def exportXML(self):

         self.al.outputXMLtoFile(filename=self.fileConceptsImport)


def test_ConceptsImportArchi():

    start_time = ArchiLib.startTimer()

    logger.info("Using : %s" % fileArchimateTest)

    logger.info("Loading :" + fileConceptsExport)

    ic = ConceptsImportArchi(fileArchimateTest, fileConceptsExport)

    concepts = Concepts.loadConcepts(fileConceptsExport)

    # Create Subfolder
    folder = "Implementation & Migration"
    subfolder = "Dependancy Analysis - %s" % time.strftime("%Y%d%m_%H%M%S")

    ic.importConcepts(concepts, folder, subfolder)

    ic.exportXML()

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":
    test_ConceptsImportArchi()
