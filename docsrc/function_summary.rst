
Function Summary
================

.. currentmodule:: astronomia

Calendar Functions
------------------
.. autosummary::

   calendar.cal_to_jd
   calendar.cal_to_jde
   calendar.cal_to_day_of_year
   calendar.day_of_year_to_cal
   calendar.easter
   calendar.is_dst
   calendar.is_leap_year
   calendar.jd_to_cal
   calendar.jd_to_day_of_week
   calendar.jd_to_jcent
   calendar.lt_to_str
   calendar.sidereal_time_greenwich
   calendar.ut_to_lt

Dynamical Functions
-------------------
.. autosummary::

   dynamical.deltaT_seconds
   dynamical.dt_to_ut

ELP Functions
-------------
.. autosummary::

   elp2000.ELP2000.mean_longitude_ascending_node
   elp2000.ELP2000.mean_longitude_perigee
   elp2000.ELP2000.mean_longitude
   elp2000.ELP2000.dimension3
   elp2000.ELP2000.dimension

Equinox Functions
-----------------
.. autosummary::

   equinox.equinox_approx
   equinox.equinox

Nutation Functions
------------------
.. autosummary::

   nutation.nut_in_lon
   nutation.nut_in_obl
   nutation.obliquity
   nutation.obliquity_hi

Rise/Set Functions
------------------
.. autosummary::

   riseset.rise
   riseset.settime
   riseset.transit
   riseset.moon_rst_altitude

Sun Functions
-------------
.. autosummary::

   sun.Sun.mean_longitude
   sun.Sun.mean_longitude_perigee
   sun.Sun.dimension
   sun.Sun.dimension3
   sun.longitude_radius_low
   sun.apparent_longitude_low
   sun.aberration_low

Utility Functions
-----------------
.. autosummary::

   util.d_to_dms
   util.d_to_r
   util.diff_angle
   util.dms_to_d
   util.ecl_to_equ
   util.equ_to_horiz
   util.equ_to_ecl
   util.fday_to_hms
   util.hms_to_fday
   util.interpolate3
   util.interpolate_angle3
   util.load_params
   util.modpi2
   util.polynomial
   util.r_to_d

VSOP86d Functions
-----------------
.. autosummary::

   vsop87d.VSOP87d.dimension
   vsop87d.VSOP87d.dimension3
   vsop87d.vsop_to_fk5
   vsop87d.geocentric_planet
   vsop87d.load_vsop87d_text_db

