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

# Note : all columns should have a header with an Archimate Object
# Can also use Property.<whatever>

import pytest

# Properties
# <element xsi:type="archimate:BusinessProcess" id="0ad0bac9" name="06.0 Activity Reports">
#        <property key="ExampleName" value="ExampleValue"/>
# </element>
#
# child2 = etree.SubElement(root, "child2")
#

def ImportCSVIntoArchi(fileArchimate, folder, fileMetaEntity):

    start_time = ArchiLib.startTimer()

    logger.info("Using : %s" % fileArchimate)
    al = ArchiLib(fileArchimate)

    al.logTypeCounts()

    # insertNColumns(self, folder, subfolder, fileMetaEntity):
    al.insertNColumns("Application", folder, fileMetaEntity)

    al.outputXMLtoFile()

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v36.archimate"

    fileMetaEntity = "export_sections.csv"
    folder = "AT+LN Data Analysis"

    logger.info("dir : %s" % os.getcwd())
    ImportCSVIntoArchi(fileArchimate, folder, fileMetaEntity)