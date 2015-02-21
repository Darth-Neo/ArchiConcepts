#!/usr/bin/python
#
# Create PPTX from Archimate XML
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import glob, time, math, zipfile

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from lxml import etree
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches
from pptx.dml.color import RGBColor
#from pptx.enum.dml import MSO_THEME_COLOR
from pptx.util import Pt
#from pptx.oxml.shapes import connector
#from pptx.parts.slide import _SlideShapeTree

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from al_ArchiLib.ArchiLib import ArchiLib

from al_ArchiLib.Constants import *

class ArchiCreatePPTX(object):
    filePPTXIn  = None
    filePPTXOut = None

    def __init__(self, afileArchimate, afilePPTXIn, afilePPTXOut):
        self.A_NS           =  "http://schemas.openxmlformats.org/drawingml/2006/main"
        self.P_NS           =  "http://schemas.openxmlformats.org/presentationml/2006/main"
        self.R_NS           =  "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

        self.namespacesPPTX = {"p" : self.P_NS, "a" : self.A_NS, "r" : self.R_NS}

        self.SLD_LAYOUT_TITLE_AND_CONTENT = 1
        self.TITLE_ONLY_SLIDE_LAYOUT = 5

        self.SCALE = 0.90
        self.EMU = 914400.0

        self.filePPTXIn     = afilePPTXIn
        self.filePPTXOut    = afilePPTXOut
        self.fileArchimate  = fileArchimate

        if os.path.isfile(self.fileArchimate) <> True:
            logger.error("File does not exist : %s" % self.fileArchimate)

        etree.QName(ARCHIMATE_NS, 'model')
        self.tree = etree.parse(self.fileArchimate)

        self.prs = Presentation()

    # Example of what the xml for a connector looks like
    def addXMLConnector(self, shape):
        name = "Straight Arrow Connector 43"
        id = 34
        sourceID = 21
        targetID = 9

        t = shape.top / self.EMU
        l = shape.left / self.EMU
        h = shape.height / self.EMU
        w = shape.width / self.EMU

        nid = shape.id
        shape.name = "Straight Arrow Connector 43"

        logger.debug("shape.top     : %3.2f" % (t))
        logger.debug("shape.left    : %3.2f" % (l))
        logger.debug("shape.height  : %3.2f" % (h))
        logger.debug("shape.width   : %3.2f" % (w))
        logger.debug("shape.shape_type    : %s" % shape.shape_type)
        xmlConnector = " \
             <p:cxnSp xmlns:p=\"http://schemas.openxmlformats.org/presentationml/2006/main\" " \
                "xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\" " \
                "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\"> \
              <p:nvCxnSpPr> \
                <p:cNvPr id=\"34\" name=\"Straight Arrow Connector 43\"/> \
                <p:cNvCxnSpPr> \
                  <a:stCxn id=\"21\" idx=\"3\"/> \
                  <a:endCxn id=\"9\" idx=\"1\"/> \
                </p:cNvCxnSpPr> \
                <p:nvPr/> \
              </p:nvCxnSpPr> \
              <p:spPr> \
                <a:xfrm flipV=\"1\">  \
                  <a:off x=\"5056479\" y=\"3507277\"/>  \
                  <a:ext cx=\"1642504\" cy=\"12357\"/> \
                </a:xfrm> \
                <a:prstGeom prst=\"straightConnector1\"> <a:avLst/></a:prstGeom> \
                <a:ln> <a:headEnd type=\"none\"/> <a:tailEnd type=\"arrow\"/> </a:ln> \
              </p:spPr> \
              <p:style> \
                <a:lnRef idx=\"1\"> <a:schemeClr val=\"dk1\"/> </a:lnRef>  \
                <a:fillRef idx=\"0\"> <a:schemeClr val=\"dk1\"/> </a:fillRef> \
                <a:effectRef idx=\"0\"> <a:schemeClr val=\"dk1\"/> </a:effectRef>  \
                <a:fontRef idx=\"minor\"> \
                    <a:schemeClr val=\"tx1\"/>  \
                </a:fontRef> \
              </p:style>  \
            </p:cxnSp> "

        shape.element.xml = xmlConnector

    def getNode(self, n, listModels, type):

        attributes = n.attrib

        if attributes.get(ARCHI_TYPE) == type:
            if attributes.get("id") != None:
                listModels.append((n, attributes))

                logger.debug("%s : %s:%s:%s:%s" % (DIAGRAM_MODEL, n.tag, n.get("name"), n.get("id"), attributes.get(ARCHI_TYPE)))

        for y in n:
            self.getNode(y, listModels, type)

    def getAll(self, listModels, type=DIAGRAM_MODEL):
        for x in self.tree.getroot():
            self.getNode(x, listModels, type)

    def findNode(self, id, tag="element"):
        logger.debug("id = %s" % id)
        xp = "//%s[@id='%s']" % (tag, id)
        stp = self.tree.xpath(xp)

        if len(stp) > 0:
            return stp[0]

        return stp

    def findDiagramObject(self, listDO, value):
        for x in listDO:
            if x[0] == "archimate:DiagramObject":
                logger.debug("value : %s[%s] x : %s[%s]" % (value, type(value), x[3], type(x[3])))
                if x[3] == value:
                    logger.debug("Found!")
                    return x

        return None

    def project(self, x, y, scale=None):

        if scale == None:
            scale = self.SCALE
        try:
            x = (((float(x) / 100.0)) * scale)
            y = (((float(y) / 100.0)) * scale)
            return x, y
        except:
            return None, None

    def findShape(self, sm, listDO):

        for model in listDO:
            if model == sm:
                return model[6]

        return None

    def fixSlides(self, listSlides):

        # unzip .pptx to temporary space and remove file
        timestamp = str(time.time()).replace(".", "")
        zip_file = zipfile.ZipFile(self.PPTXFilename, "r")
        zip_file.extractall(os.path.join("./tmp", timestamp))
        zip_file.close

        os.remove(self.PPTXFilename)

        # register necessary namespaces
        etree.register_namespace("a", "http://schemas.openxmlformats.org/drawingml/2006/main")
        etree.register_namespace("p", "http://schemas.openxmlformats.org/presentationml/2006/main")
        etree.register_namespace("r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships")

        # parse xml document and find shape tree
        slideNum = 1
        slideFilename = "slide%d.xml" % slideNum
        tree = etree.parse(os.path.join("./tmp", timestamp, "ppt", "slides", slideFilename))

        root = tree.getroot()

        max_sp = 0
        xp = "//@id"
        for sp in tree.xpath(xp):
            if int(sp) > max_sp:
                max_sp = int(sp)
            logger.debug("sp : %s" % (sp))

        n = 1
        for connector in self.listConnectors:

            connectorID = int(max_sp) + n
            n += 1

            start = connector[0][6]
            start_left   = connector[0][7]
            start_top    = connector[0][8]
            start_width  = connector[0][9]
            start_height = connector[0][10]

            logger.debug("StartID : %s[%s]" % (start, connector[0][2]))
            logger.debug("    l:%d,t:%d,w:%d,h:%d)" %(start_left, start_top, start_width, start_height))

            end = connector[1][6]
            end_left   = connector[1][7]
            end_top    = connector[1][8]
            end_width  = connector[1][9]
            end_height = connector[1][10]

            logger.debug("EndID : %s[%s]" % (end, connector[1][2]))
            logger.debug("    l:%d,t:%d,w:%d,h:%d)" %(end_left, end_top, end_width, end_height))

            sxml_id = int(start)
            start_idx = int(start) + 1
            exml_id = int(end)
            end_idx  = int(end + 1)

            cxn_x = start_left
            cxn_y = start_top

            cxn_cx = end_left
            cxn_cy = end_top

            connectionShape = etree.SubElement(root, "{http://schemas.openxmlformats.org/presentationml/2006/main}cxnSp", nsmap=self.namespacesPPTX)

            nonVisualConnectorShapeDrawingProperties = etree.Element("{http://schemas.openxmlformats.org/presentationml/2006/main}nvCxnSpPr")
            cNonVisualProperties = etree.SubElement(nonVisualConnectorShapeDrawingProperties, "{http://schemas.openxmlformats.org/presentationml/2006/main}cNvPr")
            cNonVisualProperties.set("id", str(connectorID + 1))
            cNonVisualProperties.set("name", "Straight Arrow Connector "  + str(connectorID))
            cNonVisualConnectorShapeDrawingProperties = etree.SubElement(nonVisualConnectorShapeDrawingProperties, "{http://schemas.openxmlformats.org/presentationml/2006/main}cNvCxnSpPr")
            etree.SubElement(nonVisualConnectorShapeDrawingProperties, "{http://schemas.openxmlformats.org/presentationml/2006/main}nvPr")

            connectionStart = etree.SubElement(cNonVisualConnectorShapeDrawingProperties, "{http://schemas.openxmlformats.org/drawingml/2006/main}stCxn")
            connectionStart.set("id", str(sxml_id))    # shape index from which connector starts (param)
            connectionStart.set("idx", str(start_idx)) # connector spawn point index
            connectionEnd = etree.SubElement(cNonVisualConnectorShapeDrawingProperties, "{http://schemas.openxmlformats.org/drawingml/2006/main}endCxn")
            connectionEnd.set("id", str(exml_id))      # shape index at which connector ends (param)
            connectionEnd.set("idx", str(end_idx))     # connector termination point index

            shapeProperties = etree.SubElement(connectionShape, "{http://schemas.openxmlformats.org/presentationml/2006/main}spPr")
            twodTransform = etree.SubElement(shapeProperties, "{http://schemas.openxmlformats.org/drawingml/2006/main}xfrm")

            twodTransform.set("flipH", "1")

            # location of bounding box (params)
            offset = etree.SubElement(twodTransform, "{http://schemas.openxmlformats.org/drawingml/2006/main}off")
            offset.set("x", str(cxn_x).replace(".0", ""))
            offset.set("y", str(cxn_y).replace(".0", ""))

            # height and width of bounding box (params)
            extents = etree.SubElement(twodTransform, "{http://schemas.openxmlformats.org/drawingml/2006/main}ext")
            extents.set("cx", str(cxn_cx).replace(".0", ""))
            extents.set("cy", str(cxn_cy).replace(".0", ""))

            presetGeometry = etree.SubElement(shapeProperties, "{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom")
            presetGeometry.set("prst", "line")
            etree.SubElement(presetGeometry, "{http://schemas.openxmlformats.org/drawingml/2006/main}avLst")

            style = etree.SubElement(connectionShape, "{http://schemas.openxmlformats.org/presentationml/2006/main}style")

            lineReference = etree.SubElement(style, "{http://schemas.openxmlformats.org/drawingml/2006/main}lnRef")
            lineReference.set("idx", "1")
            schemeColor = etree.SubElement(lineReference, "{http://schemas.openxmlformats.org/drawingml/2006/main}schemeClr")
            schemeColor.set("val", "dk1")

            fillReference = etree.SubElement(style, "{http://schemas.openxmlformats.org/drawingml/2006/main}fillRef")
            fillReference.set("idx", "0")
            schemeColor = etree.SubElement(fillReference, "{http://schemas.openxmlformats.org/drawingml/2006/main}schemeClr")
            schemeColor.set("val", "dk1")

            effectReference = etree.SubElement(style, "{http://schemas.openxmlformats.org/drawingml/2006/main}effectRef")
            effectReference.set("idx", "0")
            schemeColor = etree.SubElement(effectReference, "{http://schemas.openxmlformats.org/drawingml/2006/main}schemeClr")
            schemeColor.set("val", "dk1")

            fontReference = etree.SubElement(style, "{http://schemas.openxmlformats.org/drawingml/2006/main}fontRef")
            fontReference.set("idx", "minor")
            schemeColor = etree.SubElement(fontReference, "{http://schemas.openxmlformats.org/drawingml/2006/main}schemeClr")
            schemeColor.set("val", "tx1")


        # write out the final tree
        f = open(os.path.join("./tmp", timestamp, "ppt", "slides", "slide1.xml"), "w")
        tree.write(f, encoding="UTF-8", xml_declaration=True)
        f.close()

        # zip the file
        zip_file = zipfile.ZipFile(self.PPTXFilename, "w", zipfile.ZIP_DEFLATED)
        os.chdir(os.path.join("./tmp", timestamp))
        for root, dirs, files in os.walk("."):
            for file in files:
                zip_file.write(os.path.join(root, file))
        zip_file.close

    def buildPPTX(self):

        title_only_slide_layout = self.prs.slide_layouts[self.TITLE_ONLY_SLIDE_LAYOUT]

        slide = self.prs.slides.add_slide(title_only_slide_layout)
        shapes = slide.shapes

        timeTxt = time.strftime("%Y%d%m_%H%M%S")
        shapes.title.text = "Built on %s" % (timeTxt)

        listModels = list()
        listConnectors = list()

        # From Archimate File
        createPPTX.getAll(listModels)

        #
        # Iterate through all Archimate Diagrams
        #
        logger.info("====Add Archimate Diagrams====")
        max_sp = 0

        for x in listModels:
            #
            # Since you must know the shape_id for each corresponding Diagram Object, make them first
            #
            listDO = list()
            logger.info("%s[%s]" % (x[0].get("name"), x[0].get("id")))

            slideName = str(x[0].get("name"))
            ls = list()
            ls.append("Slide Title")
            ls.append(slideName)
            listDO.append(ls)

            p = "//element[@id=\"%s\"]" % (x[0].get("id"))
            r = createPPTX.tree.xpath(p, namespaces=NS_MAP)
            xc = r[0].getchildren()

            for y in xc:
                child = str(y.get("archimateElement"))
                logger.debug("  %s[%s]: entity:%s" % (y.get(ARCHI_TYPE), y.get("id"), child))

                n = createPPTX.findNode(child)

                if n == None or isinstance(n, list):
                    continue

                shapeName = n.get("name").encode('ascii',errors='ignore')
                logger.debug("  DO = %s" % (shapeName))

                z = y.getchildren()
                for w in z:
                    logger.debug("    %s[%s]" % (w.get(ARCHI_TYPE), w.get("id")))

                    if w.get(ARCHI_TYPE) == "archimate:Connection":
                        logger.debug("      source=%s, target=%s, relationship=%s" % (w.get("source"), w.get("target"), w.get("relationship")))

                        ls = list()
                        ls.append("Connector")
                        ls.append(str(w.get("source")))
                        ls.append(str(w.get("target")))

                        relation = w.get("relationship")
                        rn = createPPTX.findNode(relation)
                        logger.debug("      relation : %s[%s]" % (rn.get("name"), rn.get(ARCHI_TYPE)))
                        if rn.get("name") != None:
                            ls.append(str(rn.get("name")))

                        listDO.append(ls)

                        sn = createPPTX.findNode(w.get("source"), tag="child")
                        logger.debug("  SO = %s" % sn.get("name"))

                        st = createPPTX.findNode(w.get("target"), tag="child")
                        logger.debug("  TO = %s" % st.get("name"))

                    elif w.get("x") != None:
                        logger.debug("    x=%s, y=%s" % (w.get("x"), w.get("y")))
                        ls = list()
                        ls.append(str(y.get(ARCHI_TYPE)))
                        ls.append(str(n.get(ARCHI_TYPE)))
                        ls.append(shapeName)
                        ls.append(str(y.get("id")))
                        ls.append(str(w.get("x")))
                        ls.append(str(w.get("y")))
                        listDO.append(ls)

            #
            # Now iterate the the diagram objects and add shapes to Slide
            # plus grab the shape_id!
            #
            logger.debug("====Add Slide====")
            for model in listDO:
                if model[0] == "Slide Title":
                    #
                    # New Slide
                    #
                    slide_layout = self.prs.slide_layouts[self.TITLE_ONLY_SLIDE_LAYOUT]
                    slide = self.prs.slides.add_slide(slide_layout)
                    shapes = slide.shapes

                    shapes.title.text = "%s" % (model[1])

                    logger.debug("model : %s" % model[1])

                elif model[0] == "archimate:DiagramObject":
                    logger.debug("%s" % model)
                    name = model[2]
                    x, y = createPPTX.project(model[4], model[5])

                    if x == None or y == None:
                        continue

                    left   = Inches(x)
                    top    = Inches(y)

                    width  = Inches(1.0 * createPPTX.SCALE)
                    height = Inches(0.75 * createPPTX.SCALE)

                    logger.debug("DiagramObject : %s(%s,%s)" % (model[2], model[4], model[5]))
                    logger.debug("    l:%d,t:%d,w:%d,h:%d)" %(left, top, width, height))
                    logger.debug("    Point (%d:%d)" % (left, top))

                    shape = shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)

                    # capture shape id!
                    model.append(shape.id)
                    model.append(left)
                    model.append(top)
                    model.append(width)
                    model.append(height)

                    logger.debug("shape.id : %s" % shape.id)

                    text_frame = shape.text_frame
                    text_frame.clear()
                    p = text_frame.paragraphs[0]
                    run = p.add_run()
                    run.text = name

                    font = run.font
                    font.name = "Calibri"
                    font.size = Pt(10 * createPPTX.SCALE)
                    font.color.rgb = RGBColor(50, 50, 50) # grey

                    # set shape fill
                    fill = shape.fill
                    fill.solid()
                    fill.fore_color.rgb = RGBColor(204, 224, 255)

                elif model[0] == "Connector":
                    logger.debug("  model[0] %s, model[1] %s" % (model[1], model[2]))

                    source = createPPTX.findDiagramObject(listDO, model[1])
                    target = createPPTX.findDiagramObject(listDO, model[2])

                    logger.debug("  source %s" % (source))
                    logger.debug("  target %s" % (target))

                    ll = list()
                    ll.append(source)
                    ll.append(target)
                    listConnectors.append(ll)

        # save file
        logger.info("\n Saved %s" % self.filePPTXOut)
        self.prs.save(self.filePPTXOut)

        return self.prs

        #
        # Add Connectors
        #
        # logger.debug("====Add Connectors====")
        # fixSlides(PPTXFilename, listConnectors)


if __name__ == "__main__":

    start_time = ArchiLib.startTimer()

    afileArchimate = ""
    afilePPTXIn    = "test_in.pptx"
    afilePPTXOut   = "test_out.pptx"

    createPPTX = ArchiCreatePPTX(afileArchimate, afilePPTXIn, afilePPTXOut)

    createPPTX.buildPPTX()

    ArchiLib.stopTimer(start_time)


