#!/usr/bin/python
#
# Natural Language Processing of Archimate Information
#
__author__ = u'morrj140'
__VERSION__ = u'0.1'

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

from Constants import *
from ArchiLib import ArchiLib


class AnalyzeNamedEntities(object):

    fileArchimate           = None
    ffileRelationsConcepts  = None
    al                      = None

    def __init__(self, fileArchimate, fileConceptsRelations):

        self.fileArchimate = fileArchimate
        self.fileConceptsRelations = fileConceptsRelations

        logger.info(u"Archimate File : %s" % self.fileArchimate)
        logger.info(u"Export File    : %s" % self.fileConceptsRelations)

        self.al = ArchiLib(self.fileArchimate)

    def analyzeNamedEntities(self):
        rels = (u"archimate:AccessRelationship", u"archimate:SpecialisationRelationship",
                        u"archimate:CompositionRelationship", u"archimate:AggregationRelationship")

        listType = (u"archimate:Requirement",)

        dictEntities = self.al.getTypeNodes(listType)

        concepts = Concepts(u"Entities", u"BusinessObject")

        for x in self.al.dictEdges.keys():
            try:
                logger.debug(u"[%s]=%s" % (x, self.al.dictEdges[x][ARCHI_TYPE]))

                source = self.al.dictEdges[x][u"source"]
                target = self.al.dictEdges[x][u"target"]

                logger.debug(u"  Source : %s" % source)
                logger.debug(u"  Target : %s" % target)
            except:
                logger.warn(u"[%s] ARCH_TYPE Exception" % (x))
                continue

            if self.al.dictEdges[x][ARCHI_TYPE] in rels:
                logger.info(u"%s   ->  [ %s ]  ->   %s" % (self.al.dictNodes[source][u"name"][:20],
                                                          self.al.dictEdges[x][ARCHI_TYPE],
                                                          self.al.dictNodes[target][u"name"][:20]))

                listNodes = self.al.getEdgesForNode(source, rels)
                for x in listNodes:
                    logger.debug(u"    %s" % (x))


        Concepts.saveConcepts(concepts, fileConceptsRelations)


def test_AnalyzeNamedEntities():

    start_time = ArchiLib.startTimer()

    ane = AnalyzeNamedEntities(fileArchimateTest, fileConceptsRelations)

    ane.analyzeNamedEntities()

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":
    test_AnalyzeNamedEntities()