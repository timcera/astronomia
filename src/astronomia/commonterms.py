"""Copyright 2000, 2001 Astrolabe by William McClain.

Forked in 2013 to Astronomia

Copyright 2013 Astronomia by Tim Cera

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

Useful constants terms.

Don't change these unless you are moving to a new universe.
"""

from .util import d_to_r

#
# Constant terms.
#
kL1 = (
    d_to_r(218.3164477),
    d_to_r(481267.88123421),
    d_to_r(-0.0015786),
    d_to_r(1.0 / 538841),
    d_to_r(-1.0 / 65194000),
)
kD = (
    d_to_r(297.8501921),
    d_to_r(445267.1114034),
    d_to_r(-0.0018819),
    d_to_r(1.0 / 545868),
    d_to_r(-1.0 / 113065000),
)
kM = (
    d_to_r(357.5291092),
    d_to_r(35999.0502909),
    d_to_r(-0.0001536),
    d_to_r(1.0 / 24490000),
)
kM1 = (
    d_to_r(134.9633964),
    d_to_r(477198.8675055),
    d_to_r(0.0087414),
    d_to_r(1.0 / 69699),
    d_to_r(-1.0 / 14712000),
)
kF = (
    d_to_r(93.2720950),
    d_to_r(483202.0175233),
    d_to_r(-0.0036539),
    d_to_r(-1.0 / 3526000),
    d_to_r(1.0 / 863310000),
)
ko = (
    d_to_r(125.0445479),
    d_to_r(-1934.1362891),
    d_to_r(0.0020754),
    d_to_r(1.0 / 467441.0),
    d_to_r(1.0 / 60616000.0),
)
