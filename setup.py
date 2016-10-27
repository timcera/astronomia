#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py upload_docs')
    sys.exit()

readme = open('README.rst').read()

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'mando >= 0.4',
    'tstoolbox',
]

setup(name='astronomia',
      version=open("VERSION").readline().strip(),
      description="Library for calculation of ephemeris and other astronomical calculations",
      long_description=readme + '\n\n',
      classifiers=['Environment :: Console',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: Scientific/Engineering :: Astronomy',
                   ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='ephemeris astronomy',
      author='Tim Cera, P.E.',
      author_email='tim@cerazone.net',
      url='http://timcera.bitbucket.org/astronomia/docsrc/index.html',
      license='GPL2',
      packages=['astronomia'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      scripts=['apps/solstice.py', 'apps/check_perihelion.py',
          'apps/cronus.py', 'apps/easter-cgi.py', 'apps/solstice-cgi.py'],
      data_files=[(os.path.join('share', 'astronomia'), ['apps/astronomia_params.txt'])],
      entry_points={
          'console_scripts':
              ['astronomia=astronomia.astronomia:main']
      },
      test_suite='tests',
      )
