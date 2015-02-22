#!/usr/bin/python
#
# Natural Language Processing of Archimate Information
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.AnalyzeGraph import AnalyzeGraph
from al_ArchiLib.Neo4JLib import Neo4JLib

from al_Constants import *

def analyzeGraph(gdb):
    start_time = ArchiLib.startTimer()

    ag = AnalyzeGraph(gdb)

    ag.analyzeNetworkX(fileConceptsExport)

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":
    analyzeGraph(gdbTest)

    



