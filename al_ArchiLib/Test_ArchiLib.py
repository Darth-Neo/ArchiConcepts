#!/usr/bin/python
#
# al_ArchiLib Testing
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import time
import json

from Constants import *
from Logger import *

logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

from ArchiLib import ArchiLib

import pytest

dirTest = "test" + os.sep

fileArchimate      = dirTest + "Testing.archimate"

conceptsExport     = dirTest  + "export.p"
conceptsEstimation = dirTest  + "estimation.p"
conceptsArchi      = dirTest  + "archi.p"

exportCSV          = dirTest  + "export.csv"
exportReportCSV    = dirTest  + "report.csv"


@pytest.fixture(scope="module")
def cleandir():
    cwd = os.getcwd()

    listFiles = list()
    listFiles.append("Estimation.p")
    listFiles.append("export.p")
    listFiles.append("report.csv")
    listFiles.append("export.csv")

    for lf in listFiles:
        ftr = cwd + os.sep + "test" + os.sep + lf

        if os.path.exists(ftr):
            logger.info("remove : %s" % ftr)
            os.remove(ftr)

@pytest.mark.Archi
def test_Archi_Counts(cleandir):

    if __name__ == "__main__":
        cleandir()

    assert (os.path.isfile(fileArchimate)  == True)
    logger.info("Exists : %s" % fileArchimate)

    #archimate:TriggeringRelationship : 4 != 24
    #archimate:UsedByRelationship : 12 != 72
    #archimate:ApplicationService : 6 != 36
    #archimate:AccessRelationship : 13 != 78
    #archimate:FlowRelationship : 5 != 30
    #archimate:DataObject : 5 != 30
    #archimate:BusinessObject : 5 != 30
    #archimate:BusinessProcess : 7 != 42
    #archimate:BusinessEvent : 2 != 12
    #archimate:ApplicationComponent : 3 != 18

    testDict = {"archimate:TriggeringRelationship" : 4 , "archimate:UsedByRelationship" : 12,
                "archimate:ApplicationService" : 6, "archimate:AccessRelationship" : 13,
                "archimate:FlowRelationship" : 5, "archimate:DataObject" : 5 ,
                "archimate:BusinessObject" : 5, "archimate:BusinessProcess" : 7,
                "archimate:BusinessEvent" : 2, "archimate:ApplicationComponent" : 3}

    al = ArchiLib(fileArchimate)

    listCounts = al.logTypeCounts()

    logger.info("listCounts : %d" % len(listCounts))

    assert (len(listCounts)  == 10)

    TestStatus = True

    for x in listCounts:
        if testDict[x[0]] == x[1] :
            logger.info("%s, %s == %s" % (x[0], x[1], testDict[x[0]]))
        else:
            logger.error("%s : %s != %s" % (x[0], x[1], testDict[x[0]]))
            TestStatus = False

    assert (TestStatus == True)

@pytest.mark.Archi
def test_CheckForArchimateFile(cleandir):

    if __name__ == "__main__":
        cleandir()

    assert (os.path.isfile(fileArchimate)  == True)

@pytest.mark.Archi
def test_ExportArchi(cleandir):

    if __name__ == "__main__":
        cleandir()

    logger.info("Using : %s" % fileArchimate)

    assert (os.path.isfile(fileArchimate)  == True)

    al = None
    concepts = None

    al = ArchiLib(fileArchimate)

    assert (al != None)

    concepts = Concepts("Node", "Nodes")

    assert (concepts  != None)

    logger.info("Found %d Nodes" % len(al.dictNodes))
    logger.info("Found %d Edges" % len(al.dictEdges))

    assert (len(al.dictNodes) == 40)
    assert (len(al.dictEdges) == 35)

    count = 0
    listTSort = list()
    for x in al.dictEdges.keys():
        logger.info("[%s]=%s" % (al.dictEdges[x]["id"], x))

        if al.dictEdges[x].has_key("source"):
            source = al.dictEdges[x]["source"]
            target = al.dictEdges[x]["target"]

            logger.info("  Rel    : %s" % (al.dictEdges[x][ARCHI_TYPE]))

            sourceName = al.getNodeName(source)
            targetName = al.getNodeName(target)

            logger.info(" %s--%s--%s" % (sourceName, al.dictEdges[x][ARCHI_TYPE][10:], targetName))

            sc = concepts.addConceptKeyType(sourceName, al.dictNodes[source][ARCHI_TYPE][10:])
            #getWords(sourceName, sc)

            tc = sc.addConceptKeyType(targetName, al.dictNodes[target][ARCHI_TYPE][10:])
            #getWords(sourceName, tc)

    Concepts.saveConcepts(concepts, conceptsExport)

    assert(len(concepts.cd) == 17)

    assert (os.path.isfile(conceptsExport)  == True)

    assert(concepts.typeName == "Nodes")

@pytest.mark.Archi
def test_ExportArchiFolderModels(cleandir):

    if __name__ == "__main__":
        cleandir()

    assert (os.path.isfile(fileArchimate)  == True)
    al = ArchiLib(fileArchimate)

    folder = "Scenarios"

    logger.info("Exporting Folder : %s" % folder)
    listMTE = al.getModelsInFolder(folder)
    assert (listMTE != None)

    logger.info("len(listMTE) = %d" % len(listMTE))
    assert (len(listMTE) == 2)

    concepts = Concepts("Export", "Pickle")

    for ModelToExport in listMTE:
        logger.info("  Model : %s" % ModelToExport)
        d = concepts.addConceptKeyType(ModelToExport, "Model")
        al.recurseModel(ModelToExport, d)

    al.outputCSVtoFile(concepts, fileExport=exportCSV)
    assert (os.path.isfile(exportCSV)  == True)

    Concepts.saveConcepts(concepts, conceptsExport)
    logger.info("Save Concepts : %s" % conceptsExport)

    assert (os.path.isfile(conceptsExport)  == True)

@pytest.mark.Archi
def test_ArchimateConcepts(cleandir):

    if __name__ == "__main__":
        cleandir()

    logger.info("Using : %s" % fileArchimate)

    assert (os.path.isfile(fileArchimate)  == True)

    concepts = Concepts(conceptsArchi, "Archimate")

    al = ArchiLib(fileArchimate)

    #
    # Create Concepts from Archimate
    #
    al.folderConcepts(concepts)

    Concepts.saveConcepts(concepts, conceptsArchi)
    logger.info("Saved concepts to : %s" % conceptsArchi)

    assert (os.path.isfile(conceptsArchi)  == True)

@pytest.mark.Archi
def test_ExportArchiModel(cleandir):

    if __name__ == "__main__":
        cleandir()

    assert (os.path.isfile(fileArchimate)  == True)

    al = ArchiLib(fileArchimate)

    listMTE = list()
    listMTE.append("01. Market to Leads")

    concepts = Concepts("Export", "Model")

    for ModelToExport in listMTE:
        al.recurseModel(ModelToExport, concepts)

    Concepts.saveConcepts(concepts, conceptsExport)
    assert (os.path.isfile(conceptsExport)  == True)

    al.outputCSVtoFile(concepts, exportCSV)
    assert (os.path.isfile(exportCSV)  == True)

def goArchiLib():

    test_CheckForArchimateFile(cleandir)
    test_Archi_Counts(cleandir)
    test_ExportArchi(cleandir)
    test_ExportArchiFolderModels(cleandir)
    test_ExportArchiModel(cleandir)

if __name__ == "__main__":
    goArchiLib()