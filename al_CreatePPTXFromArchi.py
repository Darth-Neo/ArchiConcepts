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

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from al_ArchiLib.CreatePPTX import *

if __name__ == "__main__":
    cpfa = CreatePPTX()

    cpfa.build()







