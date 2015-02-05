#!/usr/bin/python
#
# Archimate Counts
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
from nl_lib.Constants import *
from nl_lib import Logger
from nl_lib.Concepts import Concepts
import time

logger = Logger.setupLogging(__name__)

import al_ArchiLib as AL

if __name__ == "__main__":
    al = AL.ArchiLib()

    al.logTypeCounts()