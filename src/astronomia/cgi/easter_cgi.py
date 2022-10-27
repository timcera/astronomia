#! /usr/bin/env python
"""
    Astrolabe copyright 2000, 2001 William McClain
    Astrolabe forked to Astronomia 2013
    Astronomia copyright 2013

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

CGI interface to the Easter routine.

Generate dates of Easter for a range of years, both Gregorian
and Julian calendars.

One application handles both the input form and the displayed
results.

"""

import cgi
import sys
import time

#
# Rather than setup PYTHONPATH in a shell script, we add it
# through sys. That way we need only one file for the application.
#
# This path is specific to SourceForge.
#
sys.path.append("/home/groups/a/as/astronomia/lib/python")

from astronomia.calendar import easter

form = cgi.FieldStorage()

#
# Collect the input parameters
#


def display_form():
    fields = time.localtime(time.time())
    year = fields[0]

    print("Content-type: text/html")
    print()
    print("<HEAD>")
    print("<TITLE>Astronomia Easter Parameters</TITLE>")
    print("</HEAD>")

    print("<BODY>")
    print("<H1>Astronomia Easter Parameters</H1>")

    print(
        '<FORM action="http://astronomia.sourceforge.net/cgi-bin/easter-cgi.py" method="post">'
    )

    print("<TABLE>")
    print("<TR>")
    print('<TD><LABEL for="starting_year">Starting year</LABEL></TD>')
    print(
        f'<TD><INPUT type="text" size=4 name="starting_year" id="starting_year" value="{year-5}"></TD>'
    )
    print("</TR>")
    print("<TR>")
    print('<TD><LABEL for="ending_year">Ending year</LABEL></TD>')
    print(
        f'<TD><INPUT type="text" size=4 name="ending_year" id="ending_year" value="{year+5}"></TD>'
    )
    print("</TR>")
    print("</TABLE>")

    print(
        '<INPUT type="checkbox" checked name="gregorian_calendar" value="1"> Gregorian calendar<BR>'
    )
    print(
        '<INPUT type="checkbox" checked name="julian_calendar" value="1"> Julian calendar<BR>'
    )

    print('<INPUT type="submit" value="Run"> <INPUT type="reset">')

    print('<INPUT type="hidden" name="results" value="1">')

    print("</FORM>")
    print("</BODY>")


#
# Display an error message
#


def display_error(msg):
    print("<HEAD>")
    print("<TITLE>Astronomia Easter Error</TITLE>")
    print("</HEAD>")
    print("<BODY>")
    print("<H1>", msg, "</H1>")
    print("</BODY>")


#
# Display the results
#


def display_results():
    print("Content-type: text/html")
    print()
    print("<HEAD>")
    print("<TITLE>Astronomia Easter Results</TITLE>")
    print("</HEAD>")

    #
    # To do: We should validate the integer values
    #
    # If no starting_year, start with 5 years ago.
    #
    if "starting_year" in form:
        starting_year = int(form["starting_year"].value)
    else:
        fields = time.localtime(time.time())
        year = fields[0]
        starting_year = year - 5

    #
    # If no ending_year, end 10 years after the starting_year.
    #
    if "ending_year" in form:
        ending_year = int(form["ending_year"].value)
    else:
        ending_year = starting_year + 10

    #
    # Make sure end_year >= starting_year.
    #
    if ending_year < starting_year:
        display_error(
            "Ending year {ending_year} is earlier than starting year {starting_year}"
        )
        return

    #
    # We can't go farther back than the first Julian Day number.
    #
    if starting_year < -4712:
        display_error("Starting year {starting_year} is earlier than 4713BC")
        return

    julian_calendar = "julian_calendar" in form
    gregorian_calendar = "gregorian_calendar" in form

    #
    # Must have at least one calendar type.
    #
    if not julian_calendar and not gregorian_calendar:
        display_error("No calendar type selected")
        return

    #
    # Finally, we display the results.
    #
    print("<BODY>")
    print("<H1>Astronomia Easter Results</H1>")

    print("<TABLE BORDER>")

    print("<TR>")
    if gregorian_calendar:
        print("<TH>Gregorian</TH>")
    if julian_calendar:
        print("<TH>Julian</TH>")
    print("</TR>")

    for year in range(starting_year, ending_year + 1):
        print("<TR>")
        if gregorian_calendar:
            month, day = easter(year, True)
            print("<TD><TT>{day:02}-{month:02}-{year:02}</TT></TD>")
        if julian_calendar:
            month, day = easter(year, False)
            print("<TD><TT>{day:02}-{month:02}-{year:02}</TT></TD>")
        print("</TR>")
    print("</TABLE>")

    # handy diagnostic routines
    """
    print "<H1>print_environ</H1>"
    cgi.print_environ()
    print "<H1>print_directory</H1>"
    cgi.print_directory()
    print "<H1>print_environ_usage</H1>"
    cgi.print_environ_usage()
    print "<H1>FieldStorage</H1>"
    #form = cgi.FieldStorage()
    cgi.print_form(form)
    """

    print("</BODY>")


#
# Main routine. There is a hidden field "results" on the parameter form. If it
# is not present, we display the form. If it is, we display the results.
#
if "results" in form:
    display_results()
else:
    display_form()
