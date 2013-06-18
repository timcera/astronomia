'''
Tests for the elp2000 functions.
'''

from unittest import TestCase

from astronomia.constants import days_per_second
from astronomia.equinox import equinox_approx, equinox
from astronomia.calendar import cal_to_jd, hms_to_fday

class TestEquinox(TestCase):
    def test_equinox(self):
        jd = equinox_approx(1962, 'summer')
        self.assertAlmostEqual(jd, 2437837.39245, places=5)

        jd = equinox(2437837.38589, 'summer', days_per_second)
        self.assertAlmostEqual(jd, cal_to_jd(1962, 6, 21) +
                hms_to_fday(21, 24, 42), places=5)

        tbl = [
                (1996,
                    (("spring", 20, hms_to_fday( 8,  4,  7)),
                    ("summer",  21, hms_to_fday( 2, 24, 46)),
                    ("autumn",  22, hms_to_fday(18,  1,  8)),
                    ("winter",  21, hms_to_fday(14,  6, 56)))),
                (1997,
                    (("spring", 20, hms_to_fday(13, 55, 42)),
                    ("summer",  21, hms_to_fday( 8, 20, 59)),
                    ("autumn",  22, hms_to_fday(23, 56, 49)),
                    ("winter",  21, hms_to_fday(20,  8,  5)))),
                (1998,
                    (("spring", 20, hms_to_fday(19, 55, 35)),
                    ("summer",  21, hms_to_fday(14,  3, 38)),
                    ("autumn",  23, hms_to_fday( 5, 38, 15)),
                    ("winter",  22, hms_to_fday( 1, 57, 31)))),
                (1999,
                    (("spring", 21, hms_to_fday( 1, 46, 53)),
                    ("summer",  21, hms_to_fday(19, 50, 11)),
                    ("autumn",  23, hms_to_fday(11, 32, 34)),
                    ("winter",  22, hms_to_fday( 7, 44, 52)))),
                (2000,
                    (("spring", 20, hms_to_fday( 7, 36, 19)),
                    ("summer",  21, hms_to_fday( 1, 48, 46)),
                    ("autumn",  22, hms_to_fday(17, 28, 40)),
                    ("winter",  21, hms_to_fday(13, 38, 30)))),
                (2001,
                    (("spring", 20, hms_to_fday(13, 31, 47)),
                    ("summer",  21, hms_to_fday( 7, 38, 48)),
                    ("autumn",  22, hms_to_fday(23,  5, 32)),
                    ("winter",  21, hms_to_fday(19, 22, 34)))),
                (2002,
                    (("spring", 20, hms_to_fday(19, 17, 13)),
                    ("summer",  21, hms_to_fday(13, 25, 29)),
                    ("autumn",  23, hms_to_fday( 4, 56, 28)),                               
                    ("winter",  22, hms_to_fday( 1, 15, 26)))),
                (2003,
                    (("spring", 21, hms_to_fday( 1,  0, 50)),                               
                    ("summer",  21, hms_to_fday(19, 11, 32)),
                    ("autumn",  23, hms_to_fday(10, 47, 53)),
                    ("winter",  22, hms_to_fday( 7,  4, 53)))),
                (2004,
                    (("spring", 20, hms_to_fday( 6, 49, 42)),
                    ("summer",  21, hms_to_fday( 0, 57, 57)),
                    ("autumn",  22, hms_to_fday(16, 30, 54)),
                    ("winter",  21, hms_to_fday(12, 42, 40)))),
                (2005,
                    (("spring", 20, hms_to_fday(12, 34, 29)),
                    ("summer",  21, hms_to_fday( 6, 47, 12)),
                    ("autumn",  22, hms_to_fday(22, 24, 14)),
                    ("winter",  21, hms_to_fday(18, 36, 1))))]
        months = {"spring" : 3,  "summer" : 6, "autumn" : 9, "winter" : 12}

        for yr, terms in tbl:
            for season, day, fday in terms:
                approx = equinox_approx(yr, season)
                jd = equinox(approx, season, days_per_second)
                self.assertAlmostEqual(jd, cal_to_jd(yr, 
                                                     months[season],
                                                     day + fday),
                                                     places=4)

