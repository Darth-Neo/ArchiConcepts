#!/usr/bin/python
#
# Natural Language Processing of Archimate Information
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, GraphVizGraph

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.ConceptsGraph import ConceptsGraph


def graphConcepts(conceptFile, fileImageExport):

    start_time = ArchiLib.startTimer()

    c = Concepts(u"GraphConcepts", u"GRAPH")
    concepts = Concepts.loadConcepts(conceptFile)

    # c.logConcepts()

    # graph = PatternGraph()
    graph = GraphVizGraph()

    cg = ConceptsGraph(graph=graph, fileImage=fileImageExport)

    cg.conceptsGraph(concepts)

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":
    # conceptFile = u"documents.p"
    # conceptFile = u"words.p"
    # conceptFile = u"NVPChunks.p"
    # conceptFile = u"chunks.p"
    # conceptFile = u"topicsDict.p"
    # conceptFile = u"TopicChunks.p"
    # conceptFile = u"ngrams.p"
    # conceptFile = u"ngramscore.p"
    conceptFile = u"ngramsubject.p"
    # conceptFile = u"archi.p"
    # conceptFile = u"batches.p"

    graphConcepts(conceptFile, fileImageExport)





