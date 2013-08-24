
Introduction
============
Astrolabe is a collection of subroutines and
applications for calculating the positions of the sun, moon,
planets and other celestial objects. The emphasis is on high
accuracy over a several thousand year time span. Note that
the techniques used are overkill for most calendar
applications. 

The subroutine library attempts to implement some
the techniques described in <cite>Astronomical
Algorithms</cite>, second edition 1998, by Jean Meeus, <a
href="http://www.willbell.com/">Willmann-Bell, Inc</a>. 

Currently there are no graphical applications apart from
some demo CGI interfaces. 

Astronomia will work with Python 2.6+ and 3.0+.

Documentation
=============
Reference documentation is at http://pythonhosted.org/astronomia/

Installation
============

At the command line::

    $ pip install astronomia
    # OR
    $ easy_install astronomia

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv astronomia
    $ pip install astronomia

Development
===========
Development is managed on bitbucket at
https://bitbucket.org/timcera/astronomia/overview.

History
=======
Astronomia is a fork of the Astrolabe library created by Bill McClain.  The
Astrolabe library is no longer available.

I focused on the Python code, updating with newer data and equations as I found them.
