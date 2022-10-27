"""
Tests for the elp2000 functions.
"""

from unittest import TestCase

from astronomia.calendar import (
    cal_to_day_of_year,
    cal_to_jd,
    day_of_year_to_cal,
    jd_to_cal,
    jd_to_day_of_week,
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

    def test_dow(self):
        jd = cal_to_jd(1954, 6, 30.0)
        self.assertEqual(jd, 2434923.5)
        dow = jd_to_day_of_week(jd)
        self.assertEqual(dow, 3)

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

    def test_ecl_to_equ(self):
        ra, dec = ecl_to_equ(d_to_r(113.215630), d_to_r(6.684170), d_to_r(23.4392911))
        self.assertAlmostEqual(r_to_d(ra), 116.328942, places=5)
        self.assertAlmostEqual(r_to_d(dec), 28.026183, places=6)
