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

gdb = "http://localhost:7474/db/data/"
#gdb = "http://10.92.82.60:7574/db/data/"

THRESHOLD = 4

def addGraphNodes(graph, concepts, n=0):
    n += 1
    for c in concepts.getConcepts().values():
        logger.debug("%d : %d Node c : %s:%s" % (n, len(c.getConcepts()), c.name, c.typeName))
        if c.typeName == "CommonTopic":
            continue
        graph.addConcept(c)
        if len(c.getConcepts()) > THRESHOLD:
            addGraphNodes(graph, c, n)

def addGraphEdges(graph, concepts, n=0):
    n += 1
    i = 1
    for c in concepts.getConcepts().values():
        if c.typeName == "CommonTopic":
            continue
        logger.debug("%d : %d Edge c : %s:%s" % (n, len(c.getConcepts()), c.name, c.typeName))
        if i == 1:
            p = concepts
            i += 1
        else:
            graph.addEdge(p, c)
        if len(c.getConcepts()) != 0:
            addGraphEdges(graph, c, n)

def graphConcepts(concepts, filename="example.png"):

    #graph = Neo4JGraph(gdb)

    #logger.info("Clear the Graph @" + gdb)
    #graph.clearGraphDB()

    graph = GraphVizGraph()
    graph.g.node_attr['shape']='circle'
    graph.g.edge_attr['color']='green'
    graph.g.graph_attr['label']=filename

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
        graph.drawGraph("concepts.png")
        filename = "concepts.net"
        logger.info("Saving Graph - %s" % filename)
        graph.saveGraphPajek("concepts.png")
        graph.saveGraph("concepts.gml")
        logger.info("Saving Graph - %s" % "concepts.gml")
        
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
    #conceptFile = "archi.p"
    #conceptFile = "pptx.p"
    conceptFile = "documentsSimilarity.p"

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

    filename = "Requirements_" + time.strftime("%Y%d%m_%H%M%S") + ".png"
    
    graphConcepts(c, filename=filename)

    



