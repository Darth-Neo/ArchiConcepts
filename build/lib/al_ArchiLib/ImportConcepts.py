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

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from al_ArchiLib.Constants import *
import al_ArchiLib as AL

class ImportConcepts(object):

    def __init__(self):
        self.dictConcepts = dict()

        self.al = AL.ArchiLib()

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
        attrib[AL.ARCHI_TYPE] = "archimate:AssociationRelationship"
        self.al.insertRel(tag, "Relations", attrib)

        self.insertConceptRelation(concept, n)

def insertConceptNode(self, concepts, subfolder, n=0):
    tag = "element"
    folder = subfolder

    if n == 0:
        attrib = dict()
        attrib["name"] = concepts.name
        attrib[AL.ARCHI_TYPE] = concepts.typeName
        self.al.insertNode(tag, folder, attrib)
        C_ID = attrib["id"]

        if not self.dictConcepts.has_key(concepts.name):
            self.dictConcepts[concepts.name] = C_ID

    n += 1
    spaces = " " * n

    for concept in concepts.getConcepts().values():
        attrib = dict()
        attrib["name"] = concept.name
        attrib[AL.ARCHI_TYPE] = concept.typeName
        self.al.insertNode(tag, folder, attrib)
        C_ID = attrib["id"]

        if not self.dictConcepts.has_key(concept.name):
            self.dictConcepts[concept.name] = C_ID

        logger.info("%s%s[%s].id[%s]" % (spaces, concept.name, concept.typeName, C_ID))

        insertConceptNode(concept, subfolder, n)

if __name__ == "__main__":
    ic = ImportConcepts()

    logger.info("Using : %s" % AL.fileArchimate)

    conceptFile = AL.fileConceptsBatches
    logger.info("Loading :" + conceptFile)

    concepts = Concepts.loadConcepts(conceptFile)

    # Create Subfolder
    folder = "Implementation & Migration"
    subfolder = "Dependancy Analysis - %s" % time.strftime("%Y%d%m_%H%M%S")

    attrib = dict()
    attrib["id"] = ic.al.getID()
    attrib["name"] = subfolder
    ic.al.insertNode("folder", folder, attrib)

    logger.info("--- Insert Nodes ---")
    insertConceptNode(concepts, subfolder)

    logger.info("--- Insert Relations ---")
    insertConceptRelation(concepts)

    ic.al.outputXMLtoFile(filename=fileImportConcepts)

