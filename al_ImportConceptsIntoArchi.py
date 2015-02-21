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

from al_ArchiLib.ArchiLib import ArchiLib
from al_Constants import *

dictConcepts = dict()

def insertConceptRelation(concepts, n=0):
    tag = "element"

    n += 1
    spaces = " " * n

    logger.info("%sParent:%s" % (spaces, concepts.name))

    for concept in concepts.getConcepts().values():

        logger.info("%sChild:%s" % (spaces, concepts.name))

        if not dictConcepts.has_key(concepts.name):
            continue
        if not dictConcepts.has_key(concept.name):
            continue

        sourceID = dictConcepts[concepts.name]
        targetID = dictConcepts[concept.name]

        logger.info("%s%s[%s]->%s[%s]" % (spaces, concepts.name, sourceID, concept.name, targetID))

        attrib = dict()
        attrib["source"] = sourceID
        attrib["target"] = targetID
        attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
        al.insertRel(tag, "Relations", attrib)

        insertConceptRelation(concept, n)

def insertConceptNode(concepts, subfolder, n=0):
    tag = "element"
    folder = subfolder

    if n == 0:
        attrib = dict()
        attrib["name"] = concepts.name
        attrib[ARCHI_TYPE] = concepts.typeName
        al.insertNode(tag, folder, attrib)
        C_ID = attrib["id"]

        if not dictConcepts.has_key(concepts.name):
            dictConcepts[concepts.name] = C_ID

    n += 1
    spaces = " " * n

    for concept in concepts.getConcepts().values():
        attrib = dict()
        attrib["name"] = concept.name
        attrib[ARCHI_TYPE] = concept.typeName
        al.insertNode(tag, folder, attrib)
        C_ID = attrib["id"]

        if not dictConcepts.has_key(concept.name):
            dictConcepts[concept.name] = C_ID

        logger.info("%s%s[%s].id[%s]" % (spaces, concept.name, concept.typeName, C_ID))

        insertConceptNode(concept, subfolder, n)


if __name__ == "__main__":
    logger.info("Using : %s" % fileArchimate)

    conceptFile = "batches.p"
    logger.info("Loading :" + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    al = ArchiLib()

    # Create Subfolder
    folder = "Implementation & Migration"
    subfolder = "Dependancy Analysis - %s" % time.strftime("%Y%d%m_%H%M%S")

    attrib = dict()
    attrib["id"] = al.getID()
    attrib["name"] = subfolder
    al.insertNode("folder", folder, attrib)

    logger.info("--- Insert Nodes ---")
    insertConceptNode(concepts, subfolder)

    logger.info("--- Insert Relations ---")
    insertConceptRelation(concepts)

    al.outputXMLtoFile(filename="import_concepts.archimate")
