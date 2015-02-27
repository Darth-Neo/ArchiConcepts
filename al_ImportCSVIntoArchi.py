#!/usr/bin/python
#
# Archimate to Concepts
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.ArchiLib import ArchiLib

from al_Constants import *

import pytest

# Properties
# <element xsi:type="archimate:BusinessProcess" id="0ad0bac9" name="06.0 Activity Reports">
#        <property key="ExampleName" value="ExampleValue"/>
# </element>
#
# child2 = etree.SubElement(root, "child2")
#

def ImportCSVIntoArchi(fileArchimate, folder):

    start_time = ArchiLib.startTimer()

    logger.info("Using : %s" % fileArchimate)
    al = ArchiLib(fileArchimate)

    al.logTypeCounts()

    al.insertNColumns("Application", "Import", folder)

    al.outputXMLtoFile()

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/FOS V4.archimate"

    fileMetaEntity = "import.csv"

    logger.info("dir : %s" % os.getcwd())
    ImportCSVIntoArchi(fileArchimate, fileMetaEntity)