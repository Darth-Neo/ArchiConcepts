__author__ = 'morrj140'

import sys
import os
import StringIO
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

import import_artifacts as ia
EMU = 914400.0

namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}

XML_NS         =  "http://www.w3.org/2001/XMLSchema-instance"
ARCHIMATE_NS   =  "http://www.archimatetool.com/archimate"
NS_MAP = {"xsi": XML_NS, "archimate" : ARCHIMATE_NS}

ARCHI_TYPE = "{http://www.w3.org/2001/XMLSchema-instance}type"

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

def createDiagramModels(concepts, tree):

    # <folder name="Views" id="d18c15b0" type="diagrams">
    attrib = dict()
    attrib["id"] = str(ia.getID())
    newFolder = "PowerPointApps"
    attrib["name"] = newFolder

    xp = "//folder[@name='Application']"
    elm = etree.Element("folder", attrib, nsmap=NS_MAP)
    tree.xpath(xp)[0].insert(0, elm)

    # Make new PowerPoint Folder to import into
    # <folder name="Views" id="d18c15b0" type="diagrams">
    attrib = dict()
    attrib["id"] = str(ia.getID())
    newFolder = "PowerPoint"
    attrib["name"] = newFolder

    xp = "//folder[@name='Views']"
    elm = etree.Element("folder", attrib, nsmap=NS_MAP)
    tree.xpath(xp)[0].insert(0, elm)
    Folder_ID = attrib["id"]

    # <element xsi:type="archimate:ArchimateDiagramModel" id="176899e1" name="Default View">
    for x in concepts.getConcepts().values():

        if x.typeName == "Slide" and len(x.name) > 1:
            logger.info("Slide %s[%s]-%d" % (x.name, x.typeName, len(x.name)))

            # Create "archimate:ArchimateDiagramModel"
            attrib = dict()
            attrib["name"] = x.name
            attrib["id"] = str(ia.getID())
            attrib[ARCHI_TYPE] = "archimate:ArchimateDiagramModel"
            xp = "//folder[@name='PowerPoint']"
            elm = etree.Element("element", attrib, nsmap=NS_MAP)
            txp = tree.xpath(xp)
            txp[0].insert(0, elm)
            DM_ID = attrib["id"]

            createDiagramObjects(x, DM_ID, tree)

    createConnections(concepts)


def createDiagramObjects(concepts, dmID, tree):
    # Creare connection inside the start
    # <child xsi:type="archimate:DiagramObject" id="74386658" textAlignment="2" archimateElement="5789571a">
    #        <bounds x="200" y="96"/>
    #        <sourceConnection xsi:type="archimate:Connection" id="95144175" source="74386658" target="5256ff1f" relationship="2f2f9f96"/>
    # </child>

    listST = list()
    for x in concepts.getConcepts().values():

        # Create the archimate:ApplicationComponent
        attribAC = dict()
        attribAC["name"] = x.name
        attribAC[ARCHI_TYPE] = "archimate:ApplicationComponent"
        ia.insertNode("element", "PowerPointApps", tree, attribAC)
        acID = attribAC["id"]
        logger.debug("acID %s" % (acID))

        logger.info("Source %s[%s]-%d -- %s" % (x.name, x.typeName, len(x.name), acID))

        # Create "archimate:DiagramObject"
        attribDO = dict()
        attribDO["name"] = x.name
        attribDO["id"] = str(ia.getID())
        attribDO["textAlignment"] = "2"
        attribDO["archimateElement"] = acID
        attribDO[ARCHI_TYPE] = "archimate:DiagramObject"
        elm = etree.Element("child", attribDO, nsmap=NS_MAP)
        doID = attribDO["id"]
        xp = "//element[@id='" + dmID + "']"
        tree.xpath(xp)[0].insert(0, elm)
        logger.debug("doID %s" % (doID))

        # Create Coordinates
        coordinates = x.getConcepts()

        l = float(coordinates["l"].typeName)
        t = float(coordinates["t"].typeName)
        w = float(coordinates["w"].typeName)
        h = float(coordinates["h"].typeName)

        cx = int(l * 100)
        cy = int(t * 100)

        attrib = dict()
        attrib["x"] = str(cx)
        attrib["y"] = str(cy)
        elm = etree.Element("bounds", attrib, nsmap=NS_MAP)
        xp = "//child[@id='" + doID + "']"
        tree.xpath(xp)[0].insert(0, elm)

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

def findElement(tree, name):
    xp = "//element[@name='%s']" % name
    stp = tree.xpath(xp)
    return stp

def createConnections(concepts):

    listST = list()
    logger.info("Children")

    # find children
    for tc in concepts.getConcepts().values():
        if len(tc.name) > 1:
            logger.info(" Slide %s[%s]-%d" % (tc.name, tc.typeName, len(tc.name)))

            for tcc in tc.getConcepts().values():
                if tcc.typeName == "Source":
                    logger.info("  Source %s[%s]-%d" % (tcc.name, tcc.typeName, len(tcc.name)))

                    for tce in tcc.getConcepts().values():
                        if len(tce.name) > 1 and tce.typeName == "Target":
                            logger.info("   Target %s[%s]-%d" % (tce.name, tce.typeName, len(tce.name)))

                            for tcee in tce.getConcepts().values():
                                if tcee.typeName == "Edge":
                                    logger.info("    Edge %s[%s]-%d" % (tcee.name, tcee.typeName, len(tcee.name)))
                                    ll = (tc, tcc, tce, tcee)
                                    listST.append(ll)

    dictRel = dict()

    if True:
        for x in listST:
            try:
                source = findElement(tree, x[1].name)[0].get("id")
                target = findElement(tree, x[2].name)[0].get("id")
            except:
                continue

            edge   = x[3].name

            key = "%s%s%s" % (source,target,edge)
            if dictRel.has_key(key):
                pass
            else:
                dictRel[key] = edge

            logger.info("Source-Target : %s-%s" % (source, target))

            # Create Access Relationship
            ta = dict()
            ta["name"] = edge
            ta["source"] = source
            ta["target"] = target
            ta["id"] = ia.getID()
            ta[ARCHI_TYPE] = "archimate:AccessRelationship"
            elm = etree.Element("element", ta, nsmap=NS_MAP)
            xp = "//folder[@name='Relations']"
            tree.xpath(xp)[0].insert(0, elm)
            ar = ta["id"]

            # Create Connection at the Source
            #ta = dict()
            #ta["source"] = source
            #ta["target"] = target
            #ta["id"] = ia.getID()
            #ta["relationship"] = ar
            #ta[ARCHI_TYPE] = "archimate:Connection"
            #elm = etree.Element("sourceConnection", ta, nsmap=NS_MAP)
            #xp = "//child[@id='" + source + "']"
            #tree.xpath(xp)[0].insert(0, elm)

            # Update the Target
            #xp = "///child[@id='" + target + "']"
            #elm = tree.xpath(xp)[0].set("targetConnections", ta["id"])



def createNodes():
    pass

if __name__ == "__main__":
    filePPConcepts = "pptx.p"
    fileArchimateIn = "baseline.archimate"
    fileArchimateOut = 'import_pp.archimate'

    etree.QName(ARCHIMATE_NS, 'model')
    tree = etree.parse(fileArchimateIn)

    ia.logAll(tree)

    aConcepts = Concepts.loadConcepts(filePPConcepts)

    #aConcepts.logConcepts()

    createDiagramModels(aConcepts, tree)

    ia.outputXML(tree, filename="pp_models.archimate")



