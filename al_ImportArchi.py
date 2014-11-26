#!/usr/bin/python
#
# Archimate to Concepts
#
import sys
import os
import StringIO
import csv
import random
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

NS_MAP={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}
XML_NS         =  NS_MAP["xsi"]
ARCHIMATE_NS   =  NS_MAP["archimate"]

ARCHI_TYPE = "{%s}type" % NS_MAP["xsi"]

dictRelation = dict()
dictName = dict()

def cleanString(s):
    r = ""
    if s == None:
        return r

    for x in s.lstrip(" "):
        if x.isalnum() or x in (" ", "-", "."):
            r = r + x
    return r.lstrip(" ").rstrip(" ")

def checkDuplicate(dmID, x, tree):
    xp = "//element[@id='" + dmID + "']"
    dm = tree.xpath(xp)[0]

    dml = dm.getchildren()

    Duplicate = False
    for xdml in dml:
        logger.info("%s" % (xdml.get("name")))
        xdml_name = xdml.get("name")
        if xdml_name == x.name:
            logger.debug("%s Duplicate!" % xdml.get("id"))
            return xdml.get("id")

    logger.debug("dml[%d]" % (len(dml)))

    return None

def outputXML(tree):
    output = StringIO.StringIO()
    tree.write(output, pretty_print=True)
    logger.info("%s" % (output.getvalue()))

def findDiagramModel(tree, id):
    xp = "//element[@id='" + id + "']"
    stp = tree.xpath(xp)
    return stp

def findDiagramObject(tree, id):
    xp = "//child[@id='%s']" % id
    stp = tree.xpath(xp)
    return stp

def findDiagramObject(tree, id):
    xp = "//child[@id='%s']" % id
    stp = tree.xpath(xp)
    return stp

def findElement(tree, name):
    xp = "//element[@name='%s']" % name.rstrip(" ").lstrip(" ")
    stp = tree.xpath(xp)
    return stp

def getID():
    r = str(hex(random.randint(0, 16777215)))[-6:] + str(hex(random.randint(0, 16777215))[-2:])

    if r[0] == "x":
        return getID()
    return r

def insertNode(tag, folder, tree, attrib):

    logger.debug("attrib: %s" % (attrib))

    value = attrib["name"].rstrip(" ").lstrip(" ")

    if value != attrib["name"]:
        logger.debug("diff value .%s:%s." % (value, attrib["name"]))

    if dictName.has_key(value):
        idd = dictName[value]
        attrib["id"] = idd

        logger.debug("inFound! : %s" % idd)
    else:
        idd =  getID()
        dictName[value] = idd
        attrib["id"] = idd

        xp = "//folder[@name='" + folder + "']"
        elm = etree.Element(tag, attrib, nsmap=NS_MAP)

        txp = tree.xpath(xp)
        txp[0].insert(0, elm)
        logger.debug("inNew!   : %s" % idd)

    return idd

def insertRel(tag, folder, tree, attrib):

    logger.debug("attrib: %s" % (attrib))

    value = "%s--%s" % (attrib["source"], attrib["target"])

    if dictName.has_key(value):
        idd = dictName[value]
        attrib["id"] = idd

        logger.debug("inFound! : %s" % idd)
    else:
        idd =  getID()
        dictName[value] = idd
        attrib["id"] = idd

        xp = "//folder[@name='" + folder + "']"
        elm = etree.Element(tag, attrib, nsmap=NS_MAP)
        tree.xpath(xp)[0].insert(0, elm)
        logger.info("inNew!   : %s" % idd)

    return idd

def getNameID(value):
    logger.info("    Search for : %s" % value)
    if dictName.has_key(value):
        idd = dictName[value]
        logger.debug("    Found! : %s" % idd)
    else:
        idd =  getID()
        dictName[value] = idd
        logger.debug(    "New I  : %s" % idd)

    logger.debug("%s" % dictName)

    return idd

def logNode(n, type):

    attributes = n.attrib
    if type != None:
        if isinstance(type, tuple) or isinstance(type, list):
            if attributes.get(ARCHI_TYPE) in type:
                if attributes.get("id") != None:
                    dictName[n.get("name")] = attributes["id"]
        else:
            if attributes.get(ARCHI_TYPE) == type:
                if attributes.get("id") != None:
                    dictName[n.get("name")] = attributes["id"]

    logger.debug("logNode : %s:%s:%s:%s" % (n.tag, n.get("name"), n.get("id"), attributes.get(ARCHI_TYPE)))

    for y in n:
        logNode(y, type)

def logAll(tree, type="archimate:ApplicationComponent"):
    for x in tree.getroot():
        logNode(x, type)

def outputXML(tree, filename="import_artifacts.archimate"):#
    output = StringIO.StringIO()
    tree.write(output, pretty_print=True)

    logger.debug("%s" % (output.getvalue()))

    logger.info("Saved to : %s" % filename)

    f = open(filename,'w')
    f.write(output.getvalue())
    f.close()

    output.close()

def insertTwoColumns(tree, folder, subfolder, fileMetaEntity, eType):

    #<element xsi:type="archimate:Node" id="612a9b73" name="Linux Server"/>

    file = open(fileMetaEntity, "rU")
    reader = csv.reader(file)

    xp = "folder[@name='" + folder + "']"
    tag = "element"

    # <folder name="Process" id="e23b1e50">

    attrib = dict()
    attrib["id"] = getID()
    attrib["name"] = subfolder
    insertNode("folder", folder, tree, attrib)

    folder = subfolder

    rownum = 0

    for row in reader:
        if rownum == 0:
            rownum += 1
            continue

        logger.info("rownum : %d" % rownum)
        logger.info("row    : %s" % row)

        CM1 = row[0].decode(encoding='UTF-8',errors='ignore').lstrip()
        CM2 = row[1].decode(encoding='UTF-8',errors='ignore').lstrip()

        C1 = CM1
        attrib = dict()
        attrib["name"] = CM1
        attrib[ARCHI_TYPE] = eType
        insertNode(tag, folder, tree, attrib)
        CM1_ID = attrib["id"]

        C2 = CM2
        attrib = dict()
        attrib["name"] = CM2
        attrib[ARCHI_TYPE] = eType
        insertNode(tag, folder, tree, attrib)
        CM2_ID = attrib["id"]

        attrib = dict()
        attrib["source"] = CM1_ID
        attrib["target"] = CM2_ID
        attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
        insertRel(tag, "Relations", tree, attrib)

        C1 = C1.replace(":",".")
        C1 = C1.replace("|",".")
        C1 = C1.replace(" ",".")
        C1 = C1.replace("_",".")
        C1 = C1.replace(" ",".")

        listC1 = list()
        for x in C1.split("."):
            attrib = dict()
            attrib["name"] = x
            attrib[ARCHI_TYPE] = eType
            insertNode(tag, folder, tree, attrib)
            listC1.append(attrib["id"])

        C2 = C2.replace(":",".")
        C2 = C2.replace("|",".")
        C2 = C2.replace(" ",".")
        C2 = C2.replace("_",".")
        C2 = C2.replace(" ",".")

        listC2 = list()
        for x in C2.split("."):
            attrib = dict()
            attrib["name"] = x
            attrib[ARCHI_TYPE] = eType
            insertNode(tag, folder, tree, attrib)
            listC2.append(attrib["id"])

        if len(listC1) > 1:
            pl = listC1[0]
            for y in listC1[1:]:
                attrib = dict()
                attrib["source"] = pl
                attrib["target"] = y
                attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                insertRel(tag, "Relations", tree, attrib)
                pl = y

        if len(listC2) > 1:
            pl = listC2[0]
            for y in listC2[1:]:
                attrib = dict()
                attrib["source"] = pl
                attrib["target"] = y
                attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                insertRel(tag, "Relations", tree, attrib)
                pl = y

        attrib = dict()
        attrib["source"] = listC1[0]
        attrib["target"] = listC2[0]
        attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
        insertRel(tag, "Relations", tree, attrib)

        attrib = dict()
        attrib["source"] = CM1_ID
        attrib["target"] = listC1[0]
        attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
        insertRel(tag, "Relations", tree, attrib)

        attrib = dict()
        attrib["source"] = CM2_ID
        attrib["target"] = listC2[0]
        attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
        insertRel(tag, "Relations", tree, attrib)

def insertNColumns(tree, folder, subfolder, fileMetaEntity):

    #<element xsi:type="archimate:Node" id="612a9b73" name="Linux Server"/>

    file = open(fileMetaEntity, "rU")
    reader = csv.reader(file)

    xp = "folder[@name='" + folder + "']"
    tag = "element"

    # <folder name="Process" id="e23b1e50">

    attrib = dict()
    attrib["id"] = getID()
    attrib["name"] = subfolder
    insertNode("folder", folder, tree, attrib)

    folder = subfolder

    rownum = 0

    previous = dict()

    listColumnHeaders = list()

    for row in reader:
        if rownum == 0:
            rownum += 1
            for col in row:
                colType = "archimate:%s" % col
                listColumnHeaders.append(colType)
            continue

        logger.info("rownum : %d" % rownum)
        logger.info("row    : %s" % row)

        p = None
        colnum = 0

        for col in row:
            logger.info("    %d   [%s] %s" % (colnum, listColumnHeaders[colnum], col))

            CM = cleanString(col.decode(encoding='ASCII',errors='ignore').lstrip())

            logger.info("CM : %s" % CM)

            if CM == "":
                CM = previous[colnum]
            else:
                previous[colnum] = CM

            attrib = dict()
            attrib["name"] = CM
            attrib[ARCHI_TYPE] = listColumnHeaders[colnum]
            insertNode(tag, folder, tree, attrib)
            CM_ID = attrib["id"]

            if p != None:
                attrib = dict()
                attrib["source"] = CM_ID
                attrib["target"] = p
                attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                insertRel(tag, "Relations", tree, attrib)

                p = CM_ID
            else:
                p = CM_ID

            colnum += 1

        #previous = row

def insertScenarios(tree, fileMetaEntity):

    #<element xsi:type="archimate:Node" id="612a9b73" name="Linux Server"/>

    file = open(fileMetaEntity, "rU")
    reader = csv.reader(file)

    folder = "Relations"
    xp = "folder[@name='" + folder + "']"
    tag = "element"

    type = "archimate:AssociationRelationship"

    count = 0
    rownum = 0

    scenario = ""
    scenarioID = 0

    for row in reader:
        logger.info("rownum : %d" % rownum)
        logger.info("row    : %s" % row)
        if row[0] == "Scenario":
            scenario = row[5].decode(encoding='UTF-8',errors='ignore')
            site = row[1].decode(encoding='UTF-8',errors='ignore')

            attrib = dict()
            attrib["name"] = scenario
            attrib[ARCHI_TYPE] = "archimate:BusinessEvent"
            insertNode("element", "Business", tree, attrib)
            scenarioID = attrib["id"]

            attrib = dict()
            attrib["name"] = site
            attrib[ARCHI_TYPE] = "archimate:BusinessFunction"
            insertNode("element", "Business", tree, attrib)
            siteID = attrib["id"]

            attrib = dict()
            attrib["source"] = siteID
            attrib["target"] = scenarioID
            attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
            insertRel("element", "Relations", tree, attrib)

        elif row[0] == "Sub":
            subscenario = row[5].decode(encoding='UTF-8',errors='ignore')
            site = row[1].decode(encoding='UTF-8',errors='ignore')

            attrib = dict()
            attrib["name"] = subscenario.decode(encoding='UTF-8',errors='ignore')
            attrib[ARCHI_TYPE] = "archimate:BusinessProcess"
            insertNode("element", "Business", tree, attrib)
            subscenarioID = attrib["id"]

            attrib = dict()
            attrib["source"] = scenarioID
            attrib["target"] = subscenarioID
            attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
            insertRel("element", "Relations", tree, attrib)

            attrib = dict()
            attrib["source"] = siteID
            attrib["target"] = subscenarioID
            attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
            insertRel("element", "Relations", tree, attrib)

        elif row[0] == "Req":

            try:
                segment = row[1]
                entity = row[4]
                requirement = row[5]
                category = row[6]
                subcategory = row[7]

                attrib = dict()
                attrib["name"] = requirement
                attrib[ARCHI_TYPE] = "archimate:Requirement"
                insertNode("element", "Motivation", tree, attrib)
                requirementID = attrib["id"]

                attrib = dict()
                attrib["name"] = entity
                attrib[ARCHI_TYPE] = "archimate:BusinessObject"
                insertNode("element", "Business", tree, attrib)
                entityID = attrib["id"]

                attrib = dict()
                attrib["name"] = segment
                attrib[ARCHI_TYPE] = "archimate:BusinessFunction"
                insertNode("element", "Business", tree, attrib)
                segmentID = attrib["id"]

                attrib = dict()
                attrib["name"] = category
                attrib[ARCHI_TYPE] = "archimate:BusinessFunction"
                insertNode("element", "Business", tree, attrib)
                categoryID = attrib["id"]

                attrib = dict()
                attrib["name"] = subcategory
                attrib[ARCHI_TYPE] = "archimate:BusinessFunction"
                insertNode("element", "Business", tree, attrib)
                subcategoryID = attrib["id"]

                attrib = dict()
                attrib["source"] = entityID
                attrib["target"] = requirementID
                attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                insertRel("element", "Relations", tree, attrib)


                attrib = dict()
                attrib["source"] = categoryID
                attrib["target"] = subcategoryID
                attrib[ARCHI_TYPE] = "archimate:CompositionRelationship"
                insertRel("element", "Relations", tree, attrib)

                attrib = dict()
                attrib["source"] = scenarioID
                attrib["target"] = requirementID
                attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                insertRel("element", "Relations", tree, attrib)

                attrib = dict()
                attrib["source"] = subcategoryID
                attrib["target"] = requirementID
                attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                insertRel("element", "Relations", tree, attrib)

                attrib = dict()
                #attrib["id"] = getID()
                attrib["source"] = segmentID
                attrib["target"] = requirementID
                attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                insertRel("element", "Relations", tree, attrib)
            except:
                logger.warn("ops...%s" % row)
        else:
            logger.info("Unknown line - %s" % row)
            pass

        rownum += 1

def insertConcepts(tree, concepts, n=0):

    for x in concepts.getConcepts().values():
        logger.info("x : %s" % x.name)
        for y in x.getConcepts().values():
            logger.info("  y : %s" % y.name)
            attrib = dict()
            attrib["name"] = x.name
            attrib[ARCHI_TYPE] = "archimate:WorkPackage"
            insertNode("element", "Implementation & Migration", tree, attrib)
            wp1 = attrib["id"]

            attrib = dict()
            attrib["name"] = y.name
            attrib[ARCHI_TYPE] = "archimate:BusinessProcess"
            insertNode("element", "Process", tree, attrib)
            wp2 = attrib["id"]

            attrib = dict()
            attrib["source"] = wp1
            attrib["target"] = wp2
            attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
            insertRel("element", "Relations", tree, attrib)


if __name__ == "__main__":
    # Archimate
    fileArchimate = "//Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v4.archimate"
    etree.QName(ARCHIMATE_NS, 'model')
    tree = etree.parse(fileArchimate)

    logAll(tree)

    fileMetaEntity = "/Users/morrj140/Development/GitRepository/ArchiConcepts/DVC_20141125_Business Requirements.csv"
    logger.info("Using : %s" % fileArchimate)
    insertNColumns(tree, "Motivation", "BusinessRequirements", fileMetaEntity)


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