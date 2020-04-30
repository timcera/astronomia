.. image:: https://travis-ci.org/timcera/astronomia.svg?branch=master
    :target: https://travis-ci.org/timcera/astronomia
    :height: 20

.. image:: https://coveralls.io/repos/timcera/astronomia/badge.png?branch=master
    :target: https://coveralls.io/r/timcera/astronomia?branch=master
    :height: 20

.. image:: http://img.shields.io/pypi/v/astronomia.svg
    :alt: Latest release
    :target: https://pypi.python.org/pypi/astronomia

.. image:: http://img.shields.io/badge/license-GPL-lightgrey.svg
    :alt: astronomia license
    :target: https://pypi.python.org/pypi/astronomia/

Astronomia - Quick Guide
------------------------
Astronomia is a collection of subroutines and applications for calculating the
positions of the sun, moon, planets and other celestial objects. The emphasis
is on high accuracy over a several thousand year time span. Note that the
techniques used are overkill for most calendar applications. 

The subroutine library attempts to implement some the techniques described in
*Astronomical Algorithms*, second edition 1998, by Jean Meeus, `Willmann-Bell,
Inc. <http://www.willbell.com/">`_

Currently there are no graphical applications apart from some demo CGI
interfaces. 

Astronomia will work with Python 2.6+ and 3.0+.

Documentation
~~~~~~~~~~~~~
Reference documentation is at http://timcera.bitbucket.io/.

Installation
~~~~~~~~~~~~
At the command line::

    $ pip install astronomia
    # OR
    $ easy_install astronomia

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv astronomia
    $ pip install astronomia

Usage
~~~~~
To use Astronomia in a project::

	import astronomia

Development
~~~~~~~~~~~
Development is managed on bitbucket at
https://bitbucket.org/timcera/astronomia/overview.

History
~~~~~~~
Astronomia is a fork of the Astrolabe library created by Bill McClain.  The
Astrolabe library is no longer available.

I (Tim Cera) used the Astrolabe library within my tidal analysis package
`TAPPy <http://tappy.sf.net>`_. In 2013 I pulled Astrolabe out of TAPPy and
forked Astronomia.  I have since fixed many bugs and added features.  The most
important added feature is the ability for most functions to work with array
inputs.  Bill McClain had dual Python and 'C' code, but I focused only on the
Python code, updating with newer data and equations as I found them.
