#!/usr/bin/env python

__author__ = u'morrj140'
import os
from Logger import *
logger = setupLogging(__name__)
logger.setLevel(DEBUG)

import xlrd

CellTypes = [u"Empty", u"Text", u"Number", u"Date", u"Boolean", u"Error", u"Blank"]

def getXLSText(filename):
        logger.info(u"filename: %s" % filename)

        wsl = list()

        workbook = xlrd.open_workbook(filename)

        for worksheet_name in workbook.sheet_names():

            logger.debug(u"Worksheet-%s" % worksheet_name)

            worksheet = workbook.sheet_by_name(worksheet_name)

            # Needed due to cell retrieval
            num_rows = worksheet.nrows - 1
            curr_row = -1

            while curr_row < num_rows:
                curr_row += 1
                row = worksheet.row(curr_row)

                cl = list()
                for column in row:
                    rc = unicode(column.value).encode(u"utf-8", errors=u"ignore")
                    rc = rc.decode(u"ascii", errors=u"ignore")
                    cl.append(rc)

                nl = list()
                nl.append(worksheet_name)
                nl.append(cl)
                wsl.append(nl)

        return wsl

if __name__ == u'__main__':

    # filename = u"/Users/morrj140/Documents/SolutionEngineering/DVC/Revenue Recognition/Tylana/2015 Automate JE workplan_JMM.xlsx"

    filename = u"/Users/morrj140/Documents/SolutionEngineering/Standard Deliverables/Master MetaEntity Lists/ElementsPlus.xlsx"

    text = getXLSText(filename)

    outputFile = u".%sElementsPlus2.csv" % os.sep

    logger.info(u"Outputing to: %s" % outputFile)

    with open(outputFile, u"w") as f:
        for x in text:
            output = ""
            for y in x:

                if isinstance(y, str) or isinstance(y, unicode):
                    output += u"\"%s\"," % (y)

                elif isinstance(y, list) or isinstance(y, tuple):
                    for v in y:
                        output += u"\"%s\"," % (v)

                f.write("%s%s" % (output[:-1], os.linesep))