from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='astronomia',
      version=version,
      description="Libray for calculation of ephemeris and other astronomical calculations",
      long_description="""\
              Library of astronomical calculations
              heavily based on Astrolabe, by Bill McClain,
              Astrolabe is no longer available - at least I
              couldn't find it.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='ephemeris astronomy',
      author='Tim Cera, P.E.',
      author_email='tim@cerazone.net',
      url='',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          ],
      scripts=['apps/check_equinox.py', 'apps/create_text_vsop_db.py',
               'apps/solstice.py', 'apps/check_perihelion.py',
               'apps/cronus.py', 'apps/time_vsop_db_loads.py',
               'apps/check_vsop87d.py', 'apps/easter-cgi.py',
               'apps/validate_meeus.py', 'apps/create_binary_vsop_db.py',
               'apps/solstice-cgi.py'],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
