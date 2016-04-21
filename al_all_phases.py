#!/usr/bin/python
#
# Export Archimate into Neo4J
#
__author__ = u'morrj140'
__VERSION__ = u'0.2'

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(logging.INFO)

from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib
from al_lib.ExportArchi import ExportArchi
from al_lib.ConceptsImportNeo4J import ConceptsImportNeo4J
from al_lib.AnalyzeGraph import AnalyzeGraph


if __name__ == u"__main__":

    start_time = ArchiLib.startTimer()

    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CMS into ECM V5.archimate"

    al = ArchiLib(fileArchimate)
    ea = ExportArchi(fileArchimate, fileConceptsExport)

    logger.info(u"...Export Archi...")
    concepts = ea.exportArchi()

    logger.info(u"...Import Neo4J...")
    in4j = ConceptsImportNeo4J(fileArchimate, gdb, ClearNeo4J=True)
    in4j.importNeo4J(concepts)

    logger.info(u"...Analyze NetworkX...")
    ag = AnalyzeGraph(gdb)
    ag.analyzeNetworkX(concepts, fileConceptsExport)

    ArchiLib.stopTimer(start_time)