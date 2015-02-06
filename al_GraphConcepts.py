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

from al_ArchiLib.Constants import *
from al_ArchiLib.ConceptsGraph import ConceptsGraph

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






