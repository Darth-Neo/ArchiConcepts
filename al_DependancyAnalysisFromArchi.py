#!/usr/bin/python
#
# Archimate to Dependancy Analysis
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.DependencyAnalysis import *

from al_Constants import *

def dependancyAnalysisFromArchi(fileArchimate):

    start_time = ArchiLib.startTimer()

    da = DependancyAnalysis(fileArchimate)

    concepts = da.dependancyAnalysis()

    concepts.logConcepts()

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":
    dependancyAnalysisFromArchi(fileArchimateTest)