#! /usr/bin/python
#
# Natural Language Processing of PMO Information
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
import logging
from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, NetworkXGraph, Neo4JGraph, GraphVizGraph
from nl_lib.Constants import *

import al_ArchiLib as AL
import al_ExportArchi as EA
import al_AnalyzeGraph as AG
import al_QueryGraph as QG

from py2neo.neo4j import GraphDatabaseService, CypherQuery, Node, Relationship

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

def exportNeo4JToConcepts(concepts):
    # #et all nodes
    # Match n return n limit 25

    # gdb defined in al_ArchiLib
    logger.info("Neo4J instance : %s" % AL.gdb)
    graph = Neo4JGraph(AL.gdb)

    qs = "Match n return n"

    lq, qd = QG.cypherQuery(graph, qs)

    for x in lq:
        if len(x) == 2:
            logger.info("%s[%s]" % (x[0], x[1]))
            concepts.addConceptKeyType(x[0], x[1])
        else:
            logger.warn("Not a standard node : %s" % x)

    # Match r relations
    qs = "match n-[r]-m return n, r, m"
    lq, qd = QG.cypherQuery(graph, qs)

    for x in lq:
        if len(x) == 6:
            logger.info("%s[%s]" % (x[0], x[1]))
            concepts.addConceptKeyType(x[0], x[1])
        else:
            logger.warn("Not a standard node : %s" % x)

    Concepts.saveConcepts(concepts, "Nodes.p")

if __name__ == "__main__":

    # measure process time, wall time
    start_time = AL.startTimer()

    concepts = Concepts("Neo4J", "Neo4J Graph DB")

    exportNeo4JToConcepts(concepts)

    AG.analyzeNetworkX(concepts)

    AL.stopTimer(start_time)

