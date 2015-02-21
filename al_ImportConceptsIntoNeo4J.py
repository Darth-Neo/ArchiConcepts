#!/usr/bin/python
#
# Natural Language Processing of Concepts to Neo4J Information
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.ConceptsImportNeo4J import ConceptsImportNeo4J

from al_Constants import *

import pytest

def importConceptsIntoNeo4J():

    start_time = ArchiLib.startTimer()

    icnj = ConceptsImportNeo4J()

    importConcepts = Concepts.loadConcepts(fileConceptsExport)

    icnj.importNeo4J(importConcepts, ClearNeo4J=True)

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":
    importConceptsIntoNeo4J()


    



