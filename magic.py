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

    for model in listSlides:
        logger.info("start %s[%s]" % (model[0][2], model[0][6]))
        logger.info("end   %s[%s]" % (model[1][2], model[1][6]))

        start_idx = model[0][6]
        sxml_idx = start_idx + 1
        end_idx = model[1][6]
        exml_idx = start_idx + 1

        cxn_x, cxn_y = project(model[0][4], model[0][5])
        cxn_cx, cxn_cy = project(model[1][4], model[1][5])

        #cxn_x = start_construct.left + OVAL_WIDTH
        #cxn_y = start_construct.top + HALF_OVAL_HEIGHT
        #cxn_cx = end_construct.left - start_construct.left - OVAL_WIDTH
        #cxn_cy = end_construct.top - start_construct.top

        # get necessary elements
        iterator = root.iter("{http://schemas.openxmlformats.org/presentationml/2006/main}spTree")
        shapeTree = iterator.next()

        #iterator = root.iter("{http://schemas.openxmlformats.org/presentationml/2006/main}grpSpPr")
        #groupShapeProperties = iterator.next()

        # add properties
        # twodTransform = etree.SubElement(groupShapeProperties, "a:xfrm")
        #offset = etree.SubElement(twodTransform, "a:off")
        #offset.set("x", "0")
        #offset.set("y", "0")
        #extents = etree.SubElement(twodTransform, "a:ext")
        #extents.set("cx", "0")
        #extents.set("cy", "0")
        #childOffset = etree.SubElement(twodTransform, "a:chOff")
        #childOffset.set("x", "0")
        #childOffset.set("y", "0")
        #childExtents = etree.SubElement(twodTransform, "a:chExt")
        #childExtents.set("cx", "0")
        #childExtents.set("cy", "0")

        connectionShape = etree.SubElement(shapeTree, "p:cxnSp")
        nonVisualConnectorShapeDrawingProperties = etree.SubElement(connectionShape, "p:nvCxnSpPr")
        cNonVisualProperties = etree.SubElement(nonVisualConnectorShapeDrawingProperties, "p:cNvPr")
        cNonVisualProperties.set("id", str(sxml_idx))
        cNonVisualProperties.set("name", "Connector " + str(sxml_idx))
        cNonVisualConnectorShapeDrawingProperties = etree.SubElement(nonVisualConnectorShapeDrawingProperties, "p:cNvCxnSpPr")
        etree.SubElement(nonVisualConnectorShapeDrawingProperties, "p:nvPr")

        connectionStart = etree.SubElement(cNonVisualConnectorShapeDrawingProperties, "a:stCxn")
        connectionStart.set("id", str(sxml_idx))    # shape index from which connector starts (param)
        connectionStart.set("idx", start_idx)       # connector spawn point index
        connectionEnd = etree.SubElement(cNonVisualConnectorShapeDrawingProperties, "a:endCxn")
        connectionEnd.set("id", str(exml_idx))      # shape index at which connector ends (param)
        connectionEnd.set("idx", end_idx)           # connector termination point index

        shapeProperties = etree.SubElement(connectionShape, "p:spPr")
        twodTransform = etree.SubElement(shapeProperties, "a:xfrm")

        twodTransform.set("flipH", "1")

        # location of bounding box (params)
        offset = etree.SubElement(twodTransform, "a:off")
        offset.set("x", str(cxn_x).replace(".0", ""))
        offset.set("y", str(cxn_y).replace(".0", ""))

        # height and width of bounding box (params)
        extents = etree.SubElement(twodTransform, "a:ext")
        extents.set("cx", str(cxn_cx).replace(".0", ""))
        extents.set("cy", str(cxn_cy).replace(".0", ""))

        presetGeometry = etree.SubElement(shapeProperties, "a:prstGeom")
        presetGeometry.set("prst", "line")
        etree.SubElement(presetGeometry, "a:avLst")

        style = etree.SubElement(connectionShape, "p:style")

        lineReference = etree.SubElement(style, "a:lnRef")
        lineReference.set("idx", "1")
        schemeColor = etree.SubElement(lineReference, "a:schemeClr")
        schemeColor.set("val", "dk1")

        fillReference = etree.SubElement(style, "a:fillRef")
        fillReference.set("idx", "0")
        schemeColor = etree.SubElement(fillReference, "a:schemeClr")
        schemeColor.set("val", "dk1")

        effectReference = etree.SubElement(style, "a:effectRef")
        effectReference.set("idx", "0")
        schemeColor = etree.SubElement(effectReference, "a:schemeClr")
        schemeColor.set("val", "dk1")

        fontReference = etree.SubElement(style, "a:fontRef")
        fontReference.set("idx", "minor")
        schemeColor = etree.SubElement(fontReference, "a:schemeClr")
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
