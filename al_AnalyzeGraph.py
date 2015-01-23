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

from al_ArchiLib import *
import al_QueryGraph as QG

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

    # gdb is set in al_ArchiLib
    logger.info("Neo4J instance : %s" % gdb)
    graphNeo4J = Neo4JGraph(gdb)

    pr = 0
    len_pr = len(gl)
    sum_pr = 0.0

    logger.info("---%s---[%d]" % (title, len(gl)))

    n = 0
    for x in gl:

        nodeValue = gl[x]

        n += 1

        sum_pr = nodeValue

        if nodeValue > pr:
            pr = nodeValue

        nodeKey = gNodes[x]

        if isinstance(nodeKey, dict) and nodeKey.has_key("typeName"):
            typeName = nodeKey['typeName']

            if typeName in relations.keys():
                logger.debug("Skip : %s" % typeName)
                continue

            updateNeo4J(graphNeo4J, x, typeName, title, nodeValue*scale)

            degree = nx.degree(graph)[x]

            updateNeo4J(graphNeo4J, x, typeName, "Degree", degree)

            logger.info("%s : %s[%s]=%3.4f" % (title, x, typeName, nodeValue*scale))

    logger.info("Metrics for %s" % title)
    logger.info("Len gl[x]=%3.4f" % n ) #len_pr)
    logger.info("Max gl[x]=%3.4f" % pr)
    logger.info("Avg gl[x]=%3.4f" % (sum_pr / len_pr))

def updateNeo4J(graphNeo4J, name, typeName, metricName, metricValue):

    if len(metricName.split(" ")) > 1 :
        logger.error("metricName cannot contain spaces!")
        return

    UpdateQuery = "match (n {typeName:\"%s\", name:\"%s\"}) set n.%s = %3.4f return n" % (typeName, name, metricName, metricValue)
    logger.debug("UpdateQuery : %s" % UpdateQuery)
    QG.cypherQuery(graphNeo4J, UpdateQuery)

def analyzeNetworkX(concepts=None):
    if concepts == None:
        concepts = Concepts.loadConcepts(fileConceptsExport)

    logger.info(" Concepts : %s[%d][%s]" % (concepts.name, len(concepts.getConcepts()), concepts.typeName))

    graph = NetworkXGraph()

    logger.info("Adding NetworkX nodes to the graph ...")
    addGraphNodes(graph, concepts)

    logger.info("Adding NetworkX edges to the graph ...")
    addGraphEdges(graph, concepts)

    gl = nx.pagerank(graph.G)
    analyzeGraph(graph.G, gl, "PageRank", scale=1)

    #
    #  Other NetworkX metrics of Interest
    #
    #gl = nx.connected_components(graph.G) # [[1, 2, 3], ['spam']]
    #analyzeGraph(graph.G, gl, "Connected")

    #gl = nx.clustering(graph.G)
    #analyzeGraph(graph.G, gl, "Cluster")

    #gl = nx.closeness_centrality(graph.G)
    #analyzeGraph(graph.G, gl, "Closeness")

    #gl = nx.betweenness_centrality(graph.G)
    #analyzeGraph(graph.G, gl, "Betweenness_Centrality")

    #gl = nx.hits(graph.G)
    #analyzeGraph(graph.G, gl, "Hits")
   
if __name__ == "__main__":
    analyzeNetworkX()

    



