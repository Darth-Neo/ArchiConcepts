#!/usr/bin/python
#
# Create PPTX from Archimate XML
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from al_ArchiLib.ArchiCreatePPTX import ArchiCreatePPTX

from al_Constants import *

if __name__ == "__main__":

    cpfa = ArchiCreatePPTX()

    cpfa.build()







