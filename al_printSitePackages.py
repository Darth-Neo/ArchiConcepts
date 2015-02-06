#!/usr/bin/python
#
# Print python site-packages information
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import site
import os
import logging

from nl_lib import Logger

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)


if __name__ == "__main__":

    logger.info("User Site Packages : %s" % site.getusersitepackages())
    logger.info("Site Packages      : %s" % site.getsitepackages())
