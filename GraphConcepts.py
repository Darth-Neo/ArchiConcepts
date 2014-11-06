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
    i = 1
    for c in concepts.getConcepts().values():

        logger.info("%d : %d %s c : %s:%s" % (n, len(c.getConcepts()), concepts.name, c.name, c.typeName))

        if i == 1:
            p = concepts
            graph.addConcept(p)
            graph.addConcept(c)
            graph.addEdge(concepts, c)
            i += 1
        else:
            try:
                graph.addEdge(concepts, c)
            except:
                pass

        if len(c.getConcepts()) != 0:
            addGraphEdges(graph, c, n)

def graphConcepts(concepts, filename="example.png"):

    gdb = "http://localhost:7474/db/data/"
    #gdb = "http://10.92.82.60:7574/db/data/"

    graph = Neo4JGraph(gdb)
    logger.info("Clear the Graph @" + gdb)
    graph.clearGraphDB()

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

        graph.saveGraphPajek("concepts.png")
        graph.saveGraph("concepts.gml")
        
    if isinstance(graph, PatternGraph):
        logger.info("Exporting Graph")
        graph.exportGraph()
   
if __name__ == "__main__":
    #conceptFile = "documents.p"
    #conceptFile = "NVPChunks.p"
    #conceptFile = "chunks.p"
    #conceptFile = "req.p"
    #conceptFile = "topicsDict.p"
    #conceptFile = "TopicChunks.p"
    #conceptFile = "ngrams.p"
    #conceptFile = "ngramscore.p"
    #conceptFile = "ngramsubject.p"
    conceptFile = "archi.p"
    #conceptFile = "pptx.p"
    #conceptFile = "documentsSimilarity.p"
    #conceptFile = "batches.p"

    listHomeDir = list()
    listHomeDir.append(os.getcwd())
    #listHomeDir.append("C:\Users\morrj140\Dev\GitRepository\DirCrawler\SmartMedia_20140206_120122")
    #listHomeDir.append("C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\Estimates_20141205_124422")
    #homeDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\Requirements_20143004_160216"
    #homeDir = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\ExternalInterfaces_20141205_095115"
    #listHomeDir.append("C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\Services_20143004_101231")
    #listHomeDir.append("/Users/morrj140/Development/GitRepository/DirCrawler")
    #listHomeDir.append("/Users/morrj140/Development/GitRepository/DirCrawler/Research_20141709_104529")

    c = Concepts("GraphConcepts", "GRAPH")
    
    for conceptDir in listHomeDir:
        # Change current directory to enable to save pickles
        p, f = os.path.split(conceptDir)
        logger.info("Loading :" + conceptDir + os.sep + conceptFile)
        c.addConcept(Concepts.loadConcepts(conceptDir + os.sep + conceptFile))

    # c.logConcepts()

    filename = "Batches_" + time.strftime("%Y%d%m_%H%M%S") + ".png"
    
    graphConcepts(c, filename=filename)

    



