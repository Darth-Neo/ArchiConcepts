#!/usr/bin/python
#
# Archimate to Dependancy Analysis
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.DependencyAnalysis import *

def dependancyAnalysisFromArchi(fileArchimate):

    start_time = ArchiLib.startTimer()

    da = DependancyAnalysis(fileArchimate)

    concepts = da.dependancyAnalysis()

    concepts.logConcepts()

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":

    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CMS into ECM V5.archimate"

    dependancyAnalysisFromArchi(fileArchimate)