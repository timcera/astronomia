#! /usr/bin/env python
"""
    Astrolabe copyright 2000, 2001 William McClain
    Astrolabe forked to Astronomia 2013
    Astronomia copyright 2013

    This file is part of Astronomia.

    Astronomia is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Astronomia is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Astronomia; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

Create a text version of the VSOP87d database.

Usage:

    ./create_text_vsop_db.py > vsop87d.txt   # or whatever path/file.

IMPORTANT: A text version of the database is provided with the Astronomia
package. You need to run this program ONLY if for some reason you want
to recreate that file.

This program does not use any routines from the Astronomia package. Run
it from a directory containing these files:

    VSOP87D.ear
    VSOP87D.jup
    VSOP87D.mar
    VSOP87D.mer
    VSOP87D.nep
    VSOP87D.sat
    VSOP87D.ura
    VSOP87D.ven

...which have been fetched from the ftp directory referenced at:

    http://cdsweb.u-strasbg.fr/cgi-bin/Cat?VI/81

The program will read each file, select the data required and combine all
of them into a format expected by the Astronomia vsop87d module.

Results are written to standard output; redirect them into a file in your
data directory and enter that path/file name into the astronomia_params.txt
file as the value of "vsop87d_text_path".

"""


import string

#
# Here are file format notes from the original VSOP distribution.
#

# HEADER RECORD
# =============
# Specifications :
# - iv : code of VSOP87 version               integer     i1  col.18
# - bo : name of body                         character   a7  col.23-29
# - ic : index of coordinate                  integer     i1  col.42
# - it : degree alpha of time variable T      integer     i1  col.60
# - in : number of terms of series            integer     i7  col.61-67
#
# The code iv of the version is :
# iv = 4 for the version VSOP87D
#
# The names of the bodies are :
# MERCURY, VENUS, EARTH, MARS, JUPITER, SATURN, URANUS, NEPTUNE, SUN,
# and EMB for the Earth-Moon Barycenter.
#
# The index ic of the coordinates are :
# - for the spherical coordinates (versions B,D) :
#  1 : Longitude
#  2 : Latitude
#  3 : Radius
#
# The degree alpha of the time variable is equal to :
# 0 for periodic series, 1 to 5 for Poisson series.

# TERM RECORD
# ===========
# Specifications :
# iv : code of VSOP87 version                 integer     i1  col.02
# ic : index of coordinate                    integer     i1  col.04
# it : degree alpha of time variable T        integer     i1  col.05
# n  : rank of the term in a serie            integer     i5  col.06-10
# A  : amplitude A                            real dp f18.11  col.80-97
# B  : phase     B                            real dp f14.11  col.98-111
# C  : frequency C                            read dp f20.11  col.112-131


planets = (
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
)
coords = ("L", "B", "R")

# each planet file...
for planet in planets:
    f = file(f"VSOP87D.{planet[:3].lower()}")
    while s := f.readline():
        if s[17] != "4":
            raise AssertionError
        if (s[22:29]).rstrip() != planet.upper():
            raise AssertionError
        ic = int(s[41])  # coord type
        it = int(s[59])  # time degree
        nt = int(s[60:67])  # number of terms
        print(planet, coords[ic - 1], it, nt)
        # term records
        for _ in range(nt):
            s = f.readline()
            if s[1] != "4":
                raise AssertionError
            ict = int(s[3])  # coord type
            if ict != ic:
                raise AssertionError
            itt = int(s[4])  # time degree
            if itt != it:
                raise AssertionError
            A = string.strip(s[79:97])
            B = string.strip(s[97:111])
            C = string.strip(s[111:131])
            print(A, B, C)
    f.close()
#
# that's all
#
