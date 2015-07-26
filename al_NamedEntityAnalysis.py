#!/usr/bin/python
#
# Named Entity Analysis
#
__author__  = u'morrj140'
__VERSION__ = u'0.3'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib
from al_lib.AnalyzeNamedEntities import AnalyzeNamedEntities


def namedEntityAnalysis(fileArchimate=fileArchimateTest, fileConceptsRequirements=fileConceptsRequirements):

    start_time = ArchiLib.startTimer()

    ane = AnalyzeNamedEntities(fileArchimate, fileConceptsRequirements)

    ane.analyzeNamedEntities()

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":

    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v2.20.archimate"

    namedEntityAnalysis(fileArchimate=fileArchimate, fileConceptsRequirements=fileConceptsRequirements)