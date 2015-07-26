#!/usr/bin/python
#
# Draw Archimate Models
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib

from lxml import etree

#
# Globals
#
n = 10

class DrawModels(object):

    fileArchimate= None
    n = None
    al = None

    width = u"120"
    height = u"55"

    def __init__(self, fileArchimate):
        self.fileAchimate = fileArchimate
        self.n = 0
        self.al = ArchiLib(fileArchimate)

        self.start_time = ArchiLib.startTimer()

    def createArchimateElement(self, tag, folder, attrib):

        self.al.insertNode(tag, folder, attrib, new=False)
        AE_ID = attrib[ID]

        return AE_ID

    def createArchimateRelations(self, tag, folder, attrib):

        self.al.insertRel(tag, folder, attrib, new=False)
        AR_ID = attrib[ID]

        return AR_ID

    # <element
    #    xsi:type="archimate:ArchimateDiagramModel"
    #    id="66de3166"
    #    name="Info">

    def createDiagramModel(self, tag=None, folder=None, attrib=None):

        if tag == None and folder==None and attrib==None:
            tag = u"element"
            folder = u"Views"
            attrib = dict()
            attrib[NAME] = u"DM-TDO%d" % self.n
            attrib[ARCHI_TYPE] = DIAGRAM_MODEL
            self.al.insertNode(tag, folder, attrib)
            DMO_ID = attrib[ID]
            DMO = self.al.findDiagramModel(attrib[ID])

            if len(DMO) == 1:
                DMO = DMO[0]
            else:
                logger.error(u"Diagram Model Not Found")
                raise LookupError(u"Ops")

            return DMO
        else:
            self.al.insertNode(tag, folder, attrib)
            DMO_ID = attrib[ID]
            DMO = self.al.findDiagramModel(attrib[ID])

            if len(DMO) == 1:
                DMO = DMO[0]
            else:
                logger.error(u"Diagram Model Not Found")
                raise LookupError(u"Ops")

    # <child
    #     xsi:type="archimate:DiagramObject"
    #     id="ffc36ce0"
    #     lineColor="#000000"
    #     textAlignment="2"
    #     fillColor="#00ffff"
    #     archimateElement="4b326945">
    #  </child>

    def createDiagramObject(self, DMO, AE_ID, Bounds):

        tag = u"child"
        attrib = dict()
        attrib[ID] = self.al.getID()
        attrib[ARCHI_TYPE] = DIAGRAM_OBJECT
        attrib[u"lineColor"] = u"#000000"
        attrib[u"textAlignment"] = u"2"
        attrib[u"targetConnections"] = u""
        attrib[u"fillColor"] = u"#ffff00"
        attrib[u"archimateElement"] = AE_ID

        elm = etree.Element(tag, attrib, nsmap=NS_MAP)
        DMO.append(elm)
        DOE = self.al.findDiagramObject(attrib[ID])

        if len(DOE) == 1:
            DOE = DOE[0]
        else:
            logger.error(u"Diagram Object Not Found")
            raise LookupError(u"Ops")

        self.createBounds(DOE, Bounds)

        return DOE

    #
    # Create Bounds in DiagramObject
    # Example:
    #     <bounds
    #     x="162" y="175"
    #     width="120" height="55"
    # />
    def createBounds(self, DOE, attrib):

        tag = u"bounds"
        elm = etree.Element(tag, attrib, nsmap=NS_MAP)
        DOE.insert(0, elm)

    #
    # Create SourceConnections
    # Example:
    #     <sourceConnection
    #     xsi:type="archimate:Connection"
    #     id="592e8439"
    #     lineColor="#b1b1b1"
    #     source="4b59249d"
    #     target="c3fd7d30"
    #     relationship="27d1a38d"/>

    def createConnection(self, DOE1, DOE2, R_ID):

        tag = u"sourceConnection"
        attrib = dict()
        attrib[ARCHI_TYPE] = u"archimate:Connection"
        attrib[u"lineColor"] = u"#b1b1b1"
        attrib[ID] = self.al.getID()
        attrib[u"source"] = DOE1.get(ID)
        attrib[u"target"] = DOE2.get(ID)
        attrib[u"relationship"] = R_ID
        elm = etree.Element(tag, attrib, nsmap=NS_MAP)
        DOE1.insert(0, elm)
        SC_ID = attrib[ID]

        #
        # Aggregate target connectins
        # <child xsi:type="archimate:DiagramObject"
        #             id="52f55838"
        #             lineColor="#000000"
        #             textAlignment="2"
        #             targetConnections=""
        #             fillColor="#ffff00"
        #             archimateElement="c5369205">
        #        <bounds height="55"
        #  width="120" x="162" y="175"/>
        #      </child>

        attrib = DOE2.attrib

        if u"targetConnections" in attrib:
            attrib[u"targetConnections"] = attrib[u"targetConnections"] + " " + SC_ID
        else:
            attrib[u"targetConnections"] = " " + SC_ID

    #
    # Draw Model
    #
    def drawModel(self, elements):

        for AE_ID_1, b1, AE_ID_2, b2, R_ID in elements:
            #
            # Diagram Model
            #
            DMO = self.createDiagramModel()

            #
            # DiagramObjects
            #

            # <bounds x="181" y="129" width="120" height="55"/>
            bounds = dict()
            bounds[u"x"] = b1[u"x"]
            bounds[u"y"] = b1[u"y"]
            bounds[u"width"] = self.width
            bounds[u"height"] = self.height

            DOE1 = self.createDiagramObject(DMO, AE_ID_1, bounds)
            #self.createBounds(DOE1, bounds)

            # <bounds x="62" y="75" width="120" height="55"/>
            bounds = dict()
            bounds[u"x"] = b2[u"x"]
            bounds[u"y"] = b2[u"y"]
            bounds[u"width"] = self.width
            bounds[u"height"] = self.height

            DOE2 = self.createDiagramObject(DMO, AE_ID_2, bounds)
            # self.createBounds(DOE2, bounds)

            self.createConnection(DOE1, DOE2, R_ID)


    def outputXMLtoFile(self, filename=u"DiagramModeling.archimate"):
        self.al.outputXMLtoFile(filename)

        ArchiLib.stopTimer(self.start_time)

    def outputXMLtoLog(self):
        self.al.outputXMLtoLog()

        ArchiLib.stopTimer(self.start_time)

if __name__ == u"__main__":
    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/test.archimate"

    dm = DrawModels(fileArchimate)

    #
    # Elements
    #

    elements = list()

    tag = u"element"
    folder = u"Business"
    attrib = dict()
    attrib[NAME] = u"DO%d" % dm.n
    attrib[ARCHI_TYPE] = u"archimate:BusinessObject"
    AE_ID_1 = dm.createArchimateElement(tag, folder, attrib)

    dm.n += 1
    tag = u"element"
    folder = u"Business"
    attrib = dict()
    attrib[NAME] = u"DO%d" % dm.n
    attrib[ARCHI_TYPE] = u"archimate:BusinessObject"
    AE_ID_2 = dm.createArchimateElement(tag, folder, attrib)

    dm.n += 1
    tag = u"element"
    folder = u"Relations"
    attrib = dict()
    attrib[ID] = dm.al.getID()
    attrib[u"source"] = AE_ID_1
    attrib[u"target"] = AE_ID_2
    attrib[ARCHI_TYPE] = u"archimate:AssociationRelationship"
    R_ID = dm.createArchimateRelations(tag, folder, attrib)

    #
    # Create Bounds
    #

    nl = list()
    nl.append(AE_ID_1)
    bounds = dict()
    bounds[u"x"] = u"181"
    bounds[u"y"] = u"129"
    nl.append(bounds)

    nl.append(AE_ID_2)
    bounds = dict()
    bounds[u"x"] = u"62"
    bounds[u"y"] = u"75"
    nl.append(bounds)
    nl.append(R_ID)

    elements.append(nl)

    dm.drawModel(elements)

    dm.outputXMLtoFile(filename=u"dm.archimate")
