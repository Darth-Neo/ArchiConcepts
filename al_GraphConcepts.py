#!/usr/bin/python
#
# Natural Language Processing of PMO Information
#
import os
import logging
from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, NetworkXGraph, Neo4JGraph, GraphVizGraph
from nl_lib.Constants import *

logger = Logger.setupLogging(__name__)

import time

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

        logger.info("%d : %d %s c : %s:%s" % (n, len(c.getConcepts()), concepts.name, c.name, c.typeName))

        graph.addConcept(c)

        if isinstance(graph, Neo4JGraph):
            graph.addEdge(concepts, c, c.typeName)
        else:
            graph.addEdge(concepts, c)

        if len(c.getConcepts()) != 0:
            addGraphEdges(graph, c, n)

def graphConcepts(concepts, filename="example.png"):

    gdb = "http://localhost:7474/db/data/"
    #gdb = "http://10.92.82.60:7574/db/data/"

    if True:
        graph = Neo4JGraph(gdb)
        #logger.info("Clear the Graph @" + gdb)
        #graph.clearGraphDB()

    #graph = PatternGraph()
    #graph = NetworkXGraph()
    #graph = GraphVizGraph()

    logger.info("Adding nodes the graph ...")
    addGraphNodes(graph, concepts)

    logger.info("Adding edges the graph ...")
    addGraphEdges(graph, concepts)

    if isinstance(graph, GraphVizGraph):
        graph.exportGraph(filename=filename)
        logger.info("Saved Graph - %s" % filename)

    if isinstance(graph, Neo4JGraph):
        graph.setNodeLabels()

    if isinstance(graph, NetworkXGraph):
        #graph.drawGraph(filename)

        graph.saveGraph(filename)
        logger.info("Saved Graph - %s" % filename)
        graph.saveGraph("concepts.gml")
        
    if isinstance(graph, PatternGraph):
        logger.info("Exporting Graph")
        graph.exportGraph()
   
if __name__ == "__main__":
    conceptFile = "export.p"

    exportConcepts = Concepts.loadConcepts(conceptFile)

    graphConcepts(exportConcepts)

    



