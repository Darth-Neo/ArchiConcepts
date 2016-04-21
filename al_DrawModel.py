#!/usr/bin/env python
#
# Draw Archimate Models
#
# __author__ = u'morrj140'
# __VERSION__ = u'0.3'
import sys
import csv
from lxml import etree
from al_Constants import *
from al_lib.ArchiLib import ArchiLib

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)


class DrawModels(object):

    fileArchimate= None
    n = None
    al = None
    width = None
    height = None

    def __init__(self, fileArchimate):
        self.fileAchimate = fileArchimate
        self.n = 0
        self.al = ArchiLib(fileArchimate)

        self.start_time = ArchiLib.startTimer()

        self.width = u"120"
        self.height = u"55"

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

        if tag is None and folder is None and attrib is None:
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

        #
        # Diagram Model
        #
        DMO = self.createDiagramModel()

        for AE_ID, bnds in elements:
            #
            # DiagramObjects
            #
            self.createDiagramObject(DMO, AE_ID, bnds)

    #
    # Output Model
    #
    def outputXMLtoFile(self, filename=u"DiagramModeling.archimate"):
        self.al.outputXMLtoFile(filename)

        ArchiLib.stopTimer(self.start_time)

    def outputXMLtoLog(self):
        self.al.outputXMLtoLog()

        ArchiLib.stopTimer(self.start_time)

    @staticmethod
    def readElements(fileNodes):
        try:
            with open(fileNodes, "rU") as f:
                try:
                    reader = csv.reader(f)
                    listNodes = list(reader)
                except Exception, msg:
                    logger.error(u"%s" % msg)
                    sys.exit()

        except Exception, msg:
            logger.error(u"%s" % msg)

        return listNodes


if __name__ == u"__main__":

    pathModel = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models"

    # fileArchimateXML = u"DVC v3.17.archimate"
    # fileArchimateXML = u"Solution_Engineering_Template_V8.archimate"
    fileArchimateXML = u"RTPv9.archimate"

    fileArchimate = pathModel + os.sep + fileArchimateXML

    fileArchimateOutput = os.getcwd() + os.sep + fileArchimateXML[:-10] + u"drawmodel.archimate"

    dm = DrawModels(fileArchimate)

    listNodes = list()

    #
    # Elements
    #
    fileNodes = u"DVC_Dues_5.csv"
    listNodes = DrawModels.readElements(fileNodes)

    # Columns to import
    # 0 1      2     3            4           5      6      7        8
    # n	shpTxt shpNm shpLayerName Connections ShapeX ShapeY shpWidth shpHeight

    # Number of items that are not known
    unknown = 0
    n = 0
    scale = 100

    elements = list()

    for x in listNodes[1:]:

        n += 1
        shpNum = x[0]
        shpTxt = x[1]
        shpNm  = x[2]
        shpLayerName = x[3]
        shapeX = x[5]
        shapeY = x[6]
        shpWidth = x[7]
        shpHeight = x[8]

        shpLayerName = shpLayerName.decode(u"utf8", errors=u"ignore")



        if shpNm == u"** to **" or shpNm == u"## to ##" or shpLayerName == u"Connections":
            logger.debug(u"Skip - %s" % shpNm)
            continue
        else:
            logger.debug(u"%s" % u"\n".join([y.decode(u"utf8", errors=u"ignore").strip(u"\n") for y in x]))

        folder = u"Application"

        at = u"archimate:%s" % shpLayerName
        logger.info(u"at : %s" % at)

        tag = u"element"
        attrib = dict()
        attrib[NAME] = shpTxt.decode(u"utf8", errors=u"ignore").strip(u"\n")
        attrib[u"Number"] = shpNum
        attrib[ARCHI_TYPE] = at
        AE_ID_1 = dm.createArchimateElement(tag, folder, attrib)

        #
        # Create Bounds
        #
        # Note: all coordinates are based on having center of page 0,0
        nl = list()

        xx = float(shapeX) * scale
        yy = float(shapeY) * scale

        nl.append(AE_ID_1)
        bounds = dict()
        bounds[u"x"] = str(int(round(float(xx), 0)))
        bounds[u"y"] = str(int(round(float(yy), 0)))
        bounds[u"width"] = str(int(round(float(shpWidth) * scale, 0)))
        bounds[u"height"] = str(int(round(float(shpHeight) * scale, 0)))
        nl.append(bounds)

        elements.append(nl)

    logger.info(u"%d unknown" % unknown)

    dm.drawModel(elements)

    dm.outputXMLtoFile(filename=u"dm.mxl")

    try:
        from lxml import etree
        tree = etree.parse(u"dm.mxl")

    except Exception, msg:
        logger.error(u"%s" % msg)

    dm.outputXMLtoFile(filename=u"dm.archimate")
