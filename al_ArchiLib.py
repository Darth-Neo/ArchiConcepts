#!/usr/bin/python
#
# Archimate to Concepts
#
__author__ = 'morrj140'

import sys
import os
import StringIO
import csv
import random
import time

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

NS_MAP={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}
XML_NS         =  NS_MAP["xsi"]
ARCHIMATE_NS   =  NS_MAP["archimate"]
ARCHI_TYPE = "{%s}type" % NS_MAP["xsi"]

class ArchiLib(object):
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v16.archimate"

    #fileExport="export" + time.strftime("%Y%d%m_%H%M%S") +".csv"
    fileExport="export.csv"

    #dictRelation = dict()
    #dictAttrib = dict()

    dictName = dict()
    dictEdges = dict()
    dictNodes = dict()
    dictCount = dict()
    dictBP    = dict()

    relations = ("archimate:TriggeringRelationship",
                    "archimate:UsedByRelationship",
                    "archimate:AccessRelationship",
                    "archimate:FlowRelationship",
                    "archimate:AssignmentRelationship",
                    "archimate:AssociationRelationship",
                    'archimate:RealisationRelationship')

    entities = ("archimate:BusinessEvent",
                "archimate:BusinessObject",
                "archimate:BusinessProcess",
                "archimate:ApplicationService",
                "archimate:ApplicationComponent",
                "archimate:DataObject",
                "archimate:Requirement",
                "archimate:Stakeholder")

    def __init__(self, fileArchimate=None, fileExport=None):

        if fileArchimate != None:
            self.fileArchimate = fileArchimate

        if fileExport != None:
            self.fileExport = fileExport

        etree.QName(ARCHIMATE_NS, 'model')

        self.tree = etree.parse(self.fileArchimate)

        # Populate Dictionaries for easier code
        self.parseAll()

    def outputXMLtoFile(self, filename="import_artifacts.archimate"):#
        output = StringIO.StringIO()
        self.tree.write(output, pretty_print=True)

        logger.debug("%s" % (output.getvalue()))

        logger.info("Saved to : %s" % filename)

        f = open(filename,'w')
        f.write(output.getvalue())
        f.close()

        output.close()

    def outputCSVtoFile(self, concepts, fileExport=None):

        if fileExport != None:
            self.fileExport = fileExport

        listOutput = concepts.listCSVConcepts()

        colDict = dict()

        f = open(self.fileExport,'w')

        m = 0
        for x in listOutput:
            m += 1
            n = 0
            strLine = ""
            logger.debug("listOutput[%d] = %s" % (n, x))

            for y in x.split(","):
                n += 1

                logger.debug("y : %s[%d]" % (y, len(y)))

                if len(y) == 0:
                    if colDict.has_key(n):
                        y = colDict[n]
                else:
                    colDict[n] = y

                strLine = "%s%s," % (strLine, y)

            nl = strLine[:-1]

            logger.debug("%s" % nl)
            f.write(nl + "\n")

        f.close()
        logger.info("Save Model : %s" % self.fileExport)

    def outputXMLtoLog(self):
        output = StringIO.StringIO()
        self.tree.write(output, pretty_print=True)
        logger.info("%s" % (output.getvalue()))

    #
    # Model transversal functions via XPath
    #
    def findDiagramModelByName(self, name):
        r = None

        xp = "//element[@name='" + name + "']"
        stp = self.tree.xpath(xp)

        if stp[0].get(ARCHI_TYPE) == "archimate:ArchimateDiagramModel":
            r = stp[0]

        return r

    def findRelationsByID(self, id, Target=False):
        if Target == False:
            xp = "//element[@source='%s']" % (id)
        else:
            xp = "//element[@source='%s' or @target='%s']" % (id, id)
        logger.debug("%s" % xp)
        stp = self.tree.xpath(xp)
        return stp

    def findRelationsByTargetID(self, id):
        xp = "//element[@target='%s']" % id
        stp = self.tree.xpath(xp)
        return stp

    def findDiagramModel(self, id):
        xp = "//element[@id='" + id + "']"
        stp = self.tree.xpath(xp)
        return stp

    def findDiagramObject(self, id):
        xp = "//child[@id='%s']" % id
        stp = self.tree.xpath(xp)
        return stp

    def findElement(self, name):
        xp = "//element[@name='%s']" % name.rstrip(" ").lstrip(" ")
        stp = self.tree.xpath(xp)
        return stp

    def findElementByID(self, id):
        xp = "//element[@id='%s']" % id
        stp = self.tree.xpath(xp)
        return stp

    def recurseElement(self, e, concepts, n=0):

        n += 1

        try:
            attributes = e.attrib
        except:
            logger.warn("Ops...")
            return concepts

        logger.debug("recurseElement %s: %s:%s:%s:%s" % (n, e.tag, e.get("name"), e.get("id"), attributes.get(ARCHI_TYPE)))

        if attributes.get("id") != None:
            id = attributes["id"]
            name = e.get("name")
            type = e.get(ARCHI_TYPE)[10:]

            d = concepts.addConceptKeyType(name, type)

            next = self.findRelationsByID(id)

            for x in next:
                nid = x.get("target")
                en = self.findElementByID(id)
                self.recurseElement(en, d, n)

        return concepts


    def recurseChildren(self, concepts, x, n=0):
        n += 1

        xid = x.get("id")
        xi = x.items()
        xc, xname = self.getElementName(x.get("archimateElement"))

        ce = self.tree.xpath("//child[@id='%s']" % (xid))
        nc  = ce[0].getchildren()

        #
        # Add source into concepts
        #
        #c = concepts.addConceptKeyType(ModelToExport + ":" + xname, x.get(ARCHI_TYPE)[10:])

        #
        # for each RelationShip, find the Source and Target
        #
        for y in nc:
            if y.tag == "child":
                logger.debug("%d.%s" % (n, y.tag))
                yc, yname = self.getElementName(y.get("archimateElement"))
                d = concepts.addConceptKeyType(yname, yc.get(ARCHI_TYPE)[10:])
                self.recurseChildren(d, y)

            if y.tag == "sourceConnection":
                logger.debug("skip - %s" % y.tag)

                yid = y.get("id")
                yi = y.items()

                sid = y.get("source")
                s, sname = self.getChildName(sid)

                tid = y.get("target")
                t, tname = self.getChildName(tid)

                relid = y.get("relationship")
                rel, rname = self.getElementName(relid)

                if rname == None:
                    rname = "Target"

                d = concepts.addConceptKeyType(rname, rel.get(ARCHI_TYPE)[10:])
                e = d.addConceptKeyType(tname, t.get(ARCHI_TYPE)[10:])

                logger.debug("    %s" % yi)
                logger.debug("%s,%s,%s,%s,%s,%s\n" % (sname, s.get(ARCHI_TYPE), rel.get(ARCHI_TYPE), rname, tname, t.get(ARCHI_TYPE)))

            #recurseElement(t, e, tree)

    def recurseModel(self, ModelToExport, concepts):
        #
        # Find DiagramModel Element to Export
        #
        xp = "//element[@name='%s']" % (ModelToExport)
        logger.debug("XP : %s" % xp)

        se = self.tree.xpath(xp)

        nse = len(se)
        logger.debug("num se : %d" % nse)
        #
        # Iterate over the DiagramModel's DiagramObjects children
        #
        for m in se:
            if m.get(ARCHI_TYPE) == "archimate:ArchimateDiagramModel":
                logger.debug("%s:%s:%s" % (m.get("name"), m.get(ARCHI_TYPE), m.tag))

                r = m.getchildren()

                c = concepts.addConceptKeyType(m.get("name"), m.get(ARCHI_TYPE)[10:])

                #
                # for each DiagramObject, Find the ArchimateElement
                #
                for x in r:

                    if x.get(ARCHI_TYPE) != "archimate:DiagramObject":
                        continue

                    xid = x.get("id")

                    xc, xname = self.getElementName(x.get("archimateElement"))

                    logger.info("  %s[%s]" % (xname, x.get(ARCHI_TYPE)))

                    d = c.addConceptKeyType(xname, xc.get(ARCHI_TYPE)[10:])

                    self.recurseChildren(d, x)

        return concepts

    #
    # Model functions via dictionaries
    #
    def logTypeCounts(self, ListOnly = False):
        if not ListOnly:
            logger.info("Type Counts")

        listCounts = self.dictCount.items()

        if not ListOnly:
            for x in sorted(listCounts, key=lambda c: abs(c[1]), reverse=False):
                if x[1] > 1:
                    logger.info("  %d - %s" % (x[1], x[0]))

            logger.info(" ")

        return listCounts

    def countNodeType(self, type):
        if self.dictCount.has_key(type):
            self.dictCount[type] += 1
        else:
            self.dictCount[type] = 1

    def parseAll(self):
        for x in self.tree.getroot():
            logger.info("Folder : %s" % x.get("name"))
            self.getElementsFromFolder(x.get("name"))

    def getElementsFromFolder(self, folder):

        se = self.tree.xpath("folder[@name='%s']" % (folder))

        if folder == "Views":
            return

        if folder == "Relations":
            for x in se:
                self.getNode(x, self.dictEdges)
        else:
            for x in se:
                self.getNode(x, self.dictNodes)

    def getNode(self, el, d):
        logger.debug("el.tag = %s" % (el.tag))

        attributes = el.attrib

        # Not every node will have a type
        if el.tag in ("element", "child"):
            self.countNodeType(attributes[ARCHI_TYPE])

        nl = dict()
        for atr in attributes:
            nl[atr] = attributes[atr]
            logger.debug("%s = %s" % (atr, attributes[atr]))

        if nl.has_key("id"):
            d[nl["id"]] = nl
            self.dictName[el.get("name")] = el.get("id")

        for elm in el:
            self.getNode(elm, d)

    def getTypeNodes(self, type):
        d = dict()

        for x in self.dictNodes.values():
            if x.get(ARCHI_TYPE) in type:
                d[x.get("name")] = x
        return d

    def getNodeName(self, node):
        name = " "

        try:
            logger.debug("  Node : %s" % (self.dictNodes[node]["name"]))
            name = self.dictNodes[node]["name"]
        except:
            logger.debug("Node not Found")

        return name

    def getEdgesForNode(self, source, searchType, n=5, m=0):
        listNodes = list()

        if n == 0:
            return listNodes
        else:
            n -= 1

        m += 1

        xp = "//element[@source='%s']" % source
        stp = self.tree.xpath(xp)

        for x in stp:
            logger.debug("Index %d:%d Depth" % (m, n))

            sourceNE = x.get("source")
            targetNE = x.get("target")

            dns = x.get(ARCHI_TYPE)

            if  dns in searchType:
                spaces = " " * n
                nodeName = self.getNodeName(targetNE)
                if nodeName != "NA":
                    nn = "%s%s" % (spaces, nodeName)
                    listNodes.append(nn)

                    ln = self.getEdgesForNode(targetNE, searchType, n, m)
                    for y in ln:
                        listNodes.append(y)

        return listNodes


    def getModelsInFolder(self, folder):
        xp = "//folder[@name='%s']" % (folder)

        se = self.tree.xpath(xp)

        modelList = se[0].getchildren()

        models = list()

        for x in modelList:
            modelName = str(x.get("name"))
            models.append(modelName)

        return models

    def getFolders(self):
        se = self.tree.xpath('folder')

        l = list()

        for x in se:
            l.append(x.get("name"))
            logger.debug("%s" % (x.get("name")))

        return l

    def getChildName(self, id):

        xp = "//child[@id='%s']" % str(id)

        logger.debug("xp : %s" % xp)

        se = self.tree.xpath(xp)

        if len(se) > 0:
            ae = se[0].get("archimateElement")
            return self.getElementName(ae)

    def getElementName(self, id):

        xp = "//element[@id='%s']" % str(id)

        logger.debug("xp : %s" % xp)

        se = self.tree.xpath(xp)

        if len(se) > 0:
            element = se[0]
            name = se[0].get("name")
            if name == None:
                name = element.get(ARCHI_TYPE)[10:]

            logger.debug("getElementName - %s:%s" % (element.get(ARCHI_TYPE), name))
            return element, name
        else:
            return None, None

    def getNameID(self, value):
        logger.info("    Search for : %s" % value)
        if self.dictName.has_key(value):
            idd = self.dictName[value]
            logger.debug("    Found! : %s" % idd)
        else:
            idd =  self._getID()
            self.dictName[value] = idd
            logger.debug(    "New I  : %s" % idd)

        logger.debug("%s" % self.dictName)

        return idd


    def insertNode(self, tag, folder, attrib):
        idd = None

        try:
            logger.debug("attrib: %s" % (attrib))

            value = attrib["name"].rstrip(" ").lstrip(" ")

            if value != attrib["name"]:
                logger.debug("diff value .%s:%s." % (value, attrib["name"]))

            if self.dictName.has_key(value):
                idd = self.dictName[value]
                attrib["id"] = idd

                logger.debug("inFound! : %s" % idd)
            else:
                idd =  self._getID()
                self.dictName[value] = idd
                attrib["id"] = idd

                xp = "//folder[@name='" + folder + "']"
                elm = etree.Element(tag, attrib, nsmap=NS_MAP)

                txp = self.tree.xpath(xp)
                txp[0].insert(0, elm)
                logger.debug("inNew!   : %s" % idd)
        except:
            logger.warn("attrib: %s" % (attrib))

        return idd

    def insertRel(self, tag, folder, attrib):

        logger.debug("attrib: %s" % (attrib))

        value = "%s--%s" % (attrib["source"], attrib["target"])

        if self.dictName.has_key(value):
            idd = self.dictName[value]
            attrib["id"] = idd

            logger.debug("inFound! : %s" % idd)
        else:
            idd =  self._getID()
            self.dictName[value] = idd
            attrib["id"] = idd

            xp = "//folder[@name='" + folder + "']"
            elm = etree.Element(tag, attrib, nsmap=NS_MAP)
            self.tree.xpath(xp)[0].insert(0, elm)
            logger.debug("inNew!   : %s" % idd)

        return idd

    def insertTwoColumns(self, folder, subfolder, fileMetaEntity, eType):

        #<element xsi:type="archimate:Node" id="612a9b73" name="Linux Server"/>

        file = open(fileMetaEntity, "rU")
        reader = csv.reader(file)

        xp = "folder[@name='" + folder + "']"
        tag = "element"

        # <folder name="Process" id="e23b1e50">

        attrib = dict()
        attrib["id"] = self._getID()
        attrib["name"] = subfolder
        self.insertNode("folder", folder, attrib)

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
            self.insertNode(tag, folder, attrib)
            CM1_ID = attrib["id"]

            C2 = CM2
            attrib = dict()
            attrib["name"] = CM2
            attrib[ARCHI_TYPE] = eType
            self.insertNode(tag, folder, attrib)
            CM2_ID = attrib["id"]

            attrib = dict()
            attrib["source"] = CM1_ID
            attrib["target"] = CM2_ID
            attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
            self.insertRel(tag, "Relations", attrib)

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
                self.insertNode(tag, folder, attrib)
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
                self.insertNode(tag, folder, attrib)
                listC2.append(attrib["id"])

            if len(listC1) > 1:
                pl = listC1[0]
                for y in listC1[1:]:
                    attrib = dict()
                    attrib["source"] = pl
                    attrib["target"] = y
                    attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                    self.insertRel(tag, "Relations", attrib)
                    pl = y

            if len(listC2) > 1:
                pl = listC2[0]
                for y in listC2[1:]:
                    attrib = dict()
                    attrib["source"] = pl
                    attrib["target"] = y
                    attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                    self.insertRel(tag, "Relations", attrib)
                    pl = y

            attrib = dict()
            attrib["source"] = listC1[0]
            attrib["target"] = listC2[0]
            attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
            self.insertRel(tag, "Relations", attrib)

            attrib = dict()
            attrib["source"] = CM1_ID
            attrib["target"] = listC1[0]
            attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
            self.insertRel(tag, "Relations", attrib)

            attrib = dict()
            attrib["source"] = CM2_ID
            attrib["target"] = listC2[0]
            attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
            self.insertRel(tag, "Relations", attrib)

    def insertNColumns(self, folder, subfolder, fileMetaEntity):

        #<element xsi:type="archimate:Node" id="612a9b73" name="Linux Server"/>

        file = open(fileMetaEntity, "rU")
        reader = csv.reader(file)

        xp = "folder[@name='" + folder + "']"
        tag = "element"

        # <folder name="Process" id="e23b1e50">

        attrib = dict()
        attrib["id"] = self._getID()
        attrib["name"] = subfolder
        self.insertNode("folder", folder, attrib)

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

            logger.info("----------------------------------------------------------------------------------------")
            logger.debug("rownum : %d" % rownum)
            logger.debug("row    : %s" % row)

            p = None
            colnum = 0

            for col in row:
                logger.debug("    %d   [%s] %s" % (colnum, listColumnHeaders[colnum], col))

                CM = self._cleanString(col.decode(encoding='ASCII',errors='ignore').lstrip())

                if CM == "" or CM == None:
                    logger.info("Using %d[%s]" % (colnum, previous[colnum]))
                    CM = previous[colnum]
                else:
                    previous[colnum] = CM
                    logger.info("CM  %d[%s]" % (colnum, CM))

                attrib = dict()
                attrib["name"] = CM
                attrib[ARCHI_TYPE] = listColumnHeaders[colnum]
                self.insertNode(tag, folder, attrib)
                CM_ID = attrib["id"]

                if p != None:
                    attrib = dict()
                    attrib["source"] = CM_ID
                    attrib["target"] = p
                    attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                    self.insertRel(tag, "Relations", attrib)

                    p = CM_ID
                else:
                    p = CM_ID

                colnum += 1

    def insertScenarios(self, fileMetaEntity):

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
                self.insertNode("element", "Business", attrib)
                scenarioID = attrib["id"]

                attrib = dict()
                attrib["name"] = site
                attrib[ARCHI_TYPE] = "archimate:BusinessFunction"
                self.insertNode("element", "Business", attrib)
                siteID = attrib["id"]

                attrib = dict()
                attrib["source"] = siteID
                attrib["target"] = scenarioID
                attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                self.insertRel("element", "Relations", attrib)

            elif row[0] == "Sub":
                subscenario = row[5].decode(encoding='UTF-8',errors='ignore')
                site = row[1].decode(encoding='UTF-8',errors='ignore')

                attrib = dict()
                attrib["name"] = subscenario.decode(encoding='UTF-8',errors='ignore')
                attrib[ARCHI_TYPE] = "archimate:BusinessProcess"
                self.insertNode("element", "Business", attrib)
                subscenarioID = attrib["id"]

                attrib = dict()
                attrib["source"] = scenarioID
                attrib["target"] = subscenarioID
                attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                self.insertRel("element", "Relations", attrib)

                attrib = dict()
                attrib["source"] = siteID
                attrib["target"] = subscenarioID
                attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                self.insertRel("element", "Relations", attrib)

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
                    self.insertNode("element", "Motivation", attrib)
                    requirementID = attrib["id"]

                    attrib = dict()
                    attrib["name"] = entity
                    attrib[ARCHI_TYPE] = "archimate:BusinessObject"
                    self.insertNode("element", "Business", attrib)
                    entityID = attrib["id"]

                    attrib = dict()
                    attrib["name"] = segment
                    attrib[ARCHI_TYPE] = "archimate:BusinessFunction"
                    self.insertNode("element", "Business", attrib)
                    segmentID = attrib["id"]

                    attrib = dict()
                    attrib["name"] = category
                    attrib[ARCHI_TYPE] = "archimate:BusinessFunction"
                    self.insertNode("element", "Business", attrib)
                    categoryID = attrib["id"]

                    attrib = dict()
                    attrib["name"] = subcategory
                    attrib[ARCHI_TYPE] = "archimate:BusinessFunction"
                    self.insertNode("element", "Business", attrib)
                    subcategoryID = attrib["id"]

                    attrib = dict()
                    attrib["source"] = entityID
                    attrib["target"] = requirementID
                    attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                    self.insertRel("element", "Relations", attrib)


                    attrib = dict()
                    attrib["source"] = categoryID
                    attrib["target"] = subcategoryID
                    attrib[ARCHI_TYPE] = "archimate:CompositionRelationship"
                    self.insertRel("element", "Relations", attrib)

                    attrib = dict()
                    attrib["source"] = scenarioID
                    attrib["target"] = requirementID
                    attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                    self.insertRel("element", "Relations", attrib)

                    attrib = dict()
                    attrib["source"] = subcategoryID
                    attrib["target"] = requirementID
                    attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                    self.insertRel("element", "Relations", attrib)

                    attrib = dict()
                    #attrib["id"] = getID()
                    attrib["source"] = segmentID
                    attrib["target"] = requirementID
                    attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                    self.insertRel("element", "Relations", attrib)
                except:
                    logger.warn("ops...%s" % row)
            else:
                logger.info("Unknown line - %s" % row)
                pass

            rownum += 1

    def insertConcepts(self, tree, concepts, n=0):

        for x in concepts.getConcepts().values():
            logger.info("x : %s" % x.name)
            for y in x.getConcepts().values():
                logger.info("  y : %s" % y.name)
                attrib = dict()
                attrib["name"] = x.name
                attrib[ARCHI_TYPE] = "archimate:WorkPackage"
                self.insertNode("element", "Implementation & Migration", attrib)
                wp1 = attrib["id"]

                attrib = dict()
                attrib["name"] = y.name
                attrib[ARCHI_TYPE] = "archimate:BusinessProcess"
                self.insertNode("element", "Process", attrib)
                wp2 = attrib["id"]

                attrib = dict()
                attrib["source"] = wp1
                attrib["target"] = wp2
                attrib[ARCHI_TYPE] = "archimate:AssociationRelationship"
                self.insertRel("element", "Relations", attrib)


    #
    # These functions interact with nl_lib
    #

    def folderConcepts(self, concepts):
        r = self.tree.xpath('folder')

        for x in r:

            folder = str(x.get("name")).strip()

            logger.debug("folder : %s" % (folder))

            se = self.tree.xpath("folder[@name='%s']" % (folder))

            for element in se:
                self.createConcepts(concepts, element)

        #concepts.logConcepts()

    def conceptAttributes(self, c, el, n):
        n = n + 1
        spaces = " " * n

        attrib = el.attrib

        d = c.addConceptKeyType("Attributes", "Attribute")

        attributes = el.attrib
        for atr in attributes.keys():
            logger.info("%sAttributes[%s]=%s" % (spaces, atr, attributes[atr] ))
            d.addConceptKeyType(atr, attributes[atr])

        if el.tag == 'Documentation':
            d.addConceptKeyType(el.text, "Text")

    def createConcepts(self, concept, el, i=10, n=1):
        if i == 0:
            return

        spaces = " " * n
        i = i - 1

        id = el.get("id")
        tag = el.tag

        if id != None:
            c = concept.addConceptKeyType(id, tag)
        else:
            c = concept.addConceptKeyType(tag, tag)

        logger.info("%s%s[%s]" % (spaces, c.name, c.typeName))

        self.conceptAttributes(c, el, n+1)

        for elm in el:
            self.createConcepts(c, elm, i, n+1)

    def createArchimate(self, fileArchiModel, fileArchiP):
        archi = Concepts.loadConcepts(fileArchiP)

        rootName = etree.QName(ARCHIMATE_NS, 'model')
        root = etree.Element(rootName, version="2.6.0", name=fileArchiP ,id="02cec69f", nsmap=NS_MAP)
        xmlSheet = etree.ElementTree(root)

        self.createArchimateElements(xmlSheet, archi, root)

        output = StringIO.StringIO()
        xmlSheet.write(output, pretty_print=True)

        logger.info("%s" % (output.getvalue()))

        f = open(fileArchiModel,'w')
        f.write(output.getvalue())
        f.close()

        output.close()

    def createArchimateElements(self, xmlSheet, archi, root, n=1):

        spaces = " " * n

        cd = archi.getConcepts().values()

        for x in cd:
            logger.debug("%s%s:%s" % (spaces, x.typeName, x.name))

            if x.typeName != "Attribute":

                tag = x.typeName
                id = x.name
                attrib = x.getConcepts()["Attributes"]

                ad = dict()
                for y in attrib.getConcepts().values():
                    for z in attrib.getConcepts().values():
                        ad[z.name]  = z.typeName

                element = etree.SubElement(root, tag, ad)

                self.createArchimateElements(xmlSheet, x, element)

    #
    # Utility Functions
    #

    def _getID(self):
        r = str(hex(random.randint(0, 16777215)))[-6:] + str(hex(random.randint(0, 16777215))[-2:])

        if r[0] == "x":
            return self.getID()
        return r

    def _cleanString(self, s):
        r = ""
        if s == None:
            return r

        for x in s.lstrip(" "):
            if x.isalnum() or x in (" ", "-", "."):
                r = r + x
        return r.lstrip(" ").rstrip(" ")

    def _cleanCapital(self, s):
        r = ""

        if s == None:
            return None

        v = s.replace(":"," ")
        v = v.replace("|"," ")
        v = v.replace(" "," ")
        v = v.replace("_"," ")
        v = v.replace("-"," ")
        v = v.replace("/"," ")

        n = 0
        for x in v:
            if x == x.upper() and n != 0:
                r = r + " " + x
            else:
                r =r + x

            n += 1

        logger.debug("cleanCapital : %s" % r)
        return r

    def _checkDuplicate(self, dmID, x):
        xp = "//element[@id='" + dmID + "']"
        dm = self.tree.xpath(xp)[0]

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
    #
    # Generic print of info
    #
    def print_xml(self, el, i=3, n=0):
        if i==0:
            return

        spaces = " " * n
        n = n + 1

        #print("%se.%d.%s - %s" % (spaces, i, el.tag, el.text))
        print("%se.%d.%s" % (spaces, i, el.tag))

        spaces = " " * n
        n = n + 1

        #nm = el.nsmap
        #for n in nm:
        #    print("--%s = %s" % (n, nm[n]))

        attributes = el.attrib
        for atr in attributes:
            print("%sa.%d.%s = %s" % (spaces, i, atr, attributes[atr]))

        i = i - 1
        for elm in el:
            self.print_xml(elm, i, n)

    def print_folders(self):
        r = self.tree.xpath('folder')

        for x in r:
            print("%s" % (x.get("name")))

    def print_folder(self, folder):

        se = self.tree.xpath("folder[@name='%s']" % (folder))

        for x in se:
            self.print_xml(x, i=6)

    def print_elements(self):
        r = self.tree.getroot()

        r = self.tree.xpath('folder/element')

        for x in r:
            print x.get("name")

    def print_id(self, id):
        a = "id"
        p = "//child[@%s=\"%s\"]" % (a, id)
        r = self.tree.xpath("//@id=\"%s\"" % id, namespaces=NS_MAP)

        try:
            self.print_xml(r[0], i=1)
        except:
            print("Fail - %s" % p)

    def print_types(self, a):

        dictTypes = dict()

        r = self.tree.xpath("//@%s" % a, namespaces=NS_MAP)

        for x in r:
            if dictTypes.has_key(x):
                dictTypes[x] += 1
            else:
                dictTypes[x] = 1

        for x in dictTypes:
            logger.info("Parent - %s:ID - %s" % (x.getparent().get("name"),x.getparent().get("id")))

            p = "//element[@%s=\"%s\"]" % (a, x)
            r = self.tree.xpath(p, namespaces=NS_MAP)

            if len(r) > 0:
                self.print_xml(r[0], i=1)

    def addToNodeDict(self, type, d):
        if d.has_key(type):
            d[type] += 1
        else:
            d[type] = 1