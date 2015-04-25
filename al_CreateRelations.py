#!/usr/bin/python
#
# Archimate Relations
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.CreateRelationsInArchi import CreateRelationsInArchi

from al_Constants import *

import pytest

def createRelations(fileArchimate=fileArchimateTest):

    start_time = ArchiLib.startTimer()

    cr = CreateRelationsInArchi(fileArchimate)

    cr.createRelations()

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":

    # fileArchimate is also defined in al_Constants
    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v38.archimate"

    createRelations(fileArchimate)
