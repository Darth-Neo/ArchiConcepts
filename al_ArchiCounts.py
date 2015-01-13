#!/usr/bin/python
#
# Archimate Counts
#
__author__ = 'morrj140'

import os
from nl_lib.Constants import *
from nl_lib import Logger
from nl_lib.Concepts import Concepts
import time

logger = Logger.setupLogging(__name__)

from al_ArchiLib import *

if __name__ == "__main__":
    al = ArchiLib()

    al.logTypeCounts()