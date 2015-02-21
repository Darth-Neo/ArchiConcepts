#!/usr/bin/python
#
# Create PPTX from Archimate XML
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.ArchiCreatePPTX import ArchiCreatePPTX

from al_Constants import *

import pytest

def createPPTXFromArchi():
    cpfa = ArchiCreatePPTX(fileArchimateTest, filePPTXIn, filePPTXOut)

    cpfa.buildPPTX()

if __name__ == "__main__":
    createPPTXFromArchi()






