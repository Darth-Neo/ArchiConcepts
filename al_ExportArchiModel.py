#!/usr/bin/python
#
# Archimate to export a model
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)

from al_Constants import *
from al_lib.ArchiLib import ArchiLib
from al_lib.ExportModel import ExportArchiModel


def exportArchiModel(fileArchimate, fileConceptsExport, model, fileCSVExport):

    start_time = ArchiLib.startTimer()

    eam = ExportArchiModel(fileArchimate, fileConceptsExport, fileCSVExport)

    listMTE = list()
    listMTE.append(model)

    eam.exportArchiModel(listMTE)

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":

    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v2.15.archimate"

    model = u"To-Be - Revenue Recognition - Application Context"

    exportArchiModel(fileArchimate, fileConceptsExport, model, fileCSVExport)
