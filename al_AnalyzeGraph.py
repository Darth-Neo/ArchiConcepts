#!/usr/bin/python
#
# Natural Language Processing of Archimate Information
#
import os
from subprocess import call
import time

import logging
from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, NetworkXGraph, GraphVizGraph, Neo4JGraph
from nl_lib.Constants import *
import networkx as nx

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from al_QueryGraph import *

def addGraphNodes(graph, concepts, n=0, threshold=0.0005):
    n += 1
    for c in concepts.getConcepts().values():
        logger.debug("%d : %d Node c : %s:%s" % (n, len(c.getConcepts()), c.name, c.typeName))

        graph.addConcept(c)

        if len(c.getConcepts()) > threshold:
            addGraphNodes(graph, c, n)

def addGraphEdges(graph, concepts, n=0):
    n += 1

    graph.addConcept(concepts)

    for c in concepts.getConcepts().values():

        logger.debug("%d : %d %s c : %s:%s" % (n, len(c.getConcepts()), concepts.name, c.name, c.typeName))

        graph.addConcept(c)

        graph.addEdge(concepts, c)

        if len(c.getConcepts()) != 0:
            addGraphEdges(graph, c, n)

def analyzeGraph(graph, gl, title, scale=1, threshold=0.0005):

    gNodes = graph.node

    graphNeo4J = connectNeo4J()

    pr = 0
    len_pr = len(gl)
    sum_pr = 0.0

    logger.info("---%s---[%d]" % (title, len(gl)))

    n = 0
    for x in gl:

        n += 1
        if isinstance(gl, dict) and x != None:
            sum_pr = gl[x]

            if gl[x] > pr:
                pr = gl[x]

            if gNodes[x].has_key(["typeName"]):
                typeName = gNodes[x]['typeName']

            if gl[x] > threshold:
                logger.debug("%s : %s[%s]=%3.4f" % (title, x, typeName, gl[x]*scale))

            updateNeo4J(graphNeo4J, x, typeName, title, gl[x]*scale)

            degree = nx.degree(graph)[x]

            updateNeo4J(graphNeo4J, x, typeName, "Degree", degree)

        else:
            logger.debug("%s [%d]" % (x, n))

    logger.info("Len gl[x]=%3.4f" % len_pr)
    logger.info("Max gl[x]=%3.4f" % pr)
    logger.info("Avg gl[x]=%3.4f" % (sum_pr / len_pr))

def connectNeo4J(gdb="http://localhost:7474/db/data/"):
    #gdb = "http://10.92.82.60:7574/db/data/"

    graphNeo4J = Neo4JGraph(gdb)

    return graphNeo4J

def updateNeo4J(graphNeo4J, name, typeName, metricName, metricValue):

    if len(metricName.split(" ")) > 1 :
        logger.error("metricName cannot contain spaces!")
        return

    UpdateQuery = "match (n {typeName:\"%s\", name:\"%s\"}) set n.%s = %3.4f return n" % (typeName, name, metricName, metricValue)
    logger.debug("UpdateQuery : %s" % UpdateQuery)
    cypherQuery(graphNeo4J, UpdateQuery)


def analyzeConcepts(concepts, filename="example.png", draw=False, save=False):
    graph = NetworkXGraph()
    #graph = GraphVizGraph()
    #graph = PatternGraph()

    logger.info("Adding nodes the graph ...")
    addGraphNodes(graph, concepts)

    logger.info("Adding edges the graph ...")
    addGraphEdges(graph, concepts)

    if isinstance(graph, GraphVizGraph):
        graph.exportGraph(filename=filename)
        logger.info("Saved Graph - %s" % filename)

    if isinstance(graph, NetworkXGraph):

        if draw == True:
            graph.drawGraph(filename)

        if save == True:
            graph.saveGraph(filename)
            logger.info("Saved Graph - %s" % filename)

        #gl = nx.connected_components(graph.G) # [[1, 2, 3], ['spam']]
        #analyzeGraph(graph.G, gl, "Connected")

        #gl = nx.clustering(graph.G)
        #analyzeGraph(graph.G, gl, "Cluster")

        #gl = nx.closeness_centrality(graph.G)
        #analyzeGraph(graph.G, gl, "Closeness")

        #gl = nx.betweenness_centrality(graph.G)
        #analyzeGraph(graph.G, gl, "Betweenness_Centrality")

        gl = nx.pagerank(graph.G)
        analyzeGraph(graph.G, gl, "PageRank", scale=1)

        #gl = nx.hits(graph.G)
        #analyzeGraph(graph.G, gl, "Hits")
        
    if isinstance(graph, PatternGraph):
        logger.info("Exporting Graph")
        graph.exportGraph()
   
if __name__ == "__main__":

    conceptFile = "export.p"

    exportConcepts = Concepts.loadConcepts(conceptFile)

    analyzeConcepts(exportConcepts)

    



