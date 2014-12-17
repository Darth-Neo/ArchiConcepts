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
            if isinstance(graph, Neo4JGraph):
                graph.addEdge(concepts, c, c.typeName)
            else:
                graph.addEdge(concepts, c)
            i += 1
        else:
            try:
                if isinstance(graph, Neo4JGraph):
                    graph.addEdge(concepts, c, c.typeName)
                else:
                    graph.addEdge(concepts, c)
            except:
                pass

        if len(c.getConcepts()) != 0:
            addGraphEdges(graph, c, n)

def graphConcepts(concepts, filename="example.png"):

    gdb = "http://localhost:7474/db/data/"
    #gdb = "http://10.92.82.60:7574/db/data/"

    if True:
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
        graph.saveGraph("concepts.gml")
        
    if isinstance(graph, PatternGraph):
        logger.info("Exporting Graph")
        graph.exportGraph()
   
if __name__ == "__main__":
    cfl = list()
    #cfl.append("documents.p")
    #cfl.append("NVPChunks.p")
    #cfl.append("chunks.p")
    #cfl.append("req.p")
    #cfl.append("topicsDict.p")
    #cfl.append("TopicChunks.p")
    #cfl.append("ngrams.p")
    #cfl.append("ngramscore.p")
    #cfl.append("ngramsubject.p")
    cfl.append("archi.p")
    #cfl.append("pptx.p")
    #cfl.append("documentsSimilarity.p")
    #cfl.append("batches.p")
    #cfl.append("export.p")
    #cfl.append("req.p")
    #cfl.append("report.p")

    #homeDir = os.getcwd()
    homeDir = "/Users/morrj140/Development/GitRepository/ArchiConcepts"
    #homeDir = "/Users/morrj140/Development/GitRepository/DirCrawler"
    #homeDir = "/Users/morrj140/Development/GitRepository/DirCrawler/Research_20141709_104529"

    os.chdir(homeDir)

    c = Concepts("GraphConcepts", "GRAPH")
    
    for cf in cfl:
        # Change current directory to enable to save pickles
        logger.info("Loading :" + homeDir + os.sep + cf)
        c.addConcept(Concepts.loadConcepts(homeDir + os.sep + cf))

    # c.logConcepts()

    filename = "Concepts_" + time.strftime("%Y%d%m_%H%M%S") + ".png"
    
    graphConcepts(c, filename=filename)

    



