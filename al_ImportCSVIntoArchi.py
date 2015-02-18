#!/usr/bin/python
#
# Archimate to Concepts
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import csv
import random

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib


# Properties
# <element xsi:type="archimate:BusinessProcess" id="0ad0bac9" name="06.0 Activity Reports">
#        <property key="ExampleName" value="ExampleValue"/>
# </element>
#
# child2 = etree.SubElement(root, "child2")
#


if __name__ == "__main__":
    start_time = ArchiLib.startTimer()

    logger.info("Using : %s" % fileArchimate)

    al = ArchiLib(fa="/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v26.archimate")

    al.logTypeCounts()

    fileMetaEntity = "DVCEvolution.csv"

    al.insertNColumns("Application", "Evolution", fileMetaEntity)

    al.outputXMLtoFile()

    ArchiLib.stopTimer(start_time)