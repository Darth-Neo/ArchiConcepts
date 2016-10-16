#!/usr/bin/python
#
# Print python site-packages information
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

import site

if __name__ == u"__main__":

    usp = site.getusersitepackages()

    print(u"User Site Packages : %s" % usp)


    for x in usp:
        print(u"Site Packages      : %s" % x)
