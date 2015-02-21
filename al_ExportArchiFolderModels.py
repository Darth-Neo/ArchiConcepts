#!/usr/bin/python
#
# Archimate Export All Models in a Folder
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import time

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.ExportFolderModels import ExportArchiFolderModels

from al_Constants import *

if __name__ == "__main__":
    start_time = ArchiLib.startTimer()

    eafm = ExportArchiFolderModels()

    eafm.exportArchiFolderModels()

    ArchiLib.stopTimer(start_time)



