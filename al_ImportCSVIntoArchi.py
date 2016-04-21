#!/usr/bin/python
#
# Archimate to Concepts
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from Logger import *
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

    _ = al.logTypeCounts(ListOnly=True)

    al.insertNColumns(folder, subfolder, fileMetaEntity, CaseFix=False)

    al.outputXMLtoFile()

    relations = len(al.dictRel)
    nodes = len(al.dictND)

    logger.info(u"----------------------------------------------------------------------------------------")
    logger.info(u"Encountered %d errors and added %d Nodes and %d relations" % (len(al.listErrors), nodes, relations))

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":

    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DALE_V8.archimate"
    fileMetaEntity = u"%s%sTRANREC.csv" % (os.getcwd(), os.sep)
    folder = u"Application"
    # folder = u"Implementation & Migration"
    subfolder = u"RTP_2016_04_20_1200"

    logger.info(u"dir : %s" % os.getcwd())
    ImportCSVIntoArchi(fileArchimate, folder, subfolder, fileMetaEntity)
