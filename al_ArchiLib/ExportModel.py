#!/usr/bin/python
#
# Archimate to export a model
#
__author__ = u'morrj140'
__VERSION__= u'0.1'

import sys
import os
import StringIO
import time

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from Constants import *
from ArchiLib import ArchiLib


class ExportArchiModel(object):
    fileArchimate = None
    fileConceptsExport = None

    def __init__(self, fileArchimate, fileConceptsExport, fileCSVExport=None):

        self.fileArchimate = fileArchimate
        self.fileConceptsExport = fileConceptsExport
        self.fileCSVExport = fileCSVExport

        self.al = ArchiLib(self.fileArchimate)

    def exportArchiModel(self, listMTE):

        logger.info(u"Using : %s" % self.fileArchimate)
        concepts = Concepts(u"Export", u"Model")

        for ModelToExport in listMTE:
            self.al.recurseModel(ModelToExport, concepts)

        Concepts.saveConcepts(concepts, self.fileConceptsExport)

        if self.fileCSVExport <> None:
            self.al.outputCSVtoFile(concepts, self.fileCSVExport)


def text_ExportModel():

    start_time = ArchiLib.startTimer()

    eam = ExportArchiModel(fileArchimateTest, fileConceptsExport)

    listMTE = list()

    listMTE.append(u"To-Be DAM Functional Reference Architecture")

    eam.exportArchiModel(listMTE)

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":
    text_ExportModel()