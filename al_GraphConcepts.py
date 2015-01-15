#!/usr/bin/python
#
# Natural Language Processing of Archimate Information
#
import os
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

import logging
logger.setLevel(logging.INFO)

from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, GraphVizGraph
from nl_lib.Constants import *

from al_ArchiLib import *

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

def graphConcepts(concepts, graph=None, filename="example.png"):

    #graph = PatternGraph()
    graph = GraphVizGraph()

    logger.info("Adding %s nodes the graph ..." % type(graph))
    addGraphNodes(graph, concepts)
    logger.info("Adding %s edges the graph ..." % type(graph))
    addGraphEdges(graph, concepts)

    if isinstance(graph, GraphVizGraph):
        graph.exportGraph(filename=filename)
        logger.info("Saved Graph - %s" % filename)

    if isinstance(graph, PatternGraph):
        #graph.g.remove("ProjectConceptsSimilarity")
        logger.info("Exporting Graph")
        graph.exportGraph()

def logGraph(gl, title, scale=1):
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

    c = Concepts("GraphConcepts", "GRAPH")
    concepts = Concepts.loadConcepts(conceptFile)

    # c.logConcepts()

    graphConcepts(concepts, filename="DVC.png")






