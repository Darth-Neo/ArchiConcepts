import sys
import os
import StringIO
import glob, time, math, zipfile
from nl_lib import Logger
logger = Logger.setupLogging(__name__)
from nl_lib.Constants import *
from nl_lib.Concepts import Concepts
from lxml import etree
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.util import Pt
import import_artifacts as ia

SCALE=0.90

def project(x, y, scale=SCALE):
    try:
        x = (((float(x) / 100.0)) * scale)
        y = (((float(y) / 100.0)) * scale)
        return x, y
    except:
        return None, None

if __name__ == "__main__":
    pass

def fixSlides(PPTXFilename, listSlides):

    # unzip .pptx to temporary space and remove file
    timestamp = str(time.time()).replace(".", "")
    zip_file = zipfile.ZipFile(PPTXFilename, "r")
    zip_file.extractall(os.path.join("./tmp", timestamp))
    zip_file.close

    os.remove(PPTXFilename)

    # register necessary namespaces
    etree.register_namespace("a", "http://schemas.openxmlformats.org/drawingml/2006/main")
    etree.register_namespace("p", "http://schemas.openxmlformats.org/presentationml/2006/main")
    etree.register_namespace("r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships")

    # parse xml document and find shape tree
    tree = etree.parse(os.path.join("./tmp", timestamp, "ppt", "slides", "slide1.xml"))
    root = tree.getroot()

    n = 1

    shapeTree = slide.spTree

    logger.info("shapeTree - %d" % (len(shapeTree)))

    st = shapeTree.xml

    logger.debug("ST %s" % st)

    tree = etree.fromstring(st)

    xp = "//@id"
    for sp in tree.xpath(xp):
        if int(sp) > max_sp:
            max_sp = int(sp)
        logger.debug("sp : %s" % (sp))

    # register necessary namespaces
    etree.register_namespace("a", "http://schemas.openxmlformats.org/drawingml/2006/main")
    etree.register_namespace("p", "http://schemas.openxmlformats.org/presentationml/2006/main")
    etree.register_namespace("r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships")
    namespaces = namespacesPPTX

    n = 1
    for connector in listConnectors[:1]:

        connectorID = int(max_sp) + n
        n += 1

        start = connector[0][6]
        start_left   = connector[0][7]
        start_top    = connector[0][8]
        start_width  = connector[0][9]
        start_height = connector[0][10]

        logger.info("StartID : %s[%s]" % (start, connector[0][2]))
        logger.info("    l:%d,t:%d,w:%d,h:%d)" %(start_left, start_top, start_width, start_height))

        end = connector[1][6]
        end_left   = connector[1][7]
        end_top    = connector[1][8]
        end_width  = connector[1][9]
        end_height = connector[1][10]

        logger.info("EndID : %s[%s]" % (end, connector[1][2]))
        logger.info("    l:%d,t:%d,w:%d,h:%d)" %(end_left, end_top, end_width, end_height))


        sxml_id = int(start)
        start_idx = int(start) + 1
        exml_id = int(end)
        end_idx  = int(end + 1)

        cxn_x = start_left
        cxn_y = start_top

        cxn_cx = end_left
        cxn_cy = end_top

        connectionShape = etree.SubElement(shapeTree, "{http://schemas.openxmlformats.org/presentationml/2006/main}cxnSp", nsmap=namespaces)

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
    zip_file = zipfile.ZipFile(PPTXFilename, "w", zipfile.ZIP_DEFLATED)
    os.chdir(os.path.join("/tmp", timestamp))
    for root, dirs, files in os.walk("."):
        for file in files:
            zip_file.write(os.path.join(root, file))
    zip_file.close
