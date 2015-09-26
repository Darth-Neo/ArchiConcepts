#!/usr/bin/python
#
# Draw Archimate Models
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'
import sys
import csv
from lxml import etree

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)

from al_Constants import *

from al_lib.ArchiLib import ArchiLib


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

    def outputXMLtoFile(self, filename=u"DiagramModeling.archimate"):
        self.al.outputXMLtoFile(filename)

        ArchiLib.stopTimer(self.start_time)

    def outputXMLtoLog(self):
        self.al.outputXMLtoLog()

        ArchiLib.stopTimer(self.start_time)

def extractBusiness(x, c=2, scale=10):

    at = u""
    unknown = 0
    folder = u"Business"

    a = x[c]

    if a[:21] == u"Rectangle Fill:Custom":
        logger.debug(u"1 %s" % a)
        at = u"archimate:BusinessObject"
        scale = 5

    elif a[:9] == u"Rectangle":
        logger.debug(u"2 %s" % a)
        at = u"archimate:BusinessObject"
        scale = 5

    elif a[:8] == u"Swimlane":
        logger.debug(u"3 %s" % a)
        at = u"archimate:BusinessActor"
        scale = 5

    elif a[:5] == u"Sheet":
        logger.debug(u"4 %s" % a)
        at = u"archimate:BusinessCollaboration"
        scale = 5

    elif a[:14] == u"CFF Container":
        logger.debug(u"5 %s" % a)
        at = u"archimate:BusinessActor"
        scale = 5

    elif a[:7] == u"Process":
        logger.debug(u"6 %s" % a)
        at = u"archimate:BusinessProcess"

    elif a[:10] == u"Phase List":
        logger.debug(u"7 %s" % a)
        at = u"archimate:BusinessActor"

    elif a[:9] == u"Separator":
        logger.debug(u"8 %s" % a)
        at = u"archimate:BusinessActor"
        scale = 5

    elif a[:7] == u"Hexagon":
        logger.debug(u"9 %s" % a)
        at = u"archimate:BusinessFunction"
        scale = 5

    elif a[:9] == u"Start/End":
        logger.debug(u"10 %s" % a)
        at = u"archimate:BusinessActor"
        scale = 5

    elif a[:10] == u"Subprocess":
        logger.debug(u"11 %s" % a)
        at = u"archimate:BusinessProcess"

    else:
        # logger.debug(u"+++> %d Unknown %s" % (unknown, a))
        unknown += 1

    return at, folder, unknown, scale

def extractApplication(x, c=2, scale=10):

    at = u""
    unknown = 0
    folder = u"Application"

    a = x[c]

    if a[:4] == u"Data":
        logger.debug(u"12 %s" % a)
        at = u"archimate:DataObject"

    elif a[:9] == u"DataPoint":
        logger.debug(u"13 %s" % a)
        at = u"archimate:DataObject"

    elif a[:8] == u"Database":
        logger.debug(u"14 %s" % a)
        at = u"archimate:ApplicationComponent"

    elif a[:8] == u"Document":
        logger.debug(u"15 %s" % a)
        at = u"archimate:DataObject"

    elif a[:12] == u"Service desk":
        logger.debug(u"16 %s" % a)
        at = u"archimate:ApplicationFunction"

    elif a[:6] == u"Output":
        logger.debug(u"17 %s" % a)
        at = u"archimate:DataObject"
        scale = 5

    elif a[:8] == u"Decision":
        logger.debug(u"18 %s" % a)
        at = u"archimate:ApplicationFunction"
        scale = 5

    else:
        # logger.debug(u"+++> %d Unknown %s" % (unknown, a))
        unknown += 1

    return at, folder, unknown, scale

if __name__ == u"__main__":
    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/Example.archimate"

    dm = DrawModels(fileArchimate)
    listNodes = list()

    #
    # Elements
    #
    fileNodes = u"DVC_2.1.csv"

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

    # Columns to import
    # 0    1    2          3          4     5
    # Name Text localCenty localCentx Width Height

    # Number of items that are not known
    unknown = 0

    n = 0

    scale = 100

    elements = list()

    for x in listNodes[1:]:

        logger.info(u"%s" % "\t".join([y for y in x]).decode(u"utf8", errors=u"ignore").strip("\n"))
        n += 1

        text = x[0]

        # at = u"archimate:%s" % x[8]
        # folder = x[9]

        #
        # Business
        #
        c = 1

        if True:
            at, folder, bu, scale = extractBusiness(x, c, scale)

            if bu != 0:
                #
                # Applications
                #
                at, folder, au, scale = extractApplication(x, c, scale)
                if au != 0:
                    # logger.debug(u"Unknown - %s" % x[1])
                    unknown += 1
                    continue

        # at = u"archimate:%s" % x[1].strip(u" ")
        # logger.info(u".%s.%s" % (at, NOTE))
        if at == NOTE or at == SYSTEM_SOFTWARE:
            logger.info(u"-->Skip - %s <---" % x[8])
            continue


        tag = u"element"
        attrib = dict()
        attrib[NAME] = text.decode(u"utf8", errors=u"ignore").strip(u"\n")
        # attrib[u"Number"] = x[7]
        attrib[ARCHI_TYPE] = at
        AE_ID_1 = dm.createArchimateElement(tag, folder, attrib)

        #
        # Create Bounds
        #

        nl = list()

        xx = (float(x[4]) - (float(x[2]) * 0.5)) * scale
        yy = (float(x[3]) - (float(x[3]) * 0.5)) * scale

        nl.append(AE_ID_1)
        bounds = dict()
        bounds[u"x"] = str(int(round(float(xx), 0)))
        bounds[u"y"] = str(int(round(float(yy), 0)))
        bounds[u"width"] = str(int(round(float(x[4]) * scale, 0)))
        bounds[u"height"] = str(int(round(float(x[5]) * scale, 0)))
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
