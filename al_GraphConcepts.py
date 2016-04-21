#!/usr/bin/python
#
# Natural Language Processing of Archimate Information
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

import os
from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, GraphVizGraph, NetworkXGraph

from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib

def graphConcepts(conceptFile):

    start_time = ArchiLib.startTimer()

    concepts = Concepts.loadConcepts(conceptFile)
    # concepts.logConcepts()

    # graph = PatternGraph()
    graph = GraphVizGraph()
    # graph = NetworkXGraph(conceptFile[:-2]+u".png")

    graph.addGraphNodes(concepts)
    graph.addGraphEdges(concepts)

    if isinstance(graph, NetworkXGraph):
        graph.saveJSON(concepts)

    if isinstance(graph, GraphVizGraph):
        graph.exportGraph()

    if isinstance(graph, PatternGraph):
        graph.exportGraph()

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":

    logger.info(u"%s" % os.getcwd())
    # os.chdir(u"." + os.sep + u"run")

    conceptFile = os.getcwd() + os.sep + u"archi.p"

    graphConcepts(conceptFile)






