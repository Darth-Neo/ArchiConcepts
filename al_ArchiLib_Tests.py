#!/usr/bin/python
#
# al_ArchiLib Testing
#
__author__ = 'morrj140'
import sys
import os
import StringIO
import time

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from al_ArchiLib import *

fileArchimate = "Testing.archimate"

def test_Archi_Counts():

    assert (os.path.isfile(fileArchimate)  == True)

    TestStatus = True

    testDict = {"archimate:TriggeringRelationship" : 4 , "archimate:UsedByRelationship" : 12,
                "archimate:ApplicationService" : 6, "archimate:AccessRelationship" : 13,
                "archimate:FlowRelationship" : 5, "archimate:DataObject" : 5 ,
                "archimate:BusinessObject" : 5, "archimate:BusinessProcess" : 7,
                "archimate:BusinessEvent" : 2, "archimate:ApplicationComponent" : 3}

    al = ArchiLib(fileArchimate)

    listCounts = al.logTypeCounts(ListOnly=True)

    assert (len(listCounts)   == 10)

    for x in listCounts:
        if testDict[x[0]] == x[1] :
            logger.info("%s, %s == %s" % (x[0], x[1], testDict[x[0]]))
        else:
            logger.error("%s : %s != %s" % (x[0], x[1], testDict[x[0]]))
            TestStatus = False

    if TestStatus == False:
        logger.error("=====Test Failed!=====")

    else:
        logger.info ("_____Test Passed_____")

    assert (TestStatus == True)

def test_CheckForArchimateFile():

    assert (os.path.isfile(fileArchimate)  == True)

def test_ExportArchi():
    fileConcepts = "export.p"

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

    Concepts.saveConcepts(concepts, fileConcepts)

    assert(len(concepts.cd) == 17)

    assert (os.path.isfile(fileConcepts)  == True)

    assert(concepts.typeName == "Nodes")

def test_ExportArchiFolderModels():
    fileExport="report.csv"
    conceptsFile = "Estimation.p"

    assert (os.path.isfile(fileArchimate)  == True)
    al = ArchiLib(fileArchimate, fileExport)

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

    al.outputCSVtoFile(concepts, fileExport=fileExport)
    assert (os.path.isfile(fileExport)  == True)

    Concepts.saveConcepts(concepts, conceptsFile)
    logger.info("Save Concepts : %s" % conceptsFile)

    assert (os.path.isfile(conceptsFile)  == True)


def test_ArchimateConcepts():
    fileArchiP = "archi.p"
    fileArchiModel = "Testing.archimate"

    logger.info("Using : %s" % fileArchimate)

    assert (os.path.isfile(fileArchimate)  == True)

    concepts = Concepts(fileArchiP, "Archimate")

    al = ArchiLib(fileArchimate)

    #
    # Create Concepts from Arhimate
    #
    al.folderConcepts(concepts)

    Concepts.saveConcepts(concepts, fileArchiP)
    logger.info("Saved concepts to : %s" % fileArchiP)

    assert (os.path.isfile(fileArchiP)  == True)

def test_ExportArchiModel():
    conceptsFile = "Estimation.p"
    fileExport="export.csv"

    assert (os.path.isfile(fileArchimate)  == True)

    al = ArchiLib(fileArchimate, fileExport)

    listMTE = list()
    listMTE.append("01. Market to Leads")

    concepts = Concepts("Export", "Model")

    for ModelToExport in listMTE:
        al.recurseModel(ModelToExport, concepts)

    Concepts.saveConcepts(concepts, conceptsFile)
    assert (os.path.isfile(conceptsFile)  == True)

    al.outputCSVtoFile(concepts)
    assert (os.path.isfile(fileExport)  == True)

if __name__ == "__main__":

    #test_CheckForArchimateFile()
    #test_Archi_Counts()
    #test_ExportArchi()
    #test_ExportArchiFolderModels()
    test_ExportArchiModel()