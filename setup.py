# -*- coding: utf-8 -*-

import os
import sys

from setuptools import find_packages, setup

pkg_name = "astronomia"

version = open("VERSION").readline().strip()

if sys.argv[-1] == "publish":
    os.system("cleanpy .")
    os.system("python setup.py sdist")
    os.system("twine upload dist/{pkg_name}-{version}.tar.gz".format(**locals()))
    sys.exit()

README = open("README.rst").read()

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    "tstoolbox > 103.16.1",
]

extras_require = {
    "dev": [
        "black",
        "cleanpy",
        "twine",
        "pytest",
        "coverage",
        "flake8",
        "pytest-cov",
        "pytest-mpl",
        "pre-commit",
        "black-nbconvert",
        "blacken-docs",
        "velin",
        "isort",
        "pyroma",
        "pyupgrade",
        "commitizen",
    ]
}

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
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords="ephemeris astronomy",
    author="Tim Cera, P.E.",
    author_email="tim@cerazone.net",
    url="http://timcera.bitbucket.io/{pkg_name}/docs/index.html".format(**locals()),
    license="BSD",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"SciencePlots": ["*.mplstyle"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        "console_scripts": ["{pkg_name}={pkg_name}.{pkg_name}:main".format(**locals())]
    },
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
    python_requires=">=3.7.1",
)
