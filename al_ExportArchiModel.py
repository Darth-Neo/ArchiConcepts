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


from al_ArchiLib import *

from lxml import etree

def getModel(ModelToExport, concepts, f, tree):

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
        logger.info("%s[%s]" % (xname, x.tag))

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
                logger.info("%s,%s,%s,%s,%s,%s\n" % (ModelToExport, sname, s.get(ARCHI_TYPE), relname, tname, t.get(ARCHI_TYPE)))

                f.write("%s,%s,%s,%s,%s,%s\n" % (ModelToExport, sname, s.get(ARCHI_TYPE), relname, tname, t.get(ARCHI_TYPE)))

    return concepts

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v15.archimate"
    fileExport = "export.csv"

    p, fname = os.path.split(fileArchimate)
    logger.info("Using : %s" % fileArchimate)
    etree.QName(ARCHIMATE_NS, 'model')

    tree = etree.parse(fileArchimate)

    f = open(fileExport,'w')
    f.write("Model, Source, Type, Relationship, Target, Type\n")

    listMTE = list()
    #listMTE.append("5. Contract Management")
    #listMTE.append("4. Contract Prep")
    #listMTE.append("1. Inventory Management")
    #listMTE.append("1. Resort Setup")
    #listMTE.append("4. Proposal Presentation")
    #listMTE.append("5. Contract Presentation")
    #listMTE.append("6. Contract Closing")

    #listMTE.append("All Scenarios")
    #listMTE.append("Business Concepts")
    listMTE.append("System of Record")

    concepts = Concepts("Export", "Model")

    for ModelToExport in listMTE:
        getModel(ModelToExport, concepts, f, tree)

    Concepts.saveConcepts(concepts, "Estimation.p")

    f.close()
    logger.info("Save Model : %s" % fileExport)