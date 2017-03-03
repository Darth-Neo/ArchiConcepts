#!/usr/bin/env python
import os
import sys

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)

elementsFile = "K43elements.csv"
relationsFile = "K43relations.csv"
propertiesFile = "K43properties.csv"

de = dict()

def load_elements(debug=False):

    elements = dict()
    headers = None

    #
    # Elements
    # 0   1     2     3
    # ID, Type, Name, Documentation
    #
    with open(elementsFile, "rb") as f:
        el = f.readlines()

    for m, x in enumerate(el):

        if m == 0:
            headers = x.split(",")
            headers = [x.strip("\" ") for x in headers]
            continue

        nx = x.split(",")
        id = nx[0].strip("\"\r\n\'")
        type = nx[1].strip("\"\r\n\'")
        name = nx[2].strip("\"\r\n\'")
        documentation = nx[3].strip("\"\r\n\'")

        elements[id] = list([name, type])

        if debug is True:
            for n, y in enumerate(x.split(",")):
                spaces = " " * n
                logger.debug("{}.{} - {} {}".format(m, n, spaces, y))

    return headers, elements


def load_relations(nedl, debug=False):

    relations = dict()

    #
    # Relations
    # 0   1     2     3              4       5 6 7
    # ID, Type, Name, Documentation, Source, , , Target
    #
    with open(relationsFile, "rb") as f:
        rl = f.readlines()

    rn = rl[0].split("\r")

    for m, x in enumerate(rn):
        logger.debug("{}".format(x))

        if m == 0:
            headers = x.split(",")
            continue
        try:
            ln = x.split(",")
            id = ln[0]
            type = ln[1]
            name = ln[2]

            source = ln[4]
            source_type = nedl[source][1]
            name_source = nedl[source][0]

            target = ln[7]
            target_type = nedl[target][1]
            name_target = nedl[target][0]

            if type == "UsedByRelationship":
                logger.debug("%s : %s" % (source, target))
                relations[id] = list([type, name, name_source, source_type, name_target, target_type])

        except Exception, msg:
            logger.error("{}".format(msg))

        if debug is True:
            for n, y in enumerate(x.split(",")[1:]):
                spaces = " " * n
                logger.debug("{}.{} - {} {}".format(m, n, spaces, y))

    return relations


if __name__ == "__main__":

    ehl, edl = load_elements()

    logger.debug("Finished elements")

    rdl = load_relations(edl)

    logger.debug("Finished relations")

    with open("Output.csv", "wb") as f:

        for m, x in rdl.items():
            relation_id = m
            relation_type = x[0]
            relation_name = x[1]
            source_name = x[2]
            target_name = x[4]

            output = "{}, {}, {}, {}".format(source_name, relation_name, target_name, os.linesep)
            f.write(output)
            logger.info(output)
