#!/usr/bin/python
#
# service to caml case to Concepts
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib

def splitWords(s):
    sl = list()

    ns = u""

    for c in s:

        logger.debug(u"%s" % c)

        if c.isupper():

            logger.debug(u"%s%s" % (ns, os.linesep))
            sl.append(ns)
            ns = u"%s" % (c)
        else:
            ns = u"%s%s" % (ns, c)

    sl.append(ns)

    logger.debug(u"%s" % u", ".join([x for x in sl]))

    return sl



if __name__ == u"__main__":

    s = u"testOfTheEmergencyBroadcastSystem"

    sl = splitWords(s)

    logger.info(u"%s" % u", ".join([x for x in sl]))
