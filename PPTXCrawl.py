__author__ = 'morrj140'

import logging
from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import PatternGraph, NetworkXGraph, Neo4JGraph
from nl_lib.Constants import *

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from pptx import Presentation
from lxml import etree

# Constants
EMU = 914400.0

gdb = "http://localhost:7474/db/data/"
#gdb = "http://10.92.82.60:7574/db/data/"


def addGraphNodes(graph, concepts, n=0):
    n += 1
    for c in concepts.getConcepts().values():
        logger.debug("%d : %d Node c : %s:%s" % (n, len(c.getConcepts()), c.name, c.typeName))
        graph.addConcept(c)
        if len(c.getConcepts()) != 0:
            addGraphNodes(graph, c, n)

def addGraphEdges(graph, concepts, n=0):
    n += 1
    i = 1
    for c in concepts.getConcepts().values():
        logger.debug("%d : %d Edge c : %s:%s" % (n, len(c.getConcepts()), c.name, c.typeName))
        if i == 1:
            p = c
            i += 1
        else:
            graph.addEdge(p, c)
        if len(c.getConcepts()) != 0:
            addGraphEdges(graph, c, n)

def graphConcepts(concepts, graph=None):

    if graph == None:
        #graph = Neo4JGraph(gdb)

        #logger.info("Clear the Graph @" + gdb)
        #graph.clearGraphDB()

        graph = NetworkXGraph()
        #graph = PatternGraph()

    logger.info("Adding nodes the graph ...")
    addGraphNodes(graph, concepts)
    logger.info("Adding edges the graph ...")
    addGraphEdges(graph, concepts)

    if isinstance(graph, Neo4JGraph):
        graph.setNodeLabels()

    if isinstance(graph, NetworkXGraph):
        graph.drawGraph("concepts.png")
        filename = "concepts.net"
        logger.info("Saving Graph - %s" % filename)
        graph.saveGraphPajek(filename)
        graph.saveGraph("concepts.gml")
        logger.info("Saving Graph - %s" % "concepts.gml")

    if isinstance(graph, PatternGraph):
        logger.info("Exporting Graph")
        graph.exportGraph()

def findID(nid, dictNodes):

    for x in dictNodes.keys():
        logger.debug("    dictNodes[%s] : %s" % (dictNodes[x], x))

        if nid in dictNodes[x]:
            logger.debug("Found %s in %s" % (x, dictNodes[x]))
            return x

    return None

def logList(l, n=0):

    n += 1
    s = " " * n

    logger.info("%sn=%d" % (s, n))

    for x in l:
        #logger.info("%sx=%s" % (s, x))
        if isinstance(x, list):
            logger.info("%slist: %s" % (s, x))
            logList(x, n)
        elif isinstance(x, tuple):
            logger.info("%stuple: %s" % (s, x))
            logList(x, n)
        else:
            if isinstance(x, str):
                logger.info("%sstr: %s" % (s, x))
            elif isinstance(x, float):
                logger.info("%sfloat: %3.2f" % (s, x))
            elif isinstance(x, int):
                logger.info("%sint: %d" % (s, x))

def checkConnect(c, dictEdges, dictNodes):

    for el in dictEdges.keys():
            tel =  dictEdges[el]

            logger.debug("Edges %s[%s]" % (el, tel))

            for y in tel:
                logger.debug("  y: %s[%s]" % (y, type(y)))

                if len(y) == 3:
                    source = findID(y[1], dictNodes)
                    target = findID(y[2], dictNodes)

                    if source != None and target != None:
                        logger.debug("%s : %s" % (source, target))

                        if len(source) == 0 or len(target) == 0:
                            continue

                        d = c.addConceptKeyType(source, "Source")
                        d.addConceptKeyType(target, "Target")


def crawlPPTX(c, path_to_presentation):
    dictNodes = dict()
    dictEdges = dict()

    prs = Presentation(path_to_presentation)

    for slide in prs.slides:
        logger.debug ("--new slide--")
        logger.debug("\n%s" % slide.partname)
        logger.debug("slide : %s" % slide)

        for idx, ph in enumerate(slide.shapes.placeholders):
            logger.debug ("**    %s:%s    **" % (idx,ph))

        n = 0
        for shape in slide.shapes:
            logger.debug ("...%s..." % type(shape))

            n += 1

            logger.debug("shape.element.xml : %s" % shape.element.xml)
            logger.debug("shape.name : %s[%d]" % (shape.name,  shape.id - 1))

            if shape.name[:5] in ("Title"):
                if shape.has_text_frame:
                    text_frame = shape.text_frame

                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                            logger.debug("%s" % run.text)

            sn = shape.name

            # skip "Text "
            if shape.name[:5] in ("Recta", "Elbow", "Round", "Strai"):

                t = shape.top / EMU
                l = shape.left / EMU
                h = shape.height / EMU
                w = shape.width / EMU

                logger.debug("shape.top     : %3.2f" % (t))
                logger.debug("shape.left    : %3.2f" % (l))
                logger.debug("shape.height  : %3.2f" % (h))
                logger.debug("shape.width   : %3.2f" % (w))
                logger.debug("shape.shape_type    : %s" % shape.shape_type)

                tl = (l, t)
                tr = (l + w, t)
                bl = (l, t + h)
                br = (l + w, t + h)

                name = ""

                if shape.has_text_frame:
                    text_frame = shape.text_frame

                    for paragraph in shape.text_frame.paragraphs:
                        for run in paragraph.runs:
                            logger.debug("%s" % run.text)
                            name = name + run.text + " "

                nid = shape.id - 1

                logger.debug("name : %s[%d] - %s" % (name, nid, shape.name))

                if len(name) > 0 and dictNodes.has_key(name):
                    nl = dictNodes[name]
                    nl.append(nid)
                    logger.debug("Duplicate Keys %s...%s" % (name, dictNodes[name]))
                else:
                    nl = list()
                    nl.append(nid)
                    dictNodes[name] = nl

                #
                # Add in Connections
                #
                if sn.find("Connector") != -1:
                    logger.debug("Found Connector")

                    xmlShape = shape.element.xml

                    #logger.info("Check for connections...: %s" % xmlShape)

                    tree = etree.fromstring(xmlShape)

                    xl = tree.xpath("//@id")

                    nxl = list()
                    for x in xl:
                        nxl.append(int(x))
                        logger.debug ("%d:%s" % (nid,x))

                    if dictEdges.has_key(nid):
                        nl = dictEdges[nid]
                        nl.append(nxl)
                        logger.debug("Duplicate Edges %s...%s" % (name, dictEdges[nid]))
                    else:
                        el = list()
                        el.append(nxl)
                        dictEdges[nid] = el

                    #logger.debug ("--new shape [%d]--" % n)
                    logger.debug("  %s" % (name))
                    logger.debug("    tl = %3.2f, %3.2f -- tr %3.2f, %3.2f" % (tl[0], tl[1], tr[0], tr[1]))
                    logger.debug("    bl = %3.2f, %3.2f -- br %3.2f, %3.2f" % (bl[0], bl[1], br[0], br[1]))

        # at this point you need to make connections
        checkConnect(c, dictEdges, dictNodes)


if __name__ == "__main__":
    #graph = NetworkXGraph()

    #path_to_presentation = "/Users/morrj140/PycharmProjects/ArchiConcepts/example2.pptx"
    #path_to_presentation = "/Users/morrj140/PycharmProjects/ArchiConcepts/ARP-TBX - High Level Solution_Draft_v9.pptx"
    path_to_presentation = "/Users/morrj140/PycharmProjects/ArchiConcepts/ARP-TBX - High Level Solution_Draft_v10a.pptx"

    c = Concepts("Application", "Relations")

    crawlPPTX(c, path_to_presentation)

    c.logConcepts()

    Concepts.saveConcepts(c, "pptx.p")


