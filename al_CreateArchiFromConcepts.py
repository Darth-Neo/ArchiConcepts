#!/usr/bin/python
#
# Create Archimate XML from Concepts
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib

class CreateArchiFromConcepts(object):

    dictPoints = dict()
    dictDO = dict()

    def __init__(self, filename=None):

        self.al = ArchiLib()

        etree.QName(ARCHIMATE_NS, 'model')

        if filename == None:
            filename = fileArchimate

        self.tree = etree.parse(fileArchimate)

        self.al.parseAll()

    def showConcepts(self, concepts):
        n = 0
        for x in concepts.getConcepts().values():
            n += 1
            logger.info("x %s[%s]" % (x.name, x.typeName))
            for y in x.getConcepts().values():
                logger.info("  y %s[%s]" % (y.name, y.typeName))
                for z in y.getConcepts().values():
                    if not (z.name in ("h", "l", "t", "w")):
                        logger.info("    z  %s[%s]" % (z.name, z.typeName))

    def createDiagramModels(self, concepts):

        # <folder name="Views" id="d18c15b0" type="diagrams">
        attrib = dict()
        attrib["id"] = str(self.al.getID())
        newFolder = "PowerPointApps"
        attrib["name"] = newFolder

        xp = "//folder[@name='Application']"
        elm = etree.Element("folder", attrib, nsmap=NS_MAP)
        self.tree.xpath(xp)[0].insert(0, elm)

        # Make new PowerPoint Folder to import into
        # <folder name="Views" id="d18c15b0" type="diagrams">
        attrib = dict()
        attrib["id"] = str(self.al.getID())
        newFolder = "PowerPoint"
        attrib["name"] = newFolder

        xp = "//folder[@name='Views']"
        elm = etree.Element("folder", attrib, nsmap=NS_MAP)
        self.tree.xpath(xp)[0].insert(0, elm)
        Folder_ID = attrib["id"]

        # <element xsi:type="archimate:ArchimateDiagramModel" id="176899e1" name="Default View">
        for x in concepts.getConcepts().values():
            logger.debug("%s[%s]-%d" % (x.name, x.typeName, len(x.name)))
            if x.typeName == "Slide":
                logger.info("Slide %s[%s]-%d" % (x.name, x.typeName, len(x.name)))

                # Create "archimate:ArchimateDiagramModel"
                attrib = dict()
                attrib["name"] = x.name
                attrib["id"] = str(self.al.getID())
                attrib[ARCHI_TYPE] = "archimate:ArchimateDiagramModel"
                xp = "//folder[@name='PowerPoint']"
                elm = etree.Element("element", attrib, nsmap=NS_MAP)
                txp = self.tree.xpath(xp)
                txp[0].insert(0, elm)
                DM_ID = attrib["id"]

                self.createArchimateComponents(x, DM_ID)

        self.createConnections(concepts)

    def createArchimateComponents(self, concepts, dmID):

        # Creare connection inside the start
        # <child xsi:type="archimate:DiagramObject" id="74386658" textAlignment="2" archimateElement="5789571a">
        #        <bounds x="200" y="96"/>
        #        <sourceConnection xsi:type="archimate:Connection" id="95144175" source="74386658" target="5256ff1f" relationship="2f2f9f96"/>
        # </child>

        listST = list()

        dictACDone = dict()

        for x in concepts.getConcepts().values():
            if not (x.typeName in ("Node")):
                continue

            logger.info("Concept : %s[%s]" % (x.name, x.typeName))

            # Create Coordinates
            coordinates = x.getConcepts()

            if len(coordinates) == 0:
                logger.info("Coordinates == 0")
                continue

            if not(x.name in dictACDone):
                # Create the archimate:ApplicationComponent
                attribAC = dict()
                attribAC["name"] = x.name
                attribAC[ARCHI_TYPE] = "archimate:ApplicationComponent"
                self.al.insertNode("element", "PowerPointApps", self.tree, attribAC)
                acID = attribAC["id"]
                logger.info("  Create acID %s" % (acID))
                dictACDone[x.name] = acID
            else:
                acID = dictACDone[x.name]

            logger.info("  %s[%s]-%d -- %s" % (x.name, x.typeName, len(x.name), acID))

        logger.info("Create Diagram Objects")
        self.createDiagramObjects(concepts, dmID, dictACDone)


    def createDiagramObjects(self, concepts, dmID, dictACDone, dictDODone = None):
        # Creare connection inside the start
        # <child xsi:type="archimate:DiagramObject" id="74386658" textAlignment="2" archimateElement="5789571a">
        #        <bounds x="200" y="96"/>
        #        <sourceConnection xsi:type="archimate:Connection" id="95144175" source="74386658" target="5256ff1f" relationship="2f2f9f96"/>
        # </child>

        listST = list()

        if dictDODone == None:
            dictDODone = dict()

        for x in concepts.getConcepts().values():
            if x.name in ("t", "l", "w", "h") or x.typeName == "Edge":
                continue

            logger.info("Concept : %s[%s]" % (x.name, x.typeName))

            # Create Coordinates
            coordinates = x.getConcepts()

            if len(coordinates) == 0:
                logger.info("Coordinates == 0")
                continue

            acID = dictACDone[x.name]

            logger.info("  %s[%s]-%d -- %s" % (x.name, x.typeName, len(x.name), acID))

            # Create "archimate:DiagramObject"
            if not(x.name in dictDODone):
                attribDO = dict()
                attribDO["name"] = x.name
                attribDO["id"] = str(self.al.getID())
                attribDO["textAlignment"] = "2"
                attribDO["archimateElement"] = acID
                attribDO[ARCHI_TYPE] = "archimate:DiagramObject"

                elm = etree.Element("child", attribDO, nsmap=NS_MAP)
                doID = attribDO["id"]

                xp = "//element[@id='" + dmID + "']"
                self.tree.xpath(xp)[0].insert(0, elm)

                logger.debug("doID %s" % (doID))

                l = float(coordinates["l"].typeName)
                t = float(coordinates["t"].typeName)
                w = float(coordinates["w"].typeName)
                h = float(coordinates["h"].typeName)

                cx = int(l * 100)
                cy = int(t * 100) - 150

                key = "%s%s" % (cx,cy)
                if self.dictPoints.has_key(key):
                    cx = 100 + cx
                    cy = 100 + cy
                else:
                    self.dictPoints[key] = key

                attrib = dict()
                attrib["x"] = str(cx)
                attrib["y"] = str(cy)
                elm = etree.Element("bounds", attrib, nsmap=NS_MAP)
                xp = "//child[@id='" + doID + "']"
                self.tree.xpath(xp)[0].insert(0, elm)

                dictDODone[x.name] = doID

            self.createDiagramObjects(x, dmID, dictACDone, dictDODone)

    def createConnections(self, concepts):

        listST = list()
        logger.info("----Children----")

        # find children
        for tc in concepts.getConcepts().values():
            if len(tc.name) > 1:
                logger.debug(" Slide %s[%s]-%d" % (tc.name, tc.typeName, len(tc.name)))

                for tcc in tc.getConcepts().values():
                    logger.debug("  Source %s[%s]-%d" % (tcc.name, tcc.typeName, len(tcc.name)))

                    for tce in tcc.getConcepts().values():
                        logger.debug("   Target %s[%s]-%d" % (tce.name, tce.typeName, len(tce.name)))

                        for tcee in tce.getConcepts().values():
                            tcee.name = self.al.cleanString(tcee.name)
                            if tcee.typeName in ("Edge"):
                                logger.debug("  Source %s[%s]-%d" % (tcc.name, tcc.typeName, len(tcc.name)))
                                logger.debug("   Target %s[%s]-%d" % (tce.name, tce.typeName, len(tce.name)))
                                logger.debug("    Edge %s[%s]-%d" % (tcee.name, tcee.typeName, len(tcee.name)))
                                ll = (tc, tcc, tce, tcee)
                                listST.append(ll)

        dictRel = dict()

        for x in listST:

            try:
                sourceName = x[1].name.rstrip(" ")
                targetName = x[2].name.rstrip(" ")
                slideName = x[0].name.rstrip(" ")
                edgeName   = x[3].name.rstrip(" ")

                logger.info("%s:%s>%s->%s" % (slideName, sourceName, edgeName, targetName, ))

                src = self.al.findElement(self.tree, sourceName)
                if src != None:
                    source = src[0].get("id")
                else:
                    logger.warn("***No Source***")
                    source = " "

                tgt = self.al.findElement(self.tree, targetName)
                if tgt != None:
                    target = tgt[0].get("id")
                else:
                    logger.warn("***No Target***")
                    target = " "
            except:
                continue

            if x[1].typeName == "Edge" or x[2].typeName == "Edge":
                logger.warn("Trying to connect edges %s:%s" % (x[1].name, x[2].name))
                continue

            key = "%s%s%s" % (source, target, slideName)
            if dictRel.has_key(key):
                continue
            else:
                dictRel[key] = slideName

            # find the diagram objects
            slideXML = self.al.findElement(self.tree, slideName)

            sxl = slideXML[0].getchildren()

            sourceID = None
            targetID = None

            for sx in sxl:
                if sx.get("name") == sourceName:
                    logger.debug("  sourceName %s[%s]:%s" % (sx.get("name"), sx.get("id"), sx.get("archimateElement")))
                    sourceID = sx.get("id")
                if sx.get("name") == targetName:
                    targetID = sx.get("id")
                    logger.debug("  targetName %s[%s]:%s" % (sx.get("name"), sx.get("id"), sx.get("archimateElement")))

            if sourceID == None or targetID == None:
                continue

            # Create Used By Relationship
            ta = dict()
            ta["name"] = self.al.cleanString(edgeName)
            ta["source"] = source
            ta["target"] = target
            ta["id"] = self.al.getID()
            ta[ARCHI_TYPE] = "archimate:UsedByRelationship"
            elm = etree.Element("element", ta, nsmap=NS_MAP)
            xp = "//folder[@name='Relations']"
            self.tree.xpath(xp)[0].insert(0, elm)
            ar = ta["id"]

            logger.debug("ar       : %s" % ar)
            logger.debug("sourceID : %s" % sourceID)
            logger.debug("targetID : %s" % targetID)

            # Create Connection at the Source
            ta = dict()
            ta["source"] = sourceID
            ta["target"] = targetID
            ta["id"] = self.al.getID()
            ta["relationship"] = ar
            ta[ARCHI_TYPE] = "archimate:Connection"

            xp = "//child[@id='" + sourceID + "']"
            elm = etree.Element("sourceConnection", ta, nsmap=NS_MAP)
            self.tree.xpath(xp)[0].insert(0, elm)

            # Update the Target
            xp = "//child[@id='" + targetID + "']"
            elm = self.tree.xpath(xp)[0].set("targetConnections", ta["id"])

        def outputXML(fileName=None):
            if fileName == None:
                fileName = self.fileImportArchimate

            self.al.outputXML(self.tree, self.fileImportArchimate)

if __name__ == "__main__":
    cafc = CreateArchiFromConcepts()

    logger.info("loading Concepts : %s" % filePPTXConcepts)
    concepts = Concepts.loadConcepts(filePPTXConcepts)

    #aConcepts.logConcepts()

    cafc.createDiagramModels(concepts)

    cafc.outputXML()



