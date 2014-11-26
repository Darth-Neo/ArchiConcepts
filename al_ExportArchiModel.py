__author__ = 'morrj140'
#!/usr/bin/python
#
# Archimate to Dependancy Analysis
#
import sys
import os
import StringIO
import time
from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'archimate': 'http://www.archimatetool.com/archimate'}

XML_NS         =  "http://www.w3.org/2001/XMLSchema-instance"
ARCHIMATE_NS   =  "http://www.archimatetool.com/archimate"
NS_MAP = {"xsi": XML_NS, "archimate" : ARCHIMATE_NS}

ARCHI_TYPE = "{http://www.w3.org/2001/XMLSchema-instance}type"

def getChildName(tree, id):

    xp = "//child[@id='%s']" % str(id)

    logger.debug("xp : %s" % xp)

    se = tree.xpath(xp)

    if len(se) > 0:
        ae = se[0].get("archimateElement")
        return getElementName(tree, ae)

def getElementName(tree, id):

    xp = "//element[@id='%s']" % str(id)

    logger.debug("xp : %s" % xp)

    se = tree.xpath(xp)

    if len(se) > 0:
        return se[0], se[0].get("name")
    else:
        return None, None


if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v4.archimate"
    fileExport = "export.csv"

    p, fname = os.path.split(fileArchimate)
    logger.info("Using : %s" % fileArchimate)
    etree.QName(ARCHIMATE_NS, 'model')
    tree = etree.parse(fileArchimate)

    f = open(fileExport,'w')
    f.write("Source, Relationship, Target\n")

    ModelToExport = "Systems - ToBe"

    concepts = Concepts(ModelToExport, "Model")

    se = tree.xpath("//element[@name='%s']" % (ModelToExport))
    logger.info("%s:%s" % (se[0].tag, se[0].get("name")))
    r = se[0].getchildren()

    for x in r:
        xid = x.get("id")
        xi = x.items()

        xc, xname = getElementName(tree, x.get("archimateElement"))

        se = tree.xpath("//child[@id='%s']" % (xid))
        nc  = se[0].getchildren()

        logger.debug("%s" % xi)
        logger.info("%s:%s[%s]" % (x.tag, xname, x.tag))

        c = concepts.addConceptKeyType(xname, "Source")
        f.write("%s,,\n" % (xname))

        for y in nc:
            yid = y.get("id")
            yi = y.items()

            if y.tag == "sourceConnection":
                sid = y.get("source")
                s, sname = getChildName(tree, sid)
                tid = y.get("target")
                t, tname = getChildName(tree, tid)

                relid = y.get("relationship")
                rel, relname = getElementName(tree, relid)

                if relname == None:
                    relname = "Target"

                c.addConceptKeyType(tname, relname)

                logger.debug("    %s" % yi)
                logger.info("     %s-%s-%s" % (sname,  relname, tname))

                f.write("%s,%s,%s\n" % (sname, relname, tname))


    Concepts.saveConcepts(concepts, ModelToExport+".p")

    f.close()