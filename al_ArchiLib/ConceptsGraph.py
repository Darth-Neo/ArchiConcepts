#!/usr/bin/python
#
# Natural Language Processing of Archimate Information
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

import logging
logger.setLevel(logging.INFO)

from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, GraphVizGraph
from nl_lib.Constants import *

class ConceptsGraph(object):

    def __init__(self, graph=None, fileImage=None):
        self.threshold=0.0005

        if graph == None:
            self.graph = PatternGraph()
            #self.graph = GraphVizGraph()
        else:
            self.graph = graph

        if fileImage == None:
            self.fileImage = "example.png"
        else:
            self.fileImage = fileImage

        #
        # Hack to get GraphViz to work
        #
        os.environ['PATH'] = "%s:/opt/local/bin" % os.environ['PATH']

    def addGraphNodes(self, concepts, n=0):

        n += 1

        for c in concepts.getConcepts().values():
            logger.debug("%d : %d Node c : %s:%s" % (n, len(c.getConcepts()), c.name, c.typeName))

            self.graph.addConcept(c)

            if len(c.getConcepts()) > self.threshold:
                self.addGraphNodes(c, n)

    def addGraphEdges(self, concepts, n=0):
        n += 1

        self.graph.addConcept(concepts)

        for c in concepts.getConcepts().values():

            logger.debug("%d : %d %s c : %s:%s" % (n, len(c.getConcepts()), concepts.name, c.name, c.typeName))

            self.graph.addConcept(c)

            self.graph.addEdge(concepts, c)

            if len(c.getConcepts()) != 0:
                self.addGraphEdges(c, n)

    def conceptsGraph(self, concepts):

        logger.info("Adding %s nodes the graph ..." % type(self.graph))
        self.addGraphNodes(concepts)

        logger.info("Adding %s edges the graph ..." % type(self.graph))
        self.addGraphEdges(concepts)

        if isinstance(self.graph, GraphVizGraph):
            self.graph.exportGraph(filename=self.fileImage)
            logger.info("Saved Graph - %s" % self.fileImage)

        if isinstance(self.graph, PatternGraph):
            #graph.g.remove("ProjectConceptsSimilarity")
            logger.info("Exporting Graph")
            self.graph.exportGraph()

    def logGraph(self, gl, title, scale=1):
        logger.info("---%s---" % title)
        n = 0
        for x in gl:
            n += 1
            if isinstance(gl, dict):
                logger.info("%s [%d]:%s=%3.4f" % (title, n, x, gl[x]*scale))

            else:
                logger.info("%s [%d]" % (x, n))


if __name__ == "__main__":
    #conceptFile = "documents.p"
    #conceptFile = "words.p"
    #conceptFile = "NVPChunks.p"
    #conceptFile = "chunks.p"
    #conceptFile = "topicsDict.p"
    #conceptFile = "TopicChunks.p"
    #conceptFile = "ngrams.p"
    #conceptFile = "ngramscore.p"
    conceptFile = "ngramsubject.p"
    #conceptFile = "archi.p"
    #conceptFile = "batches.p"

    c = Concepts("GraphConcepts", "GRAPH")
    concepts = Concepts.loadConcepts(conceptFile)

    # c.logConcepts()

    cg = ConceptsGraph(fileImage="DVCBatches.png")

    cg.conceptsGraph(concepts)







