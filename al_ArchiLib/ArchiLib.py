#!/usr/bin/python
#
# Archimate Libray
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import csv
import random
import time

from Logger import *

logger = setupLogging(__name__)
logger.setLevel(INFO)

from nl_lib.Concepts import Concepts

from lxml import etree

from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter

from Constants import *

import pytest

#
# Main class to make life easier
#
class ArchiLib(object):
    dictName  = dict()
    dictEdges = dict()
    dictNodes = dict()
    dictBP    = dict()
    dictCount = dict()

    def __init__(self, fileArchimate):

        if fileArchimate != None:
            self.fileArchimate = fileArchimate
        else:
            self.fileArchimate = fileArchimate

        etree.QName(ARCHIMATE_NS, 'model')

        self.tree = etree.parse(self.fileArchimate)

        # Populate Dictionaries for easier code
        self.parseAll()

    def outputXMLtoFile(self, filename="import_artifacts.archimate"):
        output = StringIO.StringIO()
        self.tree.write(output, pretty_print=True)

        logger.debug("%s" % (output.getvalue()))

        logger.info("====> Saved to : %s" % filename)

        f = open(filename,'w')
        f.write(output.getvalue())
        f.close()

        output.close()

    def outputCSVtoFile(self, concepts, fileExport):

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

    def exportExcel(fileIn, fileOut, workSheetTitle="Scope Items"):

        wb = load_workbook(filename = fileIn)

        ws = wb.create_sheet()

        ws.title = workSheetTitle

        ws['F5'] = 3.14

        for col_idx in range(1, 40):
            col = get_column_letter(col_idx)
            for row in range(1, 600):
                ws.cell('%s%s'%(col, row)).value = '%s%s' % (col, row)

        wb.save(filename = fileOut)


    #
    # Model transversal functions via XPath
    #
    def findDiagramModelByName(self, name):
        r = None

        xp = "//element[@name='" + name + "']"
        stp = self.tree.xpath(xp)

        if stp[0].get(ARCHI_TYPE) == DIAGRAM_MODEL:
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

    def findDiagramModelByName(self, name):
        xp = "//element[@name='%s']" % (name)
        logger.debug("xp : %s" % xp)
        stp = self.tree.xpath(xp)

        for x in stp:
            if x.get(ARCHI_TYPE) == DIAGRAM_MODEL:
                stp = x
                break

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

        if stp == None:
            stp = list()
            stp.append(" ")

        return stp

    def getDiagramModels(self):
        xp = "//element[@%s='%s']" % (ARCHI_TYPE, DIAGRAM_MODEL)
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
            if m.get(ARCHI_TYPE) == DIAGRAM_MODEL:
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
            for x in sorted(listCounts, key=lambda c: abs(c[1]), reverse=True):
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
            logger.debug("Folder : %s" % x.get("name"))
            self.getElementsFromFolder(x.get("name"))

    def getElementsFromFolder(self, folder):

        se = self.tree.xpath("folder[@name='%s']" % (folder))

        if folder == "Views":
            return se[0]

        if folder == "Relations":
            for x in se:
                self.getNode(x, self.dictEdges)
        else:
            for x in se:
                self.getNode(x, self.dictNodes)

        return se

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
            xt = x.get(ARCHI_TYPE)
            if xt in type:
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
        se = self.tree.xpath('//folder')

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

    #
    # Model functions via dictionaries
    #
    def logTypeCounts(self):
        listCounts = list()

        logger.info("Type Counts")
        listCounts = self.dictCount.items()

        for x in sorted(listCounts, key=lambda c: abs(c[1]), reverse=True):
            if x[1] > 1:
                logger.info(" %d - %s" % (x[1], x[0]))
        logger.info(" ")

        return listCounts

    #
    # Node - <element xsi:type="archimate:Node" id="612a9b73" name="Linux Server"/>
    #
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

                elm = etree.Element(tag, attrib, nsmap=NS_MAP)

                xp = "//folder[@name='" + folder + "']"
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

    # Properties
    # <element xsi:type="archimate:BusinessProcess" id="0ad0bac9" name="06.0 Activity Reports">
    #        <property key="ExampleName" value="ExampleValue"/>
    # </element>
    def addProperties(self, properties):

        # To Do - stop duplicating properties

        idd = properties["ID"]
        node = self.findElementByID(idd)

        n = 0
        for key, value in properties.items():
            if key != "ID"and node.get(key) == None:
                prop = dict()
                prop["key"] = key
                prop["value"] = value
                elm = etree.Element("property", prop, nsmap=NS_MAP)
                node[0].insert(n, elm)
                n += 1

    def insertNColumns(self, folder, subfolder, fileMetaEntity):

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

        properties = dict()

        PROPERTIES_FLAG = False

        for row in reader:

            if rownum == 0:
                rownum += 1
                for col in row:
                    if col[:8] == "Property":
                        colType = col
                        listColumnHeaders.append(colType)
                    else:
                        colType = "archimate:%s" % col
                        listColumnHeaders.append(colType)
                continue

            logger.info("----------------------------------------------------------------------------------------")
            logger.debug("rownum : %d" % rownum)
            logger.debug("row    : %s" % row)

            p = None
            colnum = 0

            for col in row:
                logger.info("    %d   [%s] %s" % (colnum, listColumnHeaders[colnum], col))

                CM = self._cleanString(col.decode(encoding='ASCII',errors='ignore').lstrip())

                if listColumnHeaders[colnum][:8] == "Property":
                    logger.debug("Properties : %s - %s" % (listColumnHeaders[colnum][9:], CM))

                    if not properties.has_key("ID"):
                        properties["ID"] = p

                    properties[listColumnHeaders[colnum][9:]] = CM

                    colnum += 1
                    continue

                if len(properties) > 0:
                    logger.debug("Add %d Properties" % (len(properties)))
                    self.addProperties(properties)
                    properties = dict()

                #
                # This is for a cvs which assumes value in column
                # from a previous column
                #
                if CM == "" or CM == None:
                    logger.debug("Using %d[%s]" % (colnum, previous[colnum]))
                    CM = previous[colnum]
                else:
                    previous[colnum] = CM
                    logger.debug("CM  %d[%s]" % (colnum, CM))

                #
                # Create the attributes
                #
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

        if len(properties) > 0:
            logger.info("Add %d Properties" % (len(properties)))
            self.addProperties(properties)
            properties = dict()


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

    def _getID(self):
        r = str(hex(random.randint(0, 16777215)))[-6:] + str(hex(random.randint(0, 16777215))[-2:])

        if r[0] == "x":
            return self.getID()
        return r

    def getID(self):
        return self._getID()

    def _cleanString(self, s):
        r = ""
        if s == None:
            return r

        for x in s.lstrip(" "):
            if x.isalnum() or x in (" ", "-", "."):
                r = r + x
        return r.lstrip(" ").rstrip(" ")

    def cleanString(self, s):
        return  self._cleanString(s)


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

    def addToNodeDict(self, type, d):
        if d.has_key(type):
            d[type] += 1
        else:
            d[type] = 1

    def cleanConcept(self, concept):
        if concept.typeName[:10] == "archimate:" :
            concept.typeName = concept.typeName[10:]

        concept.name = concept.name.replace("\"", "'")

        return concept

    @staticmethod
    def startTimer():
        # measure process time, wall time
        t0 = time.clock()
        start_time = time.time()
        strStartTime = time.asctime(time.localtime(start_time))
        logger.info("Start time : %s" % strStartTime)

        return start_time

    @staticmethod
    def stopTimer(start_time):
        #measure wall time
        strStartTime = time.asctime(time.localtime(start_time))
        logger.info("Start time : %s" % strStartTime)

        end_time = time.time()

        strEndTime = time.asctime(time.localtime(end_time))
        logger.info("End   time : %s" % strEndTime)

        # measure process time
        timeTaken = end_time - start_time

        minutes = timeTaken / 60
        hours = minutes / 60
        seconds = timeTaken - (minutes * 60.0)
        logger.info("Process Time = %4.2f seconds, %d Minute(s), %d hours" % (timeTaken, minutes, hours))

if __name__ == "__main__":
    fileArchimate = "test" + os.sep + "Testing.archimate"

    al = ArchiLib()

    al.logTypeCounts()