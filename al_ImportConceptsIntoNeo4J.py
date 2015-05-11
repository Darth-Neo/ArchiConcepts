#!/usr/bin/python
#
# Natural Language Processing of Concepts to Neo4J Information
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib
from al_lib.ConceptsImportNeo4J import ConceptsImportNeo4J


def importConceptsIntoNeo4J(fileArchimate, gdb, ClearNeo4J=True):

    icnj = ConceptsImportNeo4J(fileArchimate, gdb, ClearNeo4J=ClearNeo4J)

    importConcepts = Concepts.loadConcepts(fileConceptsExport)

    icnj.importNeo4J(importConcepts)

if __name__ == u"__main__":
    start_time = ArchiLib.startTimer()

    importConceptsIntoNeo4J(fileArchimateTest, gdbTest, ClearNeo4J=True)

    ArchiLib.stopTimer(start_time)


    



