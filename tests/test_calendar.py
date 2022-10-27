"""
Tests for the elp2000 functions.
"""

import math
from unittest import TestCase

import numpy as np

from astronomia.calendar import (
    cal_to_day_of_year,
    cal_to_jd,
    cal_to_jde,
    day_of_year_to_cal,
    easter,
    fday_to_hms,
    frac_yr_to_jd,
    is_leap_year,
    jd_to_cal,
    jd_to_day_of_week,
    sidereal_time_greenwich,
    yr_frac_mon_to_jd,
)
from astronomia.coordinates import ecl_to_equ
from astronomia.util import d_to_r, r_to_d


class TestUtil(TestCase):
    def test_cal_to_jd(self):
        jd = cal_to_jd(1957, 10, 4.81)
        self.assertAlmostEqual(jd, 2436116.31, places=6)

        jd = cal_to_jd(333, 1, 27.5, False)
        self.assertAlmostEqual(jd, 1842713.0, places=6)

        jd0 = cal_to_jd(1910, 4, 20.0)
        jd1 = cal_to_jd(1986, 2, 9.0)
        self.assertEqual(jd1 - jd0, 27689)

        jd = cal_to_jd(1991, 7, 11)
        jd = jd + 10000
        yr, mo, day = jd_to_cal(jd)
        self.assertEqual(yr, 2018)
        self.assertEqual(mo, 11)
        self.assertEqual(day, 26)

        jd = frac_yr_to_jd([1991 + 1.0 / 365.0, 1991])
        self.assertEqual(jd[0] - jd[1], 1.0)
        jd = frac_yr_to_jd([1991.5, 1991])
        self.assertEqual(jd[0] - jd[1], 182.5)

        jd = yr_frac_mon_to_jd(1991, [1.5, 1])
        self.assertEqual(jd[0] - jd[1], 15.5)

        self.assertRaises(ValueError, cal_to_jd, 1991, 13)
        self.assertRaises(ValueError, cal_to_jd, 1991, 12, 32)
        self.assertRaises(ValueError, cal_to_jd, 1991.1, 12.1)

    def test_fday_to_hms(self):
        self.assertEqual(fday_to_hms(0.5), (12, 0, 0))
        self.assertEqual(fday_to_hms(0.5006944444444444445), (12, 1, 0))
        self.assertEqual(
            fday_to_hms(0.5006944444444444445 + 0.0007060185185185186), (12, 2, 1)
        )

    def test_dow(self):
        jd = cal_to_jd(1954, 6, 30.0)
        self.assertEqual(jd, 2434923.5)
        dow = jd_to_day_of_week(jd)
        self.assertEqual(dow, 3)

    def test_sidereal(self):
        N = sidereal_time_greenwich(cal_to_jd(2004, 1, 1))
        testval = (6 * 3600 + 39 * 60 + 58.60298794778828) / 43200 * math.pi
        np.testing.assert_array_almost_equal(N, testval, decimal=4)
        N = sidereal_time_greenwich(cal_to_jd(2004, 1, [1, 2]))
        testval1 = (6 * 3600 + 43 * 60 + 55.15832794114431) / 43200 * math.pi
        np.testing.assert_array_almost_equal(N, [testval, testval1], decimal=4)

    def test_doy(self):
        N = cal_to_day_of_year(1978, 11, 14)
        self.assertEqual(N, 318)

        N = cal_to_day_of_year(1988, 4, 22)
        self.assertEqual(N, 113)

    def test_doy_to_cal(self):
        mo, day = day_of_year_to_cal(1978, 318)
        self.assertEqual(mo, 11)
        self.assertEqual(day, 14)

    def test_jd_to_cal(self):
        yr, mo, day = jd_to_cal(2436116.31)

        self.assertEqual(yr, 1957)
        self.assertEqual(mo, 10)
        self.assertAlmostEqual(day, 4.81)

        yr, mo, day = jd_to_cal(1842713.0, False)

        self.assertEqual(yr, 333)
        self.assertEqual(mo, 1)
        self.assertAlmostEqual(day, 27.5)

        yr, mo, day = jd_to_cal(1507900.13, False)

        self.assertEqual(yr, -584)
        self.assertEqual(mo, 5)
        self.assertAlmostEqual(day, 28.63)

    def test_jd_to_cal_array(self):
        yr, mo, day = jd_to_cal([1842713.0, 1507900.13], False)

        np.testing.assert_array_equal(yr, [333, -584])
        np.testing.assert_array_equal(mo, [1, 5])
        np.testing.assert_array_almost_equal(day, [27.5, 28.63])

    def test_ecl_to_equ(self):
        ra, dec = ecl_to_equ(d_to_r(113.215630), d_to_r(6.684170), d_to_r(23.4392911))
        self.assertAlmostEqual(r_to_d(ra), 116.328942, places=5)
        self.assertAlmostEqual(r_to_d(dec), 28.026183, places=6)

    def test_easter(self):
        tbl = (
            (1991, 3, 31),
            (1992, 4, 19),
            (1993, 4, 11),
            (1954, 4, 18),
            (2000, 4, 23),
            (1818, 3, 22),
        )

        for yr, mo, day in tbl:
            xmo, xday = easter(yr)
            self.assertEqual(xmo, mo)
            self.assertEqual(xday, day)

        for yr in [179, 711, 1243]:
            mo, day = easter(yr, False)
            self.assertEqual(mo, 4)
            self.assertEqual(day, 12)

    def test_cal_to_jde(self):
        tbl = [
            [(2013, 6, 18, 18, 25, 30), 2456462.267708],
            [(2013, 6, 18, 18, 26, 30), 2456462.268403],
        ]
        for date, testval in tbl:
            jd = cal_to_jde(*date)
            np.testing.assert_array_almost_equal(jd, testval, decimal=6)

    def test_is_leap_year(self):
        self.assertEqual(is_leap_year(2004), True)
        self.assertEqual(is_leap_year(2004, gregorian=False), True)
