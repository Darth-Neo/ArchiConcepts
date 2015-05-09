#!/usr/bin/python
#
# Print python site-packages information
#
__author__ = u'morrj140'
__VERSION__ = u'0.3'

import site

if __name__ == u"__main__":

    print(u"User Site Packages : %s" % site.getusersitepackages())
    for x in site.getsitepackages():
        print(u"Site Packages      : %s" % x)
