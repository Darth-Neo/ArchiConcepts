#!/usr/bin/python
#
# Natural Language Processing of Concepts to Neo4J Information
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
from subprocess import call
import time
import logging
from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import Neo4JGraph
from nl_lib.Constants import *

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from al_ArchiLib import *
import al_QueryGraph as CG


def addGraphNodes(graph, concepts, n=0, threshold=1):
    n += 1
    for c in concepts.getConcepts().values():
        logger.debug("%d : %d Node c : %s:%s" % (n, len(c.getConcepts()), c.name, c.typeName))

        ArchiLib.cleanConcept(c)

        c.name = c.name.replace("\"", "'")

        graph.addConcept(c)

        if len(c.getConcepts()) > threshold:
            addGraphNodes(graph, c, n)

def addGraphEdges(graph, concepts, n=0):
    n += 1

    graph.addConcept(concepts)

    for c in concepts.getConcepts().values():

        logger.debug("%d : %d %s c : %s:%s" % (n, len(c.getConcepts()), concepts.name, c.name, c.typeName))

        ArchiLib.cleanConcept(c)

        c.name = c.name.replace("\"", "'")

        graph.addConcept(c)

        graph.addEdge(concepts, c, c.typeName)

        addGraphEdges(graph, c, n)

def logGraph(gl, title, scale=1):
    pr = 0
    len_pr = len(gl)
    sum_pr = 0.0
    try:
        logger.info("---%s---[%d]" % (title, len(gl)))

        n = 0
        for x in gl:
            n += 1
            if isinstance(gl, dict) and x != None:
                sum_pr = gl[x]
                if gl[x] > pr:
                    pr = gl[x]

                logger.info("%s [%d]:%s=%3.4f" % (title, n, x, gl[x]*scale))

            else:
                logger.info("%s [%d]" % (x, n))
    except:
        logger.warn("Ops...")

    logger.info("Len gl[x]=%3.4f" % len_pr)
    logger.info("Max gl[x]=%3.4f" % pr)
    logger.info("Avg gl[x]=%3.4f" % (sum_pr / len_pr))

def clearNeo4J():
    if gdb == LocalGBD:
        logger.info("Reset Neo4J Graph DB")
        call([resetNeo4J])

def importNeo4J(concepts, ClearNeo4J=False):

    if ClearNeo4J:
        clearNeo4J()

    logger.info("Neo4J instance : %s" % gdb)
    graph = Neo4JGraph(gdb)

    if ClearNeo4J:
        graph.clearGraphDB()

    else:
        pass

    logger.info("Adding Neo4J nodes to the graph ...")
    addGraphNodes(graph, concepts)

    logger.info("Adding Neo4J edges to the graph ...")
    addGraphEdges(graph, concepts)

    graph.setNodeLabels()

    if ClearNeo4J:
        DropNode = "MATCH (n { name: 'Node' })-[r]-() DELETE n, r"
        CG.cypherQuery(graph, DropNode)

        DropDuplicates = "match p=(n)--(r0:Relation), q=(m)--(r1:Relation) where n.name = m.name and n.typeName = m.typeName delete m, r1"
        CG.cypherQuery(graph, DropDuplicates)

    CountRequirements = "MATCH (n {typeName:'BusinessObject'}) -- m -- (o {typeName:'Requirement' }) with n, count(o) as rc  set n.RequirementCount=rc RETURN n.name, rc order by rc desc"
    CG.cypherQuery(graph, CountRequirements)

if __name__ == "__main__":

    importConcepts = Concepts.loadConcepts(fileConceptsExport)

    importNeo4J(importConcepts, ClearNeo4J=True)



    



