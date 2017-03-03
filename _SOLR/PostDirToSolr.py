#!/usr/bin/python
#
# Jython Shell
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

import os
import sys
from subprocess import call

def runCMD(startDir):
    #bin/post -c gettingstarted ~/Documents/SolutionEngineering/DVC/*.*

    command = u"/Users/morrj140/Development/src/solr-5.2.1/solr/bin/post"
    p1 = u"-c"
    p2 = u"Kronos"

    cmd = [u"%s %s %s %s" % (command, p1, p2, startDir),]

    call(cmd, shell=True)

if __name__ == u"__main__":

    option = sys.argv[0]

    startDir = u"/Users/morrj140/Documents/SolutionEngineering/PMIS/RelevantDocs"

    runCMD(startDir)