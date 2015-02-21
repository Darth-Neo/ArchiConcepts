#!/usr/bin/python
#
# XML Merging for Two Archimate XML to One.
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import sys
import os
import StringIO
import csv
import random

from nl_lib import Logger
logger = Logger.setupLogging(__name__)

from xml.etree import ElementTree as et

from al_ArchiLib.ArchiLib import ArchiLib

class XMLCombiner(object):
    def __init__(self, filenames):
        assert len(filenames) > 0, 'No filenames!'

        et.register_namespace('archimate', ArchiLib.ARCHIMATE_NS)

        # save all the roots, in order, to be processed later
        self.roots = [et.parse(f).getroot() for f in filenames]

    def combine(self):
        for r in self.roots[1:]:
            # combine each element with the first one, and update that
            self.combine_element(self.roots[0], r)

        # return the string representation
        return et.tostring(self.roots[0])

    def combine_element(self, one, other):
        """
        This function recursively updates either the text or the children
        of an element if another element is found in `one`, or adds it
        from `other` if not found.
        """
        # Create a mapping from tag name to element, as that's what we are fltering with
        mapping = {el.tag: el for el in one}
        for el in other:
            if len(el) == 0:
                # Not nested
                try:
                    # Update the text
                    mapping[el.tag].text = el.text
                except KeyError:
                    # An element with this name is not in the mapping
                    mapping[el.tag] = el
                    # Add it
                    one.append(el)
            else:
                try:
                    # Recursively process the element, and update it in the same way
                    self.combine_element(mapping[el.tag], el)
                except KeyError:
                    # Not in the mapping
                    mapping[el.tag] = el
                    # Just add it
                    one.append(el)

def outputXML(tree, filename="Merge_artifacts.archimate"):
    f = open(filename,'w')
    f.write(tree)
    f.close()

if __name__ == '__main__':

    dir = "/Users/morrj140/Documents/SolutionEngineering/Archimate Models"

    file1 = dir + os.sep + "Accovia Replacement.archimate"
    file2 = dir + os.sep + "DNX Phase 2 0.9.archimate"
    file3 = dir + os.sep + "CodeGen_v2.archimate"

    r = XMLCombiner((file1, file2, file3)).combine()
    print '-'*20
    print r
    outputXML(r)