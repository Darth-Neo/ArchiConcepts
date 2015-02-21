#!/usr/bin/python
#
# Natural Language Processing of Archimate Information
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
from subprocess import call
import time

import logging
from nl_lib import Logger
from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, NetworkXGraph, GraphVizGraph, Neo4JGraph

import networkx as nx

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.Neo4JLib import Neo4JLib

class AnalyzeNamedEntities(object):
    fileArchimate           = None
    ffileRelationsConcepts  = None
    al                      = None

    def __init__(self, fileArchimate, fileRelationsConcepts):

        self.fileArchimate = fileArchimate
        self.fileRelationsConcepts = fileRelationsConcepts

        logger.info("Archimate File : %s" % self.fileArchimate)
        logger.info("Export File    : %s" % self.fileRelationsConcepts)

        self.al = ArchiLib(fa=fileArchimate, fe=fileRelationsConcepts)

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


        Concepts.saveConcepts(concepts, fileRelationsConcepts)


if __name__ == "__main__":
    start_time = ArchiLib.startTimer()

    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v27.archimate"

    ane = AnalyzeNamedEntities(fileArchimate, fileRelationsConcepts)

    ane.analyzeNamedEntities()

    ArchiLib.stopTimer(start_time)