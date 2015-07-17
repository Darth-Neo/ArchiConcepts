#!/usr/bin/env python

__author__ = u'morrj140'
import os
from nl_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

import xlrd

def getXLSText(filename):
        logger.info(u"filename: %s" % filename)

        wsl = list()

        workbook = xlrd.open_workbook(filename)

        # sheet = "Specific Requirements"
        # worksheet = workbook.sheet_by_name(sheet)
        # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank

        CellTypes = [u"Empty", u"Text", u"Number", u"Date", u"Boolean", u"Error", u"Blank"]

        for worksheet_name in workbook.sheet_names():
            logger.debug(u"Worksheet-%s" % worksheet_name)
            worksheet = workbook.sheet_by_name(worksheet_name)
            num_rows = worksheet.nrows - 1
            num_cells = worksheet.ncols - 1
            curr_row = -1

            while curr_row < num_rows:
                curr_row += 1
                row = worksheet.row(curr_row)

                rv0 = unicode(row[0].value).encode(u"utf-8", errors=u"ignore")
                rv0 = rv0.decode(u"ascii", errors=u"ignore")

                rv2 = unicode(row[2].value).encode(u"utf-8", errors=u"ignore")
                rv2 = rv2.decode(u"ascii", errors=u"ignore")

                if len(rv0) > 1:
                    logger.info(u"%s-%s-%s" % (worksheet_name, rv0, rv2))

                    nl = list()
                    nl.append(worksheet_name)
                    nl.append(rv0)
                    nl.append(rv2)
                    wsl.append(nl)

        return wsl

if __name__ == u'__main__':
    filename = u"/Users/morrj140/Documents/SolutionEngineering/DVC/Revenue Recognition/Tylana/2015 Automate JE workplan_JMM.xlsx"
    text = getXLSText(filename)

    with open(u"journalEntries.csv", "w") as f:
        f.write("DataObject,Property.Description,Property.value%s" % os.linesep)
        for x in text:
            if not(len(x[2]) > 0):
                x[2] = u"NA"

            f.write("\"%s\",\"%s\",\"%s\"%s" % (x[0], x[1], x[2], os.linesep))