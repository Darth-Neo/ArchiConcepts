__author__ = 'morrj140'

import sys
import os
import StringIO
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

from PPTXCrawl import *

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

def createDiagramModesl(concepts, fileArchimateIn, fileArchimateOut):
    etree.QName(ARCHIMATE_NS, 'model')
    tree = etree.parse(fileArchimateIn)
    PPTXCrawl.logAll(tree)

    # <folder name="Views" id="d18c15b0" type="diagrams">
    folder = "PP_Models"
    attrib = dict()
    attrib["id"] = PPTXCrawl.getID()
    attrib["name"] = folder
    PPTXCrawl.insertNode("folder", folder, tree, attrib)
    Folder_ID = attrib["id"]

    tag = "element"

    # <element xsi:type="archimate:ArchimateDiagramModel" id="176899e1" name="Default View">
    for x in concepts.getConcepts():

        # Create "archimate:DiagramObject" inside "archimate:ArchimateDiagramModel"
        attrib = dict()
        attrib["name"] = x.name
        attrib[ARCHI_TYPE] = "archimate:ArchimateDiagramModel"
        PPTXCrawl.insertNode(tag, folder, tree, attrib)
        DM_ID = attrib["id"]

        createDiagramObjects(x, DM_ID, tree)


def createDiagramObjects(concepts, DM_ID, tree):
    # Creare connection inside the start
    # <child xsi:type="archimate:DiagramObject" id="74386658" textAlignment="2" archimateElement="5789571a">
    #        <bounds x="200" y="96"/>
    #        <sourceConnection xsi:type="archimate:Connection" id="95144175" source="74386658" target="5256ff1f" relationship="2f2f9f96"/>
    # </child>

    tag = "element"
    folder = "PP_Models"
    xp = "//folder[@name='" + folder + "']"
    txp = tree.xpath(xp)

    for x in concepts.getConcepts():

        DO = "74386658"

        strXML1 = "<child xsi:type=\"archimate:DiagramObject\" id=\"%s\" textAlignment=\"2\" archimateElement=\"5789571a\">" % (DO)
        strXML2 = " <bounds x=\"200\" y=\"96\"/>"
        strXML3 = " <sourceConnection xsi:type=\"archimate:Connection\" id=\"95144175\" source=\"74386658\" target=\"5256ff1f\" relationship=\"2f2f9f96\"/>"
        strXML4 = "</child>"

        # Create "archimate:DiagramObject" inside "archimate:ArchimateDiagramModel"
        attrib = dict()
        attrib["name"] = x.name
        attrib[ARCHI_TYPE] = "archimate:ArchimateDiagramModel"
        PPTXCrawl.insertNode(tag, folder, tree, attrib)
        DM_ID = attrib["id"]

        elm = etree.Element(tag, attrib, nsmap=NS_MAP)
        txp[0].insert(0, elm)

def createNodes():
    pass

if __name__ == "__main__":
    filePPConcepts = "pptx.p"
    fileArchimateIn = "//Users/morrj140/Documents/SolutionEngineering/Archimate Models/CodeGen_v20.archimate"
    fileArchimateOut = 'import_pp.archimate'

    aConcepts = Concepts.logConcepts(filePPConcepts, fileArchimateIn, fileArchimateOut)

    createDiagramModesl(aConcepts)



