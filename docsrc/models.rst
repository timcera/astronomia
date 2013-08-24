Models and Accuracy
===================

Mercury through Neptune
~~~~~~~~~~~~~~~~~~~~~~~

Model: The planetary model is VSOP87
(Variations Seculaires des Orbites Planetaires) by
Bretagnon and Francou. The original model documentation,
data files, and sample Fortran routines are available 
(http://vizier.cfa.harvard.edu/viz-bin/ftp-index?/ftp/cats/VI/81)
NOTE: It is '''not'''
neccessary to download any data or sources from the
original site. I have provided everything required. The
original data files require about 4.1 MB; I have combined
and reduced these to about 1.4 MB. The full accuracy of the
model is retained.

Version: The VSOP model is available in
several variants. I am using version "D" which produces
heliocentric spherical coordinates for the equinox of date.
This is the same as used in Meeus.

Accuracy: The model produces positions
of better than 1 arc-second for Mercury through Mars for
the years -2000 to +4000, for Jupiter and Saturn for the
years 0 to +4000, and for Uranus and Neptune for the years
-4000 to +8000. Within those ranges, the actual accuracies
are:

Accuracy of planetary positions

        +---------+-------------+-------------------------+
        | Planet  | Distance to | Latitude and            |
        |         | Sun (km)    | Longitude (arc seconds) |
        +=========+=============+=========================+
        | Mercury | 0.3         | 0.001                   |
        +---------+-------------+-------------------------+
        | Venus   | 2.7         | 0.005                   |
        +---------+-------------+-------------------------+
        | Earth   | 3.7         | 0.005                   |
        +---------+-------------+-------------------------+
        | Mars    | 22.8        | 0.021                   |
        +---------+-------------+-------------------------+
        | Jupiter | 272         | 0.072                   |
        +---------+-------------+-------------------------+
        | Saturn  | 1000        | 0.144                   |
        +---------+-------------+-------------------------+
        | Uranus  | 230         | 0.017                   |
        +---------+-------------+-------------------------+
        | Neptune | 1891        | 0.087                   |
        +---------+-------------+-------------------------+

A note on the Meeus version. Meeus
prints a truncated version of the model in his book. The
first edition had an optional software supplement which
included the truncated data. This supplement is no longer
available, but the complete data presented here can be used
instead of the version on the diskette. I use a different
format.

Moon
~~~~

The lunar model is Meeus's simplified version of ELP2000-82
by Chapront. The complete model can be found at
http://cdsarc.u-strasbg.fr/viz-bin/Cat?VI/79.
Accuracy of the simplified version is about 10 arc-seconds
in longitude and 4 arc-seconds in latitude. (Over what
period?)

Applications
============
check_equinox: Check the accuracy of the
equinox approximation routines over 4000 years.

cronus: A clock application that
displays a variety of celestial events in the order they
occur.

equinox-cgi:
A demo CGI interface to the Easter routine.

solstice: Displays the instants of
equinoxes and solstices for a range of years. Times are
accurate to one second.

solstice-cgi:
A demo CGI interface to the Solstice and Equinox
routines.

To Do
=====

Improve the lunar model, perhaps with the complete
Chapront ELP2000-82.

Add more material from Meeus:

  Add a model for Pluto.

  Add year-by-year polynomial model for planets Jupiter
  through Neptune.

  Add perihelion/aphelion routines for the planets, and
  perigee/apogee routines for the Moon.

  Look at adjustable truncation of the VSOP model to
  trade accuracy for time.

Fix a bug in the Rise-Set-Transit code which causes events
around 0hr UT to be dropped.

Fix a bug in cronus.py that causes equinox/solstice events
to be reported out of order on that day. (The displayed
values are correct, though).

Improve the param file parsing so people can enter their
longitude and latitude more naturally.

