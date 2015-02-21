#!/usr/bin/python
#
# Named Entity Analysis
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.AnalyzeNamedEntities import AnalyzeNamedEntities

from al_Constants import *

import pytest

def namedEntityAnalysis():

    start_time = ArchiLib.startTimer()

    ane = AnalyzeNamedEntities(fileArchimateTest, fileConceptsRequirements)

    ane.analyzeNamedEntities()

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":
    namedEntityAnalysis()