#!/usr/bin/python
#
# Natural Language Processing of Archimate Information
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, GraphVizGraph
from nl_lib.Constants import *

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.ConceptsGraph import ConceptsGraph

from al_Constants import *

import pytest

def graphConcepts(conceptFile, fileImageExport):

    start_time = ArchiLib.startTimer()

    c = Concepts("GraphConcepts", "GRAPH")
    concepts = Concepts.loadConcepts(conceptFile)

    # c.logConcepts()

    #graph = PatternGraph()
    graph = GraphVizGraph()

    cg = ConceptsGraph(graph=graph, fileImage=fileImageExport)

    cg.conceptsGraph(concepts)

    ArchiLib.stopTimer(start_time)

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

    graphConcepts(conceptFile, fileImageExport)





