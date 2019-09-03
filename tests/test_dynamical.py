"""
Tests for the elp2000 functions.
"""

from unittest import TestCase

import numpy as np

from astronomia.calendar import cal_to_jd
from astronomia.dynamical import deltaT_seconds


class TestDynamical(TestCase):
    def test_deltat(self):
        for jd, testsec in [
            (cal_to_jd(1977, 1, 18), 47.5),
            (cal_to_jd(2012, 12), 66.8),
            (cal_to_jd(-600), 18635.4),
            (cal_to_jd(-499), 17106.9),
            (cal_to_jd(-400), 15458.5),
            (cal_to_jd(-300), 14011.8),
            (cal_to_jd(-200), 12731.5),
            (cal_to_jd(-100), 11582.4),
            (cal_to_jd(0), 10533.7),
            (cal_to_jd(100), 9551.9),
            (cal_to_jd(200), 8600.4),
            (cal_to_jd(300), 7645.2),
            (cal_to_jd(400), 6667.5),
            (cal_to_jd(500), 5682.2),
            (cal_to_jd(600), 4715.1),
            (cal_to_jd(700), 3792.4),
            (cal_to_jd(800), 2938.1),
            (cal_to_jd(900), 2185.6),
            (cal_to_jd(1000), 1562.1),
            (cal_to_jd(1100), 1079.2),
            (cal_to_jd(1200), 728.9),
            (cal_to_jd(1300), 486.2),
            (cal_to_jd(1400), 317.7),
            (cal_to_jd(1500), 195.6),
            (cal_to_jd(1600), 118.3),
            (cal_to_jd(1700), 21.0),
            (cal_to_jd(1750), 13.7),
            (cal_to_jd(1800), 12.6),
            (cal_to_jd(1850), 6.5),
            (cal_to_jd(1900), -2.7),
            (cal_to_jd(2012, 9), 66.7),
            (cal_to_jd(2012, 10), 66.8),
            (cal_to_jd(2013, 1), 67.1),
            (cal_to_jd(2014, 12), 68.9),
            (cal_to_jd(2015, 1), 68.9),
            (cal_to_jd(2016, 1), 69.4),
            (cal_to_jd(2050, 1), 92.9),
            (cal_to_jd(2051, 1), 95.0),
            (cal_to_jd(2150, 1), 328.0),
            (cal_to_jd(2151, 1), 330.1),
            (cal_to_jd(1950), 29.1),
        ]:
            secs = deltaT_seconds(jd)
            np.testing.assert_array_almost_equal(secs, testsec, decimal=1)
