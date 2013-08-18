from setuptools import setup, find_packages
import os.path

setup(name='astronomia',
      version=open("VERSION").readline().strip(),
      description="Library for calculation of ephemeris and other astronomical calculations",
      long_description="""\
              Library of astronomical calculations
              based on Astrolabe, by Bill McClain.""",
      classifiers=['Environment :: Console',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Topic :: Scientific/Engineering :: Astronomy',
                   ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='ephemeris astronomy',
      author='Tim Cera, P.E.',
      author_email='tim@cerazone.net',
      url='http://timcera.bitbucket.org',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          ],
      scripts=['apps/solstice.py', 'apps/check_perihelion.py',
          'apps/cronus.py', 'apps/easter-cgi.py', 'apps/solstice-cgi.py'],
      data_files=[(os.path.join('share', 'astronomia'), ['apps/astronomia_params.txt'])],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
