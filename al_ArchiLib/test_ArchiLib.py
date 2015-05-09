#!/usr/bin/python
#
# al_ArchiLib Testing
#
__author__ = u'morrj140'
__VERSION__ = u'0.1'

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

from Constants import *
from ArchiLib import ArchiLib

import pytest

@pytest.fixture(scope=u"module")
def cleandir():
    cwd = os.getcwd()

    listFiles = list()
    listFiles.append(u"Estimation.p")
    listFiles.append(u"export.p")
    listFiles.append(u"report.csv")
    listFiles.append(u"export.csv")

    for lf in listFiles:
        ftr = cwd + os.sep + u"test" + os.sep + lf

        if os.path.exists(ftr):
            logger.info(u"remove : %s" % ftr)
            os.remove(ftr)

@pytest.mark.ArchiLib
def test_Archi_Counts(cleandir):

    if __name__ == u"__main__":
        cleandir()

    assert (os.path.isfile(fileArchimateTest) is True)
    logger.info(u"Exists : %s" % fileArchimateTest)

    # archimate:TriggeringRelationship : 4 != 24
    # archimate:UsedByRelationship : 12 != 72
    # archimate:ApplicationService : 6 != 36
    # archimate:AccessRelationship : 13 != 78
    # archimate:FlowRelationship : 5 != 30
    # archimate:DataObject : 5 != 30
    # archimate:BusinessObject : 5 != 30
    # archimate:BusinessProcess : 7 != 42
    # archimate:BusinessEvent : 2 != 12
    # archimate:ApplicationComponent : 3 != 18

    testDict = {u"archimate:TriggeringRelationship" : 4 , u"archimate:UsedByRelationship" : 12,
                u"archimate:ApplicationService" : 6, u"archimate:AccessRelationship" : 13,
                u"archimate:FlowRelationship" : 5, u"archimate:DataObject" : 5 ,
                u"archimate:BusinessObject" : 5, u"archimate:BusinessProcess" : 7,
                u"archimate:BusinessEvent" : 2, u"archimate:ApplicationComponent" : 3,
                u"archimate:Requirement" : 2}

    al = ArchiLib(fileArchimateTest)

    listCounts = al.logTypeCounts()

    assert(listCounts is not None)

    logger.info(u"listCounts : %d" % len(listCounts))

    assert (len(listCounts) == len(testDict))

    TestStatus = True

    for x in listCounts:
        logger.info(u"%s, %s == %s" % (x[0], x[1], testDict[x[0]]))

        if testDict[x[0]] == x[1]:
            logger.info(u"%s, %s == %s" % (x[0], x[1], testDict[x[0]]))
        else:
            logger.error(u"%s : %s != %s" % (x[0], x[1], testDict[x[0]]))
            TestStatus = False

    #assert (TestStatus is True)

@pytest.mark.ArchiLib
def test_CheckForArchimateFile(cleandir):

    if __name__ == u"__main__":
        cleandir()

    assert (os.path.isfile(fileArchimateTest) is True)

@pytest.mark.ArchiLib
def test_ExportArchi(cleandir):

    if __name__ == u"__main__":
        cleandir()

    logger.info(u"Using : %s" % fileArchimateTest)

    assert (os.path.isfile(fileArchimateTest) is True)

    al = None
    concepts = None

    al = ArchiLib(fileArchimateTest)

    assert (al is not None)

    concepts = Concepts(u"Node", u"Nodes")

    assert (concepts is not None)

    logger.info(u"Found %d Nodes" % len(al.dictNodes))
    logger.info(u"Found %d Edges" % len(al.dictEdges))

    assert (len(al.dictNodes) == 42)
    assert (len(al.dictEdges) == 35)

    count = 0
    listTSort = list()
    for x in al.dictEdges.keys():
        logger.info(u"[%s]=%s" % (al.dictEdges[x][u"id"], x))

        if u"source" in al.dictEdges[x]:
            source = al.dictEdges[x][u"source"]
            target = al.dictEdges[x][u"target"]

            logger.info(u"  Rel    : %s" % (al.dictEdges[x][ARCHI_TYPE]))

            sourceName = al.getNodeName(source)
            targetName = al.getNodeName(target)

            logger.info(u" %s--%s--%s" % (sourceName, al.dictEdges[x][ARCHI_TYPE][10:], targetName))

            sc = concepts.addConceptKeyType(sourceName, al.dictNodes[source][ARCHI_TYPE][10:])
            # getWords(sourceName, sc)

            tc = sc.addConceptKeyType(targetName, al.dictNodes[target][ARCHI_TYPE][10:])
            # getWords(sourceName, tc)

    Concepts.saveConcepts(concepts, fileConceptsExport)

    assert(len(concepts.cd) == 17)

    assert (os.path.isfile(fileConceptsExport) is True)

    assert(concepts.typeName == u"Nodes")

@pytest.mark.ArchiLib
def test_ExportArchiFolderModels(cleandir):

    if __name__ == u"__main__":
        cleandir()

    assert (os.path.isfile(fileArchimateTest) is True)
    al = ArchiLib(fileArchimateTest)

    folder = u"Scenarios"

    logger.info(u"Exporting Folder : %s" % folder)
    listMTE = al.getModelsInFolder(folder)
    assert (listMTE is not None)

    logger.info(u"len(listMTE) = %d" % len(listMTE))
    assert (len(listMTE) == 2)

    concepts = Concepts(u"Export", u"Pickle")

    for ModelToExport in listMTE:
        logger.info(u"  Model : %s" % ModelToExport)
        d = concepts.addConceptKeyType(ModelToExport, u"Model")
        al.recurseModel(ModelToExport, d)

    al.outputCSVtoFile(concepts, fileExport=fileCSVExport)
    assert (os.path.isfile(fileCSVExport) is True)

    Concepts.saveConcepts(concepts, fileConceptsExport)
    logger.info(u"Save Concepts : %s" % fileConceptsExport)

    assert (os.path.isfile(fileConceptsExport) is True)

@pytest.mark.ArchiLib
def test_ArchimateConcepts(cleandir):

    if __name__ == u"__main__":
        cleandir()

    logger.info(u"Using : %s" % fileArchimateTest)

    assert (os.path.isfile(fileArchimateTest) is True)

    concepts = Concepts(fileConceptsArch, u"Archimate")

    al = ArchiLib(fileArchimateTest)

    #
    # Create Concepts from Archimate
    #
    al.folderConcepts(concepts)

    Concepts.saveConcepts(concepts, fileConceptsArch)
    logger.info(u"Saved concepts to : %s" % fileConceptsArch)

    assert (os.path.isfile(fileConceptsArch) is True)

@pytest.mark.ArchiLib
def test_ExportArchiModel(cleandir):

    if __name__ == u"__main__":
        cleandir()

    assert (os.path.isfile(fileArchimateTest) is True)

    al = ArchiLib(fileArchimateTest)

    listMTE = list()
    listMTE.append(u"01. Market to Leads")

    concepts = Concepts(u"Export", u"Model")

    for ModelToExport in listMTE:
        al.recurseModel(ModelToExport, concepts)

    Concepts.saveConcepts(concepts, fileConceptsExport)
    assert (os.path.isfile(fileConceptsExport) is True)

    al.outputCSVtoFile(concepts, fileCSVExport)
    assert (os.path.isfile(fileCSVExport) is True)

def goArchiLib():

    test_CheckForArchimateFile(cleandir)
    test_Archi_Counts(cleandir)
    test_ExportArchi(cleandir)
    test_ExportArchiFolderModels(cleandir)
    test_ExportArchiModel(cleandir)

if __name__ == u"__main__":
    goArchiLib()