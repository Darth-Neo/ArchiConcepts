__author__ = u'morrj140'

from setuptools import setup, find_packages
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

setup(name=u'al_Archilib',
      version=u'0.1',
      description=u'Tools for Processing Archimate Models',
      url=u'http://github.com/darth-neo/ArchiConcepts',
      author=u'Darth Neo',
      author_email=u'morrisspid.james@gmail.com',
      license=u'MIT',
      packages=[u'al_ArchiLib'],
      zip_safe=False,

      classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        u'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        u'Intended Audience :: Developers',
        u'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        u'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        u'Programming Language :: Python :: 2',
        u'Programming Language :: Python :: 2.6',
        u'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords=u'Archimate XML Models Processing',

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed.
    install_requires = [u'nltk', u'networkx', u'py2neo', u'lxml', u'openpyxl', u'pygraphviz', u'python-pptx', u'python-docx'],)


