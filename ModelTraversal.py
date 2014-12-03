#!/usr/bin/python
#
# Archimate Model to Concepts
#
import sys
import os
import StringIO
import time
import logging

from nl_lib import Logger
logger = Logger.setupLogging(__name__)
import logging

logger.setLevel(logging.INFO)

from nl_lib.Constants import *
from nl_lib.Concepts import Concepts

from lxml import etree

import al_ArchiLib as al

def cvsConcepts(c, f):

    pc = c.getConcepts()

    for p in pc.values():
        if p.typeName in ("ID", "archimate:BusinessObject"):
            continue
        elif p.typeName in ("archimate:BusinessEvent"):
            n = 1
        elif p.typeName in ("archimate:BusinessProcess"):
            n = 2
        else:
            n = 3

        commas = "," * n

        text = "%s%s" % (commas, p.name)
        logger.info("%s" % text)

        f.write(text + "\n")

        cvsConcepts(p, f)

def recurseBusinesNodea(tree, childID, c, n = 0):
    n += 1

    spaces = " " * n

    sr = al.findRelationsByID(tree, childID)

    logger.debug("len %d" % (len(sr)))

    d = None

    for x in sr:
        logger.debug("%s%s" % (spaces, x.get(al.ARCHI_TYPE)[10:]))

        # find everything I point to
        if x.get("source") == childID:
            id = targetID = x.get("target")
            zs = al.findElementByID(tree, id)[0]

            if zs.get(al.ARCHI_TYPE) in ("archimate:BusinessEvent"):
                logger.debug("%sSource %d:%s[%s]" % (spaces, n, zs.get("name"), zs.get(al.ARCHI_TYPE)))
                d = c.addConceptKeyType(zs.get("name"), zs.get(al.ARCHI_TYPE))
                #d.addConceptKeyType(zs.get("id"), "ID")

                recurseBusinesNodea(tree, zs.get("id"), d, n)

            if zs.get(al.ARCHI_TYPE) in ("archimate:BusinessProcess"):
                logger.debug("%sSource %d:%s[%s]" % (spaces, n, zs.get("name"), zs.get(al.ARCHI_TYPE)))
                d = c.addConceptKeyType(zs.get("name"), zs.get(al.ARCHI_TYPE))
                #d.addConceptKeyType(zs.get("id"), "ID")

                recurseBusinesNodea(tree, zs.get("id"), d, n)

        # find everything pointing to me
        elif x.get("target") == childID:
            id = sourceID = x.get("source")
            zt = al.findElementByID(tree, id)[0]

            if zt.get(al.ARCHI_TYPE) in ("archimate:BusinessObject"):
                logger.debug("%s%s" % (spaces, zt.get(al.ARCHI_TYPE)[10:]))
                e = c.addConceptKeyType(zt.get("name"), zt.get(al.ARCHI_TYPE))
                #d.addConceptKeyType(zt.get("id"), "ID")

            elif zt.get(al.ARCHI_TYPE) in ("archimate:ApplicationComponet", "archimate:ApplicationData"):
                logger.debug("%s%s" % (spaces, zt.get(al.ARCHI_TYPE)[10:]))
                e = c.addConceptKeyType(zt.get("name"), zt.get(al.ARCHI_TYPE))
                #d.addConceptKeyType(zt.get("id"), "ID")

            elif zt.get(al.ARCHI_TYPE) in ("archimate:ApplicationService"):
                logger.debug("%s%s" % (spaces, zt.get(al.ARCHI_TYPE)[10:]))
                e = c.addConceptKeyType(zt.get("name"), zt.get(al.ARCHI_TYPE))
                #d.addConceptKeyType(zt.get("id"), "ID")

    logger.debug("%s%d---end---" % (spaces, n))

if __name__ == "__main__":
    fileArchimate = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v10.archimate"
    fileOut="estimate_" + time.strftime("%Y%d%m_%H%M%S") +" .csv"

    p, fname = os.path.split(fileArchimate)
    logger.info("Using : %s" % fname)

    etree.QName(al.ARCHIMATE_NS, 'model')
    tree = etree.parse(fileArchimate)

    nameModel = "All Scenarios"

    concepts = Concepts(nameModel, "Model")

    model = al.findDiagramModelByName(tree, nameModel)

    children = model.getchildren()

    for x in children:

        childID = x.get("archimateElement")
        z = al.findElementByID(tree, childID)[0]

        c = concepts.addConceptKeyType(z.get("name"), z.get(al.ARCHI_TYPE))
        c.addConceptKeyType(z.get("id"), "ID")

        logger.info("%s[%s]" % (z.get("name"), z.get(al.ARCHI_TYPE)))

        recurseBusinesNodea(tree, childID, c)

    #concepts.logConcepts()

    f = open(fileOut,'w')
    cvsConcepts(concepts, f)
    f.close()

    logger.info("Saved CSV to %s" % fileOut)

    Concepts.saveConcepts(concepts, "report.p")
    logger.info("Saved Concepts to %s" % "report.p")

