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

ArtifactColumns = ["Artifact ID", "Artifact Name", "Owner Artifact ID", "Owner Artifact Name"]

CapabilityColumns = ["Capability Name","Capability Type","Capability Created Date","Capability Modified Date",
                     "Capability Hex ID","Capability Comment","Parent Capability Hex ID"]

FunctionColumns = ["Function Name","Function Created Date","Function Modified Date","Function Hex ID",
                   "Function Comment","Function Org Unit Name","Function Org Unit Hex ID","Function Project Hex ID"]

RequirementColumns = ["General System Requirements", "RollUp Segment", "Category"]

keyColumns = { "Artifact" : (0,2), "BusinessFunction" : (4, 6), "Function" : (3, 6), "Stakeholder" : (6, 3),
               "Requirement" : (-1,-1), "Category" : (-1, -1)}
nameColumns = { "Artifact" : (1,3), "BusinessFunction" : (0, 6), "Function" : (0, 5), "Stakeholder" : (5, 0),
                "Requirement" : (1,0), "Category" : (0,1)}

dictNode = dict()
dictRelation = dict()
dictName = dict()

def getID():
    return str(hex(random.randint(0, 16777215)))[-6:] + str(hex(random.randint(0, 16777215))[-2:])

def insertNode(tag, folder, tree, attrib):

    logger.info("attrib: %s" % (attrib))

    value = attrib["name"].lower()

    if dictName.has_key(value):
        idd = dictName[value]
        attrib["id"] = idd

        logger.debug("inFound! : %s" % idd)
    else:
        idd =  getID()
        dictName[value] = idd
        attrib["id"] = idd

        xp = "folder[@name='" + folder + "']"
        elm = etree.Element(tag, attrib, nsmap=NS_MAP)
        tree.xpath(xp)[0].insert(0, elm)
        logger.info("inNew!   : %s" % idd)

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

        xp = "folder[@name='" + folder + "']"
        elm = etree.Element(tag, attrib, nsmap=NS_MAP)
        tree.xpath(xp)[0].insert(0, elm)
        logger.info("inNew!   : %s" % idd)

    return idd


def getNameID(value):
    logger.info("    Search for : %s" % value)
    if dictName.has_key(value):
        idd = dictName[value]
        logger.info("    Found! : %s" % idd)
    else:
        idd =  getID()
        dictName[value] = idd
        logger.info(    "New I  : %s" % idd)

    logger.debug("%s" % dictName)

    return idd

def insertMNode(p, row, se, tag="element", eType="archimate:Artifact"):
    #<element xsi:type="archimate:Node" id="612a9b73" name="Linux Server"/>

    logger.debug("%s::%s" % (row[0], row[1]))

    # Generate 8 digit Hex number
    id = getID()
    logger.debug("id : %s" % (id))

    attrib = dict()
    attrib["id"] = id
    in_id = eType[10:]
    logger.info("in_id : %s" % (in_id))

    colnum = nameColumns[in_id][0]
    logger.info("colnum : %s" % (colnum))

    attrib["name"] = row[colnum].decode(encoding='UTF-8',errors='ignore')
    attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] = eType

    colnum = keyColumns[in_id][0]
    if colnum == -1:
        value = row[0].decode(encoding='UTF-8',errors='ignore')
    else:
        value = row[colnum].decode(encoding='UTF-8',errors='ignore')

    logger.info("value : %s" % (value))

    if len(value) == 0:
        value = row[0]

    if dictNode.has_key(value):
        return 0
    else:
        dictNode[value] = id
        dictName[attrib["name"]] = id

    elm = etree.Element(tag, attrib, nsmap=NS_MAP)
    se[0].insert(0, elm)

    return 1

def insertMRelation(p, row, se, tag="element", eType="archimate:Artifact"):

    #<folder name="Relations" id="c1ff528d" type="relations">
    # <element xsi:type="archimate:AssociationRelationship" id="b0341e0e" source="ea7c85c4" target="e38ecb1d"/>

    # Generate 8 digit Hex number
    id = getID()

    #name = row[1]
    in_id = eType[10:]
    colnum = nameColumns[in_id][0]

    if len(row[colnum].strip()) > 0:
        attrib = dict()
        attrib["id"] = id

        if colnum == -1:
            NodeID1 = row[0].decode(encoding='UTF-8',errors='ignore')
            attrib["source"] = getNameID(NodeID1)
        else:
            NodeID1 = row[colnum].decode(encoding='UTF-8',errors='ignore')
            attrib["source"] = dictName[NodeID1]

        colnum = keyColumns[eType[10:]][1]
        if colnum == -1:
            NodeID2 = row[1].decode(encoding='UTF-8',errors='ignore')
            attrib["target"] = getNameID(NodeID2)
        else:
            NodeID2 = row[colnum].decode(encoding='UTF-8',errors='ignore')
            attrib["target"] = dictName[NodeID2]

        attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] = "archimate:AssociationRelationship"

        hash = NodeID1 + NodeID2

        if dictRelation.has_key(hash):
            return 0
        else:
            dictRelation[hash] = NodeID1 + NodeID2

        logger.debug("%s::%s" % (row[0], row[1]))

        elm = etree.Element(tag, attrib, nsmap=NS_MAP)
        se[0].insert(0, elm)

        return 1

    return 0


def insertIntoFolder(tree, folder, fileMetaEntity, eType):

    file = open(fileMetaEntity, "rU")
    reader = csv.reader(file)

    xp = "folder[@name='" + folder + "']"
    se = tree.xpath(xp)
    p = se[0].getparent()

    count = 0
    rownum = 0
    for row in reader:

        if rownum == 0:
            rownum += 1
            continue
        else:
            rownum += 1

        logger.debug("%d\t%s" % (rownum, row))

        if len(row[0].strip()) == 0:
            break

        if folder == "Relations":
            count += insertMRelation(p, row, se, eType=eType)
        else:
            count += insertMNode(p, row, se, eType=eType)

    logger.info("%d inserted in %s" % (count, folder))

    file.close()


def insertNNodes(tree, folders, types, fileMetaEntity):
    #<element xsi:type="archimate:Node" id="612a9b73" name="Linux Server"/>

    file = open(fileMetaEntity, "rU")
    reader = csv.reader(file)

    tag = "element"

    rownum = 0

    for row in reader:

        # Skip first Rom
        if rownum == 0:
            rownum += 1
            continue
        else:
            rownum += 1

        logger.info("%d\t%s" % (rownum, row))

        # Stop
        if len(row[0].strip()) == 0:
            break

        colnum = 0
        for col in row:
            logger.info("%d\t%s" % (colnum, col))

            # Nodes
            folder = folders[colnum]
            logger.debug("Folder[%d] : %s" % (colnum, folder))

            name = col.decode(encoding='UTF-8',errors='ignore').strip()
            attrib = dict()
            attrib["name"] = name
            attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] = types[colnum]
            insertNode(tag, folder, tree, attrib)
            logger.debug("Node:%s,%s" % (attrib["id"], attrib["name"]))
            colnum += 1

def insertNRelations(tree, fileMetaEntity):
    #<element xsi:type="archimate:Node" id="612a9b73" name="Linux Server"/>

    file = open(fileMetaEntity, "rU")
    reader = csv.reader(file)

    folder = "Relations"
    xp = "folder[@name='" + folder + "']"
    tag = "element"

    type = "archimate:AssociationRelationship"

    count = 0
    rownum = 0

    for row in reader:

        if rownum == 0:
            rownum += 1
            continue
        else:
            rownum += 1

        logger.info("%d\t%s" % (rownum, row))

        if len(row[0].strip()) == 0:
            break

        #Relations
        colnum = 0
        for col in row:

            # Skip first Rom
            if colnum == 0:
                colnum += 1
                continue

            logger.info("%d\t%s" % (colnum, row))

            # Stop
            if len(row[0].strip()) == 0:
                break

            # Nodes
            attrib = dict()

            s = row[colnum-1].decode(encoding='UTF-8',errors='ignore')
            t = row[colnum].decode(encoding='UTF-8',errors='ignore')

            source = getNameID(s)
            target = getNameID(t)

            attrib["source"] = source
            attrib["target"] = target
            attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] = type

            insertRel(tag, folder, tree, attrib)

            colnum += 1

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

def logNode(n):

    attributes = n.attrib

    if attributes.get(ARCHI_TYPE) == "archimate:BusinessFunction":
        if attributes.get("id") != None:
            dictName[n.get("name")] = attributes["id"]

            logger.debug("logNode : %s:%s:%s:%s" % (n.tag, n.get("name"), n.get("id"), attributes.get(ARCHI_TYPE)))

    for y in n:
        logNode(y)

def logAll(tree):
    for x in tree.getroot():
        logNode(x)

def outputXML(tree, filename="import_artifacts.archimate"):
    output = StringIO.StringIO()
    tree.write(output, pretty_print=True)

    logger.debug("%s" % (output.getvalue()))

    logger.info("Saved to : %s" % filename)

    f = open(filename,'w')
    f.write(output.getvalue())
    f.close()

    output.close()

if __name__ == "__main__":
    # Archimate
    fileArchimate = "/Users/morrj140/PycharmProjects/ArchiConcepts/CodeGen_v5.archimate"
    etree.QName(ARCHIMATE_NS, 'model')
    tree = etree.parse(fileArchimate)

    logAll(tree)

    fileMetaEntity = "/Users/morrj140/PycharmProjects/ArchiConcepts/Workbook4.csv"
    insertScenarios(tree, fileMetaEntity)

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