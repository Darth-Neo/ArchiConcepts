__author__ = 'morrj140'

from setuptools import setup, find_packages
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

setup(name='al_Archilib',
      version='0.1',
      description='Tools for Processing Archimate Models',
      url='http://github.com/darth-neo/ArchiConcepts',
      author='Darth Neo',
      author_email='morrisspid.james@gmail.com',
      license='MIT',
      packages=['al_ArchiLib'],
      zip_safe=False,

      classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='Archimate XML Models Processing',

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed.
    install_requires = ['nltk', 'networkx', 'py2neo', 'lxml', 'openpyxl', 'pygraphviz', 'python-pptx', 'python-docx'],)


