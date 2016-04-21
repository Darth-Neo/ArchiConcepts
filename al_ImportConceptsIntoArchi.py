#!/usr/bin/python
#
#  Concepts to Archimate Elements
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib

from nl_lib.Concepts import Concepts

dictConcepts = dict()


def insertConceptRelation(al, concepts, n=0):
    tag = u"element"

    n += 1
    spaces = u" " * n

    logger.info(u"%sParent:%s" % (spaces, concepts.name))

    for concept in concepts.getConcepts().values():

        logger.info(u"%sChild:%s" % (spaces, concepts.name))

        if not dictConcepts.has_key(concepts.name):
            continue
        if not dictConcepts.has_key(concept.name):
            continue

        sourceID = dictConcepts[concepts.name]
        targetID = dictConcepts[concept.name]

        logger.info(u"%s%s[%s]->%s[%s]" % (spaces, concepts.name, sourceID, concept.name, targetID))

        attrib = dict()
        attrib[u"source"] = sourceID
        attrib[u"target"] = targetID
        attrib[ARCHI_TYPE] = u"archimate:AssociationRelationship"
        al.insertRel(tag, u"Relations", attrib)

        insertConceptRelation(concept, n)


def insertConceptNode(al, concepts, subfolder, n=0):
    tag = u"element"
    folder = subfolder

    if n == 0:
        attrib = dict()
        attrib[u"name"] = concepts.name
        attrib[ARCHI_TYPE] = concepts.typeName
        al.insertNode(tag, folder, attrib)
        C_ID = attrib[u"id"]

        if not dictConcepts.has_key(concepts.name):
            dictConcepts[concepts.name] = C_ID

    n += 1
    spaces = u" " * n

    for concept in concepts.getConcepts().values():
        attrib = dict()
        attrib[u"name"] = concept.name
        attrib[ARCHI_TYPE] = concept.typeName
        al.insertNode(tag, folder, attrib)
        C_ID = attrib[u"id"]

        if concept.name not in dictConcepts:
            dictConcepts[concept.name] = C_ID

        logger.info(u"%s%s[%s].id[%s]" % (spaces, concept.name, concept.typeName, C_ID))

        insertConceptNode(concept, subfolder, n)

def importConceptsIntoArchi():

    logger.info(u"Using : %s" % fileArchimateTest)

    conceptFile = fileConceptsBatches
    logger.info(u"Loading :" + conceptFile)
    concepts = Concepts.loadConcepts(conceptFile)

    al = ArchiLib()

    # Create Subfolder
    folder = u"Implementation & Migration"
    subfolder = u"Dependancy Analysis - %s" % time.strftime(u"%Y%d%m_%H%M%S")

    attrib = dict()
    attrib[u"id"] = al.getID()
    attrib[u"name"] = subfolder
    al.insertNode(u"folder", folder, attrib)

    logger.info(u"--- Insert Nodes ---")
    insertConceptNode(al, concepts, subfolder)

    logger.info(u"--- Insert Relations ---")
    insertConceptRelation(al, concepts)

    al.outputXMLtoFile(filename=u"import_concepts.archimate")

if __name__ == u"__main__":
    importConceptsIntoArchi()