=======
 steve 
=======

Summary
=======

steve is a command line utility for downloading information for a conference,
downloading all the metadata for the videos, and making it easier to
transform the data, fix it and make it better.

It's designed to use with richard. It uses richard's API for pulling/pushing
data.

It solves this use case:

    MAL sends Will a request to add the EuroPython 2011 videos to 
    pyvideo.org. The EuroPython 2011 videos are on YouTube. Will uses
    steve to download all the data for the conference on YouTube, then
    uses steve to apply some transforms on the data, then uses steve
    to edit each video individually and finally uses steve to push
    all the data (the new conference, new videos, speakers, tags) to
    pyvideo.org.


Features
========


History
=======



License, etc
============

steve Copyright(C) 2012 Will Kahn-Greene

This program comes with ABSOLUTELY NO WARRANTY.  This is free software,
and you are welcome to redistribute it under certain conditions.  See
the Terms and Conditions section of `LICENSE`_ for details.

.. _LICENSE: http://www.gnu.org/licenses/gpl-3.0.html


Install
=======

Released version
----------------

If you want a released version of steve, do this:

1. ``pip install steve``


Bleeding edge version
---------------------

If you want a bleeding edge version of steve, do this:

1. ``git clone git://github.com/willkg/steve.git``
2. ``cd steve``
3. ``python setup.py install`` or ``python setup.py develop``


Bleeding edge for hacking purposes
----------------------------------

If you want to install steve in a way that makes it easy to hack on,
do this:

1. ``git clone git://github.com/willkg/steve.git``
2. ``cd steve``
3. ``virtualenv ./venv/``
4. ``./venv/bin/python setup.py develop``

When you want to use steve from your virtual environment, make sure to
activate the virtual environment first. e.g.:

1. ``. ./venv/bin/activate``
2. ``steve-cmd --help``


Run
===

For list of subcommands, arguments and other help, do this::

    steve-cmd --help


Example use
===========

.. Note::

   This is a conceptual example! None of this is implemented, yet!

1. Install steve.

2. Run: ``steve-cmd createproject europython2011``

   This creates a ``europython2011`` directory for project files.

   In that directory is:

   1. a ``steve.ini`` project config file.
   2. a ``json`` directory which hold the video metadata json files.

3. ``cd europython2011``

4. Edit ``steve.ini``::

       [project]
       url = http://www.youtube.com/user/PythonItalia/videos
       type = youtube

5. Run: ``steve-cmd fetch``

   This fetches the video metadata from that YouTube user and
   generates a series of JSON files, one for each video, and puts them
   in the ``json`` directory.

   The format for each file matches the format expected by the richard
   API.

6. Run: ``steve-cmd status``

   Lists the titles of all the videos that have a non-empty whiteboard
   field. Because you've just downloaded the metadata, all of the
   videos have a whiteboard field stating they haven't been edited,
   yet.

7. Run: ``steve-cmd ls``

   Lists titles and some other data for each video in the set.

8. Edit the metadata. When you're done with a video, make sure to
   clear the whiteboard field.

   TODO: steve should make this easier

9. Run: ``steve-cmd push http://example.com/api/v1/``

   This pushes the new videos to your richard instance.

That's it!

.. Note::

   I highly recommend you use version control for your steve project
   and back up the data to a different machine periodically. It
   doesn't matter which version control system you use. It doesn't
   matter how you back it up. However, it does matter that you do
   these things so you aren't sad later on when the inevitable
   happens.


Test
====

steve comes with unit tests.  Unit tests are executed using `nose`_ and
use `fudge`_ as a mocking framework.  If you don't already have nose
and fudge installed, then install them with::

    pip install nose fudge

I like to use `nose-progressive`_, too, because it's awesome.  To
install that::

    pip install nose-progressive

To run the unit tests from a git clone or the source tarball, do this
from the project directory::

    nosetests

With nose-progressive and fail-fast::

    nosetests -x --with-progressive


.. _nose-progressive: http://pypi.python.org/pypi/nose-progressive/
.. _nose: http://code.google.com/p/python-nose/
.. _fudge: http://farmdev.com/projects/fudge/


Source code
===========

Source code is hosted on github.

https://github.com/willkg/steve


Issue tracker
=============

Issue tracker is hosted on github.

https://github.com/willkg/steve/issues


Resources I found helpful
=========================

