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
import networkx as nx

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

        #gl = nx.connected_components(graph.G) # [[1, 2, 3], ['spam']]
        #logGraph(gl, "Connected")

        #gl = nx.clustering(graph.G)
        #logGraph(gl, "Cluster")

        #gl = nx.closeness_centrality(graph.G)
        #logGraph(gl, "Closeness")

        #gl = nx.betweenness_centrality(graph.G)
        #logGraph(gl, "Betweenness_Centrality")

        gl = nx.pagerank(graph.G)
        sgl = sorted(gl.iteritems(), key=lambda (c, v): v, reverse=False)

        logGraph(gl, "Page Rank")

        #gl = nx.hits(graph.G)
        #logGraph(gl, "Hits")

        #gl = nx.authority_matrix(graph.G)
        #logGraph(gl, "authority_matrix")

        #gl = nx.minimum_spanning_tree(graph.G)
        #logGraph(gl, "minimum_spanning_tree")

        #gl = nx.degree(graph.G)
        #sgl = sorted(graph.G.nodes(), key=lambda c: c[1], reverse=False)
        #logGraph(sgl, "degree")
        
    if isinstance(graph, PatternGraph):
        logger.info("Exporting Graph")
        graph.exportGraph()
   
if __name__ == "__main__":
    conceptFile = "export.p"

    exportConcepts = Concepts.loadConcepts(conceptFile)

    graphConcepts(exportConcepts)

    



