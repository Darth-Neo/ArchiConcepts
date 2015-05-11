#!/usr/bin/python
#
# Archimate Export All Models in a Folder
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib
from al_lib.ExportFolderModels import ExportArchiFolderModels


def exportArchiFolderModels(fileArchimate, fileConceptsExport, folder):

    start_time = ArchiLib.startTimer()

    eafm = ExportArchiFolderModels(fileArchimate, fileConceptsExport)

    eafm.exportArchiFolderModels(folder)

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":
    folder = u"AS400 Analysis"

    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v32.archimate"

    exportArchiFolderModels(fileArchimate, fileConceptsExport, folder)


