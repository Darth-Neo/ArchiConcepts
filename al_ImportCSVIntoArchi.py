#!/usr/bin/python
#
# Archimate to Concepts
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib


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

def ImportCSVIntoArchi(fileArchimate, folder, subfolder, fileMetaEntity):

    start_time = ArchiLib.startTimer()

    logger.info(u"Using : %s" % fileArchimate)
    al = ArchiLib(fileArchimate)

    listCounts = al.logTypeCounts(ListOnly=True)

    # insertNColumns(self, folder, subfolder, fileMetaEntity):
    al.insertNColumns(folder, subfolder, fileMetaEntity)

    al.outputXMLtoFile()

    logger.info(u"Encountered %d errors" % len(al.listError))

    fileArchimate = u"import_artifacts.archimate"
    nal = ArchiLib(fileArchimate)
    newListCounts = nal.logTypeCounts(ListOnly=True)

    for a, b in zip(listCounts, newListCounts):
        if a[1] == b[1]:
            continue
        logger.info(u"%3d-%3d-%3d Added %s" % (b[1], a[1], (b[1] - a[1]), b[0]))

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":
    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/WDW Cast v1.1.archimate"

    fileMetaEntity = u"%s%sCast Experience Prioritized User Stories(1).csv" % (os.getcwd(), os.sep)
    folder = u"Business"
    subfolder = u"WDW Cast User Stories"

    logger.info(u"dir : %s" % os.getcwd())
    ImportCSVIntoArchi(fileArchimate, folder, subfolder, fileMetaEntity)