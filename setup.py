#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup

pkg_name = "astronomia"

version = open("VERSION").readline().strip()

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist")
    os.system("twine upload dist/{pkg_name}-{version}.tar.gz".format(**locals()))
    sys.exit()

README = open("README.rst").read()

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    "tstoolbox",
]

setup(
    name=pkg_name,
    version=version,
    description="Library for calculation of ephemeris and other astronomical calculations",
    long_description=README,
    classifiers=[
        # Get strings from
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords="ephemeris astronomy",
    author="Tim Cera, P.E.",
    author_email="tim@cerazone.net",
    url="http://timcera.bitbucket.io/astronomia/docsrc/index.html",
    license="GPL2",
    packages=["astronomia"],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={"console_scripts": ["astronomia=astronomia.astronomia:main"]},
    scripts=[
        "apps/solstice.py",
        "apps/check_perihelion.py",
        "apps/cronus.py",
        "apps/easter-cgi.py",
        "apps/solstice-cgi.py",
    ],
    data_files=[
        (
            os.path.join("share", "astronomia"),
            [os.path.join("apps", "astronomia_params.txt")],
        )
    ],
    test_suite="tests",
    python_requires=">=3.6",
)
