#!/usr/bin/python
#
# Archimate Export All Models in a Folder
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_ArchiLib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.ExportFolderModels import ExportArchiFolderModels

from al_Constants import *

import pytest

def exportArchiFolderModels(fileArchimate, fileConceptsExport, folder):

    start_time = ArchiLib.startTimer()

    eafm = ExportArchiFolderModels(fileArchimate, fileConceptsExport)

    eafm.exportArchiFolderModels(folder)

    ArchiLib.stopTimer(start_time)

if __name__ == "__main__":
    folder = "3. Application"

    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CastMemberCoupons.archimate"


    exportArchiFolderModels(fileArchimate, fileConceptsExport, folder)


