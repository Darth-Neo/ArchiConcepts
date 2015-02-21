#!/usr/bin/python
#
# Natural Language Processing of Archimate Information
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

from Constants import *
from ArchiLib import ArchiLib

import pytest

class AnalyzeNamedEntities(object):
    fileArchimate           = None
    ffileRelationsConcepts  = None
    al                      = None

    def __init__(self, fileArchimate, fileConceptsRelations):

        self.fileArchimate = fileArchimate
        self.fileConceptsRelations = fileConceptsRelations

        logger.info("Archimate File : %s" % self.fileArchimate)
        logger.info("Export File    : %s" % self.fileConceptsRelations)

        self.al = ArchiLib(self.fileArchimate)

    def analyzeNamedEntities(self):
        rels = ("archimate:AccessRelationship", "archimate:SpecialisationRelationship",
                        "archimate:CompositionRelationship", "archimate:AggregationRelationship")

        listType = ("archimate:Requirement",)

        dictEntities = self.al.getTypeNodes(listType)

        concepts = Concepts("Entities", "BusinessObject")

        for x in self.al.dictEdges.keys():
            try:
                logger.debug("[%s]=%s" % (x, self.al.dictEdges[x][ARCHI_TYPE]))

                source = self.al.dictEdges[x]["source"]
                target = self.al.dictEdges[x]["target"]

                logger.debug("  Source : %s" % source)
                logger.debug("  Target : %s" % target)
            except:
                logger.warn("[%s] ARCH_TYPE Exception" % (x))
                continue

            if self.al.dictEdges[x][ARCHI_TYPE] in rels:
                logger.info("%s   ->  [ %s ]  ->   %s" % (self.al.dictNodes[source]["name"][:20],
                                                          self.al.dictEdges[x][ARCHI_TYPE],
                                                          self.al.dictNodes[target]["name"][:20]))

                listNodes = self.al.getEdgesForNode(source, rels)
                for x in listNodes:
                    logger.debug("    %s" % (x))


        Concepts.saveConcepts(concepts, fileConceptsRelations)


def test_AnalyzeNamedEntities():

    start_time = ArchiLib.startTimer()

    ane = AnalyzeNamedEntities(fileArchimateTest, fileConceptsRelations)

    ane.analyzeNamedEntities()

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":
    test_AnalyzeNamedEntities()