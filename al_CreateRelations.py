#!/usr/bin/python
#
# Archimate Relations
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.CreateRelationsInArchi import CreateRelationsInArchi

from al_Constants import *

import pytest

def createRelations(fileArchimate):

    start_time = ArchiLib.startTimer()

    cr = CreateRelationsInArchi(fileArchimate)

    cr.createRelations()

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":

    # fileArchimate is defined in al_Constants
    createRelations(fileArchimateTest)
