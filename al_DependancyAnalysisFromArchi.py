#!/usr/bin/python
#
# Archimate to Dependancy Analysis
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import time

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.DependencyAnalysis import *

from al_Constants import *

if __name__ == "__main__":
    start_time = ArchiLib.startTimer()

    da = DependancyAnalysis(fileArchimate)

    concepts = da.dependancyAnalysis()

    concepts.logConcepts()

    ArchiLib.stopTimer(start_time)