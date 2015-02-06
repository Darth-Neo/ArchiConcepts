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

from al_ArchiLib.CreateRelations import *

if __name__ == "__main__":

    cr = CreateRelations()
    cr.build()
