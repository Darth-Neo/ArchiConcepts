#! /usr/bin/python
#
# Estimate Scope_Items Export
#
__author__ = 'morrj140'
import datetime
import logging
from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.Constants import *

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.compat import range
from openpyxl.cell import get_column_letter
from openpyxl.worksheet import Worksheet as worksheet

def exportExcel(fileIn, fileOut):

    wb = load_workbook(filename = fileIn)

    ws = wb.create_sheet()

    ws.title = "Scope Items"
    ws['F5'] = 3.14

    for col_idx in range(1, 20):

        logger.info("col_idx : %d" % col_idx)

        col = get_column_letter(col_idx)

        logger.info("Col : %d" % col_idx)

        for row in range(1, 10):

            rc = '%s%s'%(col, row)

            logger.info("row : %s\tRow,Col : %s" % (row, rc))

            ws.cell(rc).value = '%s%s' % (col, row)

    wb.save(filename = fileOut)

if __name__ == "__main__":
    fileIn = 'Template_Estimate.xlsx'
    fileOut = 'Template_Estimate_new.xlsx'

    exportExcel(fileIn, fileOut)