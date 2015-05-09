#!/usr/bin/python
#
# Natural Language Processing of Archimate Information
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
from subprocess import call
import time

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, NetworkXGraph, GraphVizGraph, Neo4JGraph

import networkx as nx

from Constants import *
from ArchiLib import ArchiLib
from Neo4JLib import Neo4JLib


class AnalyzeGraph(object):

    def __init__(self, gdb):

        self.nj = Neo4JLib(gdb, fileCSVExport=fileCSVExport)
        self.graph = NetworkXGraph()
        self.scale = 1
        self.threshold = 0.0005

    def addGraphNodes(self, concepts, n=0, threshold=0.0005):

        n += 1

        for c in concepts.getConcepts().values():
            logger.debug(u"%d : %d Node c : %s:%s" % (n, len(c.getConcepts()), c.name, c.typeName))

            self.graph.addConcept(c)

            if len(c.getConcepts()) > threshold:
                self.addGraphNodes(c, n)

    def addGraphEdges(self, concepts, n=0):
        n += 1

        self.graph.addConcept(concepts)

        for c in concepts.getConcepts().values():

            logger.debug(u"%d : %d %s c : %s:%s" % (n, len(c.getConcepts()), concepts.name, c.name, c.typeName))

            self.graph.addConcept(c)

            self.graph.addEdge(concepts, c)

            if len(c.getConcepts()) != 0:
                self.addGraphEdges(c, n)

    def updateNeo4J(self, name, typeName, metricName, metricValue):

        if len(metricName.split(u" ")) > 1:
            logger.error(u"metricName cannot contain spaces!")
            return

        UpdateQuery = u"match (n {typeName:\"%s\", name:\"%s\"}) set n.%s = %3.4f return n" % (typeName, name, metricName, metricValue)
        logger.debug(u"UpdateQuery : %s" % UpdateQuery)
        self.nj.cypherQuery(UpdateQuery)

    def analyzeGraph(self, gl, title):

        gNodes = self.graph.G.node

        pr = 0
        len_pr = len(gl)
        sum_pr = 0.0

        logger.info(u"---%s---[%d]" % (title, len(gl)))

        n = 0
        for x in gl:

            nodeValue = gl[x]

            n += 1

            sum_pr = nodeValue

            if nodeValue > pr:
                pr = nodeValue

            nodeKey = gNodes[x]

            if isinstance(nodeKey, dict) and u"typeName" in nodeKey:
                typeName = nodeKey[u'typeName']

                if typeName in relations:
                    logger.debug(u"Skip : %s" % typeName)
                    continue

                self.updateNeo4J(x, typeName, title, nodeValue*self.scale)

                degree = nx.degree(self.graph.G)[x]

                self.updateNeo4J(x, typeName, u"Degree", degree)

                logger.info(u"%s : %s[%s]=%3.4f" % (title, x, typeName, nodeValue*self.scale))

        logger.info(u"Metrics for %s" % title)
        logger.info(u"Len gl[x]=%3.4f" % n)  # len_pr)
        logger.info(u"Max gl[x]=%3.4f" % pr)
        logger.info(u"Avg gl[x]=%3.4f" % (sum_pr / len_pr))

    def analyzeNetworkX(self, concepts, fileConceptsExport=None):

        if concepts is None and fileConceptsExport is not None:
            concepts = Concepts.loadConcepts(fileConceptsExport)

        logger.info(u" Concepts : %s[%d][%s]" % (concepts.name, len(concepts.getConcepts()), concepts.typeName))

        self.graph = NetworkXGraph()

        logger.info(u"Adding NetworkX nodes to the graph ...")
        self.addGraphNodes(concepts)

        logger.info(u"Adding NetworkX edges to the graph ...")
        self.addGraphEdges(concepts)

        gl = nx.pagerank(self.graph.G)
        self.analyzeGraph(gl, u"PageRank")

        #
        #  Other NetworkX metrics of Interest
        #
        # gl = nx.connected_components(graph.G) # [[1, 2, 3], ['spam']]
        # analyzeGraph(graph.G, gl, "Connected")

        # gl = nx.clustering(graph.G)
        # analyzeGraph(graph.G, gl, "Cluster")

        # gl = nx.closeness_centrality(graph.G)
        # analyzeGraph(graph.G, gl, "Closeness")

        # gl = nx.betweenness_centrality(graph.G)
        # analyzeGraph(graph.G, gl, "Betweenness_Centrality")

        # gl = nx.hits(graph.G)
        # analyzeGraph(graph.G, gl, "Hits")

def test_AnalyzeGraph():

    start_time = ArchiLib.startTimer()

    ag = AnalyzeGraph(gdb)

    ag.analyzeNetworkX(fileConceptsExport)

    ArchiLib.stopTimer(start_time)

if __name__ == U"__main__":
    if False:
        test_AnalyzeGraph()
    else:
        fileConceptsExport

        start_time = ArchiLib.startTimer()

        ag = AnalyzeGraph(gdb)

        ag.analyzeNetworkX(fileConceptsExport)

        ArchiLib.stopTimer(start_time)
