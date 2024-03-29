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

Compare the loading time of text and binary VSOp87d databases.

Usage:

    ./time_vsop_db_loads.py

Result: the binary version is only slightly faster than the text
version. Later: after modifying load_vsop87d_text_db() to use
one readlines() call instead of many readline() calls, the
text and binary times are about the same.

"""

import time

from astronomia.util import load_params
from astronomia.vsop87d import load_vsop87d_text_db

load_params()

print("reading text database...")
t0 = time.time()
load_vsop87d_text_db()
print(time.time() - t0, "seconds")
