#!/usr/bin/python
#
# Named Entity Analysis
#
__author__  = u'morrj140'
__VERSION__ = u'0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.AnalyzeNamedEntities import AnalyzeNamedEntities

from al_Constants import *

import pytest

def namedEntityAnalysis(fileArchimate=fileArchimateTest, fileConceptsRequirements=fileConceptsRequirements):

    start_time = ArchiLib.startTimer()

    ane = AnalyzeNamedEntities(fileArchimate, fileConceptsRequirements)

    ane.analyzeNamedEntities()

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":
    namedEntityAnalysis(fileArchimate=fileArchimate, fileConceptsRequirements=fileConceptsRequirements)