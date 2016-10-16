#!/usr/bin/env python

import os

from Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)

if __name__ == u"__main__":
    path = u"/Users/morrj140/Documents/SolutionEngineering/Kronos/As-Is To-Be Archimate"
    os.chdir(path)

    elements = dict()
    output = list()

    strip_strings = "\"\'\n\r"

    #  0    1      2      3
    # "ID","Type","Name","Documentation"
    with open(u"SETV4elements.csv", u"r") as f:
        try:
            n = 0
            rl = f.readline()
            while rl:
                element = rl.split(",")

                logger.debug(u"%d Element Length = %d" % (n, len(element)))
                id = element[0].strip(strip_strings)
                type = element[1].strip(strip_strings)
                name = element[2].strip(strip_strings)
                logger.info(u"{0} {1} {2} (3)".format(n, id, name, type))
                elements[id] = [name, type]
                n += 1

                rl = f.readline()

        except EOFError, msg:
            logger.warn(u"%s")

    #  0    1      2      3               4        5
    # "ID","Type","Name","Documentation","Source","Target"
    with open(u"SETV4relations.csv", u"r") as f:
        try:
            n = 0
            rl = f.readline()
            while rl:
                if n == 0:
                    rl = f.readline()
                    n += 1
                    continue

                relation = rl.split(",")
                logger.info(u"{}".format(relation))

                id = relation[0]
                type = relation[1].strip(strip_strings)
                name = relation[2].strip(strip_strings)
                documentation = relation[3].strip(strip_strings)

                source_id = relation[4].strip(strip_strings)
                target_id = relation[5].strip(strip_strings)

                logger.debug("{}".format(source_id))
                logger.debug("{}".format(target_id))

                sl = elements[source_id]
                sourceName = sl[0]
                sourceType = sl[1]

                tl = elements[target_id]
                targetName = tl[0]
                targetType = tl[1]

                l = [type, name, sourceName, sourceType, targetName, targetType]

                logger.info(u"{0} {1} {2} (3)".format(n, sourceName, targetName, type))
                output.append(l)

                rl = f.readline()
                n += 1

        except Exception, msg:
            logger.warn(u"%s" % msg)

    for relation in output:
        logger.info(u"%s" % relation)