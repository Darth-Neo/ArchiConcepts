#!/usr/bin/python
#
# Print python site-packages information
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

import site

if __name__ == "__main__":

    print("User Site Packages : %s" % site.getusersitepackages())
    for x in site.getsitepackages():
        print("Site Packages      : %s" % x)
