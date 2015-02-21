__author__ = 'morrj140'
#!/usr/bin/python
#
# Export Archimate to Concepts
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import time
import hashlib
import logging

from nl_lib import Logger
logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.ExportArchi import ExportArchi

from al_Constants import *

if __name__ == "__main__":
    start_time = ArchiLib.startTimer()

    ea = ExportArchi(fileArchimate, fileConceptsExport)

    ea.exportArchi()

    ArchiLib.stopTimer(start_time)
