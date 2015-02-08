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

from al_ArchiLib import *

dictPoints = dict()
dictDO = dict()

#<?xml version="1.0" encoding="UTF-8"?>
#<archimate:model xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:archimate="http://www.archimatetool.com/archimate" name="Example" id="b2a177dc" version="2.6.0">
#  <folder name="Business" id="349dea12" type="business">
#    <element xsi:type="archimate:BusinessActor" id="5789571a" name="Joe"/>
#    <element xsi:type="archimate:BusinessObject" id="fcf92fce" name="Wallet"/>
#    <element xsi:type="archimate:BusinessObject" id="8006f892" name="cw"/>
#    <element xsi:type="archimate:BusinessObject" id="85c1b74a" name="a"/>
#    <element xsi:type="archimate:BusinessObject" id="98a20ea0" name="b"/>
#  </folder>
#  <folder name="Application" id="f27ffa65" type="application"/>
#  <folder name="Technology" id="89783c9f" type="technology"/>
#  <folder name="Motivation" id="83595ab6" type="motivation"/>
#  <folder name="Implementation &amp; Migration" id="068d1743" type="implementation_migration"/>
#  <folder name="Connectors" id="80d65d0f" type="connectors"/>
#  <folder name="Relations" id="42824c7c" type="relations">
#    <element xsi:type="archimate:AccessRelationship" id="2f2f9f96" source="5789571a" target="fcf92fce"/>
#  </folder>
#  <folder name="Views" id="d18c15b0" type="diagrams">
#    <element xsi:type="archimate:ArchimateDiagramModel" id="176899e1" name="Default View">
#      <child xsi:type="archimate:DiagramObject" id="74386658" textAlignment="2" archimateElement="5789571a">
#        <bounds x="200" y="96"/>
#        <sourceConnection xsi:type="archimate:Connection" id="95144175" source="74386658" target="5256ff1f" relationship="2f2f9f96"/>
#      </child>
#      <child xsi:type="archimate:DiagramObject" id="5256ff1f" textAlignment="2" targetConnections="95144175" archimateElement="fcf92fce">
#        <bounds x="375" y="212"/>
#      </child>
#      <child xsi:type="archimate:DiagramObject" id="07d1f9c0" textAlignment="2" archimateElement="8006f892">
#        <bounds x="494" y="266"/>
#      </child>
#      <child xsi:type="archimate:DiagramObject" id="d00524a1" textAlignment="2" archimateElement="85c1b74a">
#        <bounds x="494" y="212"/>
#      </child>
#      <child xsi:type="archimate:DiagramObject" id="2689e8f1" textAlignment="2" archimateElement="98a20ea0">
#        <bounds x="375" y="266"/>
#      </child>
#    </element>
#  </folder>
#</archimate:model>

def showConcepts(concepts):
    n = 0
    for x in concepts.getConcepts().values():
        n += 1
        logger.info("x %s[%s]" % (x.name, x.typeName))
        for y in x.getConcepts().values():
            logger.info("  y %s[%s]" % (y.name, y.typeName))
            for z in y.getConcepts().values():
                if not (z.name in ("h", "l", "t", "w")):
                    logger.info("    z  %s[%s]" % (z.name, z.typeName))



def createDiagramModels(concepts, tree):

    # <folder name="Views" id="d18c15b0" type="diagrams">
    attrib = dict()
    attrib["id"] = str(getID())
    newFolder = "PowerPointApps"
    attrib["name"] = newFolder

    xp = "//folder[@name='Application']"
    elm = etree.Element("folder", attrib, nsmap=NS_MAP)
    tree.xpath(xp)[0].insert(0, elm)

    # Make new PowerPoint Folder to import into
    # <folder name="Views" id="d18c15b0" type="diagrams">
    attrib = dict()
    attrib["id"] = str(getID())
    newFolder = "PowerPoint"
    attrib["name"] = newFolder

    xp = "//folder[@name='Views']"
    elm = etree.Element("folder", attrib, nsmap=NS_MAP)
    tree.xpath(xp)[0].insert(0, elm)
    Folder_ID = attrib["id"]

    # <element xsi:type="archimate:ArchimateDiagramModel" id="176899e1" name="Default View">
    for x in concepts.getConcepts().values():
        logger.debug("%s[%s]-%d" % (x.name, x.typeName, len(x.name)))
        if x.typeName == "Slide":
            logger.info("Slide %s[%s]-%d" % (x.name, x.typeName, len(x.name)))

            # Create "archimate:ArchimateDiagramModel"
            attrib = dict()
            attrib["name"] = x.name
            attrib["id"] = str(getID())
            attrib[ARCHI_TYPE] = "archimate:ArchimateDiagramModel"
            xp = "//folder[@name='PowerPoint']"
            elm = etree.Element("element", attrib, nsmap=NS_MAP)
            txp = tree.xpath(xp)
            txp[0].insert(0, elm)
            DM_ID = attrib["id"]

            createArchimateComponents(x, DM_ID, tree)

    createConnections(concepts)

def createArchimateComponents(concepts, dmID, tree):

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
            insertNode("element", "PowerPointApps", tree, attribAC)
            acID = attribAC["id"]
            logger.info("  Create acID %s" % (acID))
            dictACDone[x.name] = acID
        else:
            acID = dictACDone[x.name]

        logger.info("  %s[%s]-%d -- %s" % (x.name, x.typeName, len(x.name), acID))

    logger.info("Create Diagram Objects")
    createDiagramObjects(concepts, dmID, tree, dictACDone)


def createDiagramObjects(concepts, dmID, tree, dictACDone, dictDODone = None):
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
            attribDO["id"] = str(getID())
            attribDO["textAlignment"] = "2"
            attribDO["archimateElement"] = acID
            attribDO[ARCHI_TYPE] = "archimate:DiagramObject"

            elm = etree.Element("child", attribDO, nsmap=NS_MAP)
            doID = attribDO["id"]

            xp = "//element[@id='" + dmID + "']"
            tree.xpath(xp)[0].insert(0, elm)

            logger.debug("doID %s" % (doID))

            l = float(coordinates["l"].typeName)
            t = float(coordinates["t"].typeName)
            w = float(coordinates["w"].typeName)
            h = float(coordinates["h"].typeName)

            cx = int(l * 100)
            cy = int(t * 100) - 150

            key = "%s%s" % (cx,cy)
            if dictPoints.has_key(key):
                cx = 100 + cx
                cy = 100 + cy
            else:
                dictPoints[key] = key

            attrib = dict()
            attrib["x"] = str(cx)
            attrib["y"] = str(cy)
            elm = etree.Element("bounds", attrib, nsmap=NS_MAP)
            xp = "//child[@id='" + doID + "']"
            tree.xpath(xp)[0].insert(0, elm)

            dictDODone[x.name] = doID

        createDiagramObjects(x, dmID, tree, dictACDone, dictDODone)

def createConnections(concepts):

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
                        tcee.name = cleanString(tcee.name)
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

            src = findElement(tree, sourceName)
            if src != None:
                source = src[0].get("id")
            else:
                logger.warn("***No Source***")
                source = " "

            tgt = findElement(tree, targetName)
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
        slideXML = findElement(tree, slideName)

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
        ta["name"] = cleanString(edgeName)
        ta["source"] = source
        ta["target"] = target
        ta["id"] = getID()
        ta[ARCHI_TYPE] = "archimate:UsedByRelationship"
        elm = etree.Element("element", ta, nsmap=NS_MAP)
        xp = "//folder[@name='Relations']"
        tree.xpath(xp)[0].insert(0, elm)
        ar = ta["id"]

        logger.debug("ar       : %s" % ar)
        logger.debug("sourceID : %s" % sourceID)
        logger.debug("targetID : %s" % targetID)

        # Create Connection at the Source
        ta = dict()
        ta["source"] = sourceID
        ta["target"] = targetID
        ta["id"] = getID()
        ta["relationship"] = ar
        ta[ARCHI_TYPE] = "archimate:Connection"

        xp = "//child[@id='" + sourceID + "']"
        elm = etree.Element("sourceConnection", ta, nsmap=NS_MAP)
        tree.xpath(xp)[0].insert(0, elm)

        # Update the Target
        xp = "//child[@id='" + targetID + "']"
        elm = tree.xpath(xp)[0].set("targetConnections", ta["id"])

if __name__ == "__main__":
    filePPConcepts = "pptx.p"
    fileArchimateIn = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/CodeGen_v34.archimate"
    #fileArchimateIn = "/Users/morrj140/Development/GitRepository/ArchiConcepts/baseline.archimate"
    #fileArchimateOut = 'import_pp.archimate'

    etree.QName(ARCHIMATE_NS, 'model')
    tree = etree.parse(fileArchimateIn)

    logAll(tree)

    aConcepts = Concepts.loadConcepts(filePPConcepts)

    #aConcepts.logConcepts()

    createDiagramModels(aConcepts, tree)

    outputXML(tree, filename="pp_models.archimate")



