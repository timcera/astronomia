'''
Tests for the elp2000 functions.
'''

from unittest import TestCase

from astronomia.calendar import cal_to_jd
from astronomia.dynamical import deltaT_seconds

class TestDynamical(TestCase):
    def test_deltat(self):
        jd = cal_to_jd(1977, 1, 18)
        secs = deltaT_seconds(jd)
        self.assertAlmostEqual(secs, 48, places=0)

