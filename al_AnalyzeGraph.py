#!/usr/bin/python
#
# Natural Language Processing of Archimate Information
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib
from al_lib.AnalyzeGraph import AnalyzeGraph


def analyzeGraph(gdb):
    concepts = None

    start_time = ArchiLib.startTimer()

    ag = AnalyzeGraph(gdb)

    ag.analyzeNetworkX(concepts, fileConceptsExport)

    ArchiLib.stopTimer(start_time)


if __name__ == u"__main__":

    gdb = u"http://localhost:7474/db/data/"

    analyzeGraph(gdb)

    



