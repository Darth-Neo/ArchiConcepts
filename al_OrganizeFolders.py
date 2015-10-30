#!/usr/bin/python
#
#  Concepts to Archimate Elements
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_Constants import *

from al_lib.ArchiLib import ArchiLib
from nl_lib.Concepts import Concepts

dn = dict()

def Add(k):
    if k in dn:
        dn[k] += 1
    else:
        dn[k] = 1

def organizeFolders(fileArchimate):

    logger.info(u"Using : %s" % fileArchimate)

    al = ArchiLib(fileArchimate)

    for folder in entityFolders:
        pass

    sl = al.logTypeCounts()

    nl = [(x[10:], y) for x, y in sl]

    n = 0
    for k, v in al.dictNodes.items():
        logger.debug(u"%s" % v)

        n += 1

        try:
            af = v[ARCHI_TYPE][10:]

        except KeyError, msg:
            continue

        if af in entityFolders:
            logger.debug(u"%d - %s - %s : %s" % (n, v[NAME], af, entityFolders[af]))
            Add(af)
        else:
            logger.info(u"%d Missing - %s" % (n, af))

        if False:
            # Create Subfolder
            folder = u"Implementation & Migration"
            subfolder = u"Dependancy Analysis - %s" % time.strftime(u"%Y%d%m_%H%M%S")

            attrib = dict()
            attrib[u"id"] = al.getID()
            attrib[u"name"] = subfolder
            al.insertNode(u"folder", folder, attrib)

    sum = 0
    for k, v in dn.items():
        count = [y for x, y in nl if k == x][0]
        logger.info(u"%s - %d - %d" % (k, v, count))
        sum += v

    logger.info(u"%d Records" % sum)

if __name__ == u"__main__":
    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/Accounting Engine v5.archimate"
    organizeFolders(fileArchimate)
