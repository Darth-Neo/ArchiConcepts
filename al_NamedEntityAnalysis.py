#!/usr/bin/python
#
# Named Entity Analysis
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import logging
import time

from nl_lib import Logger
logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.AnalyzeNamedEntities import AnalyzeNamedEntities

from al_Constants import *

if __name__ == "__main__":

    start_time = ArchiLib.startTimer()

    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v27.archimate"
    fileRelationsConcepts = "reqs.p"

    ane = AnalyzeNamedEntities(fileArchimate, fileRelationsConcepts)

    ane.analyzeNamedEntities()

    ArchiLib.stopTimer(start_time)