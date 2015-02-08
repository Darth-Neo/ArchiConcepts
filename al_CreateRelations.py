#!/usr/bin/python
#
# Archimate Relations
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import csv
import time
import random

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from al_ArchiLib.Constants import *
from al_ArchiLib.al_ArchiLib import ArchiLib
from al_ArchiLib.CreateRelationsInArchi import CreateRelationsInArchi


if __name__ == "__main__":

    start_time = ArchiLib.startTimer()

    cr = CreateRelationsInArchi()

    cr.createRelations()

    ArchiLib.stopTimer(start_time)
