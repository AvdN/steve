===========================
Syncing JSON and YAML files
===========================

The ``steve-cmd`` utility supports YAML files in addition to JSON
files for metadata. To support a gradual transition and adaptation of
tools to the YAML format it relies on synchronisation of the JSON and
YAML metadata to work on either of the two sets.

In the future more commands will directly work on the YAML metadata,
eventually only relying on doing a sync to JSON before uploading to
richard (and maybe even not that). 

Syncing is currently not automated (i.e. ``steve-cmd verify`` verifies
the JSON files, and you have to run ``steve-cmd sync`` **manually** to
incorporate changes to your YAML files to get those verified). This will probably change
in the future.

Usage
=====

Syncing is done by issuing::

   steve-cmd sync

This creates any directories necessary and compares the last
modification time for the JSON and YAML files, relying on them to have
the same basename (without extension). These times are compared to the
last sync timestamp stored in ``status.yaml`` (which is updated on a
successful sync). If both the JSON and the YAML (assuming both are
available) metadata files of **any** of the videos been touched, the
sync will fail and no metadata is synced (see `resolving sync
problems`_). 

It is perfectly fine to edit ``json/001.json`` and
``yaml/007.yaml`` and then synchronise. Just don't touch
``json/001.json`` and ``yaml/001.yaml``.

Any missing files are created both from ``json/`` to ``yaml/`` and
vice versa.

Sync often, if nothing needs syncing nothing is changed except for the
last synced timestamp.

Differences between JSON and YAML files
---------------------------------------

During the sync to, and from, YAML the following are auto-adapted to
provide a more readable YAML file:

- dates (``YYYY-MM-DD``) are converted to datetime objects before saving
  resulting in::

      recorded: 2015-08-08
  instead of quoted string: ``recorded: "2015-08-08"``
- Empty strings are converted to ``None`` and written as nothing
  ::

     language:
     
  instead of the empty string (``language: ""``), so you can directly 
  type something there, without having to insert
  that between double quotes, or remove those (unless the string has
  special characters you don't need those quotes in YAML
- Multi-line strings are converted to literal block scalars (with some
  ``ruamel.yaml`` magic)::

      summary: |-
        Moritz Gronbach - What's the fuzz all about? Randomized data 
        generation for robust unit testing
        [EuroPython 2015]
      
   which is more readable than the single line JSON, or non block
   YAML, version. Take care with indentation when editing these
   scalars. This is essentially two-space indented markdown.

As indicated above, this "magic" is undone, syncing from YAML to JSON.


Resolving sync problems
=======================

If one or more metadata files have been edited both on the json and
the yaml side, you have to resolve this by hand before
proceeding. Running ``steve-cmd sync`` will fail and give you the list
of files that are a problem.

If you know both files are the same (touched but not edited) remove
one of the files.

If only one is up-to-date remove the other file, ``steve-cmd sync``
will recreate it from the newer one

If both side actually have useful changes, you can copy them from 
file A to file B and remove file A. Since A and B are JSON and YAML
this might not be too easy, the alternative is (assuming ``json/001.json``
and ``yaml/001.yaml`` were both edited)::

  mv -i json/001.json json/999.json
  steve-cmd sync
  
(pick a number different from 999 if the file already exists, do the
above ``mv`` for all the files having problems, before calling ``steve-cmd sync``). 

Now use your favourite ``diff`` tool, e.g. ``meld``, to update ``yaml/001.yaml``::

  meld yaml/001.yaml yaml/999.yaml

and if yaml/001.yaml is up to date::
  
  rm yaml/999.yaml json/999.yaml json/001.yaml
  steve-cmd sync

**If you change the timestamp in the status file, any files that were
edited on both sides and have modification times older than the
timestamp, will be considered "in-sync"**
