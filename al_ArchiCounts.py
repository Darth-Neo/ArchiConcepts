#!/usr/bin/python
#
# Archimate Counts
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

import os
import time

from nl_lib import Logger
logger = Logger.setupLogging(__name__)


from al_ArchiLib.ArchiLib import ArchiLib
from al_Constants import *

import pytest

if __name__ == "__main__":

    al = ArchiLib(fileArchimateTest)

    al.logTypeCounts()