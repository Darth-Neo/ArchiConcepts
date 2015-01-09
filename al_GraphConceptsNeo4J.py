#!/usr/bin/python
#
# Natural Language Processing of Concepts to Neo4J Information
#
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

THRESHOLD = 1

def addGraphNodes(graph, concepts, n=0):
    n += 1
    for c in concepts.getConcepts().values():
        logger.debug("%d : %d Node c : %s:%s" % (n, len(c.getConcepts()), c.name, c.typeName))

        graph.addConcept(c)

        if len(c.getConcepts()) > THRESHOLD:
            addGraphNodes(graph, c, n)

def addGraphEdges(graph, concepts, n=0):
    n += 1

    graph.addConcept(concepts)

    for c in concepts.getConcepts().values():

        logger.debug("%d : %d %s c : %s:%s" % (n, len(c.getConcepts()), concepts.name, c.name, c.typeName))

        graph.addConcept(c)

        if isinstance(graph, Neo4JGraph):
            graph.addEdge(concepts, c, c.typeName)
        else:
            graph.addEdge(concepts, c)

        if len(c.getConcepts()) != 0:
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
                if gl[x] > 0.0005:
                    logger.info("%s [%d]:%s=%3.4f" % (title, n, x, gl[x]*scale))
            else:
                logger.info("%s [%d]" % (x, n))
    except:
        logger.warn("Ops...")

    logger.info("Len gl[x]=%3.4f" % len_pr)
    logger.info("Max gl[x]=%3.4f" % pr)
    logger.info("Avg gl[x]=%3.4f" % (sum_pr / len_pr))

def graphConcepts(concepts, filename="example.png"):

    call(["/Users/morrj140/Development/neo4j-community-2.1.2/bin/reset.sh"])

    gdb = "http://localhost:7474/db/data/"
    #gdb = "http://10.92.82.60:7574/db/data/"
    graph = Neo4JGraph(gdb)

    logger.info("Adding nodes the graph ...")
    addGraphNodes(graph, concepts)

    logger.info("Adding edges the graph ...")
    addGraphEdges(graph, concepts)


    if isinstance(graph, Neo4JGraph):
        graph.setNodeLabels()

   
if __name__ == "__main__":

    conceptFile = "export.p"

    exportConcepts = Concepts.loadConcepts(conceptFile)

    graphConcepts(exportConcepts)

    



