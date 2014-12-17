#!/usr/bin/python
#
# Archimate to Concepts
#
import sys
import os
import StringIO
import csv
import random

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from al_ArchiLib import *

if __name__ == "__main__":
    # Archimate
    fileArchimate = "//Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v6.archimate"
    etree.QName(ARCHIMATE_NS, 'model')
    tree = etree.parse(fileArchimate)

    logAll(tree)

    fileMetaEntity = "/Users/morrj140/Development/GitRepository/ArchiConcepts/DVC Business Requirements.csv"
    logger.info("Using : %s" % fileArchimate)
    insertNColumns(tree, "Motivation", "BusinessRequirements20141126", fileMetaEntity)


    #fileMetaEntity = "/Users/morrj140/Development/GitRepository/ArchiConcepts/Who_What_How_20141024.csv"
    #logger.info("Using : %s" % fileArchimate)
    #insertNColumns(tree, "Motivation", "Who_What_How_20141024", fileMetaEntity)

    #fileMetaEntity = "/Users/morrj140/Development/GitRepository/ArchiConcepts/Gaps20141104.csv"
    #logger.info("Using : %s" % fileArchimate)
    #insertNColumns(tree, "Implementation & Migration", "Gaps20141104", fileMetaEntity, eType="archimate:Gap")

    #concepts = Concepts.loadConcepts("batches.p")
    #insertConcepts(tree, concepts)

    # MQ
    #fileMetaEntity = "/Users/morrj140/Documents/SolutionEngineering/CodeGen/EAI Analysis/MQ Messages.csv"
    #logger.info("Using : %s" % fileArchimate)
    #insertTwoColumns(tree, "Application", "MQ Messages", fileMetaEntity, eType="archimate:ApplicationService")

    #fileMetaEntity = "/Users/morrj140/Development/GitRepository/ArchiConcepts/Party-Product-GuestComm_Func.csv"
    #fileMetaEntity = "/Users/morrj140/Development/GitRepository/ArchiConcepts/AR Functional Interface Mapping - Order, Payment & Accounting.csv"
    #logger.info("Using : %s" % fileArchimate)
    #insertNColumns(tree, "Application", "Order-Payment-Accounting", fileMetaEntity, eType="archimate:ApplicationService")


    # EAI
    #fileMetaEntity = "/Users/morrj140/Documents/SolutionEngineering/CodeGen/EAI Analysis/EAI.csv"
    #logger.info("Using : %s" % fileArchimate)
    #insertTwoColumns(tree, "Application", "EAI Services", fileMetaEntity, eType="archimate:ApplicationService")

    # Jawa
    #fileMetaEntity = "/Users/morrj140/Documents/SolutionEngineering/CodeGen/EAI Analysis/Jawa.csv"
    #logger.info("Using : %s" % fileArchimate)
    #insertTwoColumns(tree, "Application", "Jawa Services", fileMetaEntity, eType="archimate:ApplicationService")

    # Segment/Category
    #fileMetaEntity = "/Users/morrj140/Development/GitRepository/DirCrawler/CodeGen-SC.csv"
    #folders = ("Business", "Business")
    #types = ("archimate:BusinessFunction", "archimate:BusinessFunction")
    #logger.info("Using : %s" % fileArchimate)
    #type = "archimate:BusinessFunction"
    #insertNNodes(tree, folders, types, fileMetaEntity)
    #insertNRelations(tree, fileMetaEntity)

    # Requirements
    # Segment/Category
    #fileMetaEntity = "/Users/morrj140/Development/GitRepository/DirCrawler/CodeGen-Req.csv"
    #folders = ("Motivation", "Business", "Business")
    #types = ("archimate:Requirement", "archimate:BusinessFunction", "archimate:BusinessFunction")

    #logger.info("Using : %s" % fileArchimate)

    #insertNNodes(tree, folders, types, fileMetaEntity)
    #insertNRelations(tree, fileMetaEntity)

    # Artifacts
    #fileMetaEntity = "/Volumes/user/Artifacts.csv"
    #logger.info("Using : %s" % fileArchimate)
    #insertIntoFolder(tree, "Technology", fileMetaEntity, eType="archimate:Artifact")
    #insertIntoFolder(tree, "Relations", fileMetaEntity,  eType="archimate:Artifact")

    # Capability
    #fileMetaEntity = "/Users/morrj140/Development/GitRepository/DirCrawler/Mega/Capability.csv"
    #logger.info("Using : %s" % fileArchimate)
    #insertIntoFolder(tree, "Business", fileMetaEntity, eType="archimate:BusinessFunction")
    #insertIntoFolder(tree, "Relations", fileMetaEntity, eType="archimate:BusinessFunction")

    # Functions
    #fileMetaEntity = "/Users/morrj140/Development/GitRepository/DirCrawler/Mega/Function2.csv"
    #logger.info("Using : %s" % fileArchimate)
    #insertIntoFolder(tree, "Business", fileMetaEntity, eType="archimate:BusinessFunction")

    # Stakeholders
    #fileMetaEntity = "/Users/morrj140/Development/GitRepository/DirCrawler/Mega/Function.csv"
    #logger.info("Using : %s" % fileArchimate)
    #insertIntoFolder(tree, "Motivation", fileMetaEntity, eType="archimate:Stakeholder")
    #insertIntoFolder(tree, "Relations", fileMetaEntity, eType="archimate:BusinessFunction")

    outputXML(tree)