#!/usr/bin/python
#
# Archimate Deduping
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib

if __name__ == "__main__":
    fileArchiP = "archi.p"
    fileArchiModel = 'archi.archimate'

    al = ArchiLib(fileArchimate)

    al.logTypeCounts()

    p, fname = os.path.split(fileArchimate)
    logger.info("Using : %s" % fileArchimate)

    concepts = Concepts(fname, "Archimate")

    al.folderConcepts(concepts)

    #concepts.logConcepts()

    #Concepts.saveConcepts(concepts, "dedup.p")

    #
    # Generate Archimate from Concepts
    #
    output = al.createArchimate(fileArchiModel, fileArchiP)

