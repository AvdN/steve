===========================
 Using steve - commandline
===========================

The ``steve-cmd`` utility is designed to automate the basic tasks that
result in you having a directory of JSON files each containing the
metadata for a single video.

After doinge some ``steve-cmd`` work, you can then tar/zip this
directory up and send it to someone who has API access to the richard
instance you're collecting videos for. This person can then look at
the data and push it.

In this way, anyone can generate the metadata for a richard instance
from the comfort of their own command line.


Usage
=====

For list of subcommands, arguments and other help, do this::

    steve-cmd --help

The basic commands are these:

**createproject**

    Creates the directory structure and configuration files for a new
    steve project. Each project is a collection of videos from a
    single source.

**fetch**

    Fetches the metadata for the videos from the url where all the
    videos are hosted and puts it in JSON files in the ``json/``
    directory of your steve project.

**status**

    Tells you the editing status of all the JSON files.

**verify**

    Goes through the JSON files and verifies correctness of the keys
    and values. Are the required data elements present? Are the values
    of the correct type? Are there any "bad" values?

**webedit**

    Provides a (really super duper) basic web server app that lets you
    go through the JSON files in your web browser.


Also, there are some other subcommands:

**push**

    Pushes a bunch of JSON files to a richard instance.

**pull**

    Pulls a bunch of data from a richard instance and puts it in
    JSON files.

**scrapevideo**

    This is a convenience subcommand for scraping a single video at a
    url and showing the metadata.


Example use
===========

.. Note::

   This is a quick tutorial---you don't have to use steve like
   this. Use it in a way that makes your work easier!

1. Install steve.

2. Run: ``steve-cmd createproject europython2011``

   This creates a ``europython2011`` directory for project files.

   I usually call this the project directory.

   In that directory is:

   1. a ``steve.yaml`` project config file
   
   Later on a ``json/`` and a ``yaml/`` directory which hold the video
   metadata JSON/YAML files are created.

   I usually have all my helper scripts in the project directory since
   it has the ``steve.ini`` file.

3. ``cd europython2011``

4. Edit ``steve.yaml``::

    project:
      # The name of this group of videos. For example, if this was a conference
      # called EuroPython 2011, then you'd put:
      # category: EuroPython 2011
      category: 
    
      # The url for where all the videos are listed.
      # e.g. url: http://www.youtube.com/user/PythonItalia/videos
      url: 
    
      # The projectpath is where steve assumes subdirs if not explitly set
      # projectpath: /data1/src/pyvideo.steve/tmp
      # The jsonpath, if set, is where steve will look for the JSON files
      # jsonpath: /data1/src/pyvideo.steve/tmp/json
      # The yamlpath, if set, is where steve will look for the YAML files
      # yamlpath: /data1/src/pyvideo.steve/tmp/yaml
    
      # name of status file in project directory (should not be steve.yaml)
      # status: status.yaml
    
      # The url for the richard instance api.
      # e.g. url: http://example.com/api/v1/
      api_url:
    
      # Your username and api key.
      # e.g. username: willkg
      #      api_key: OU812
      # username:
      # api_key:
      #
      # Alternatively, you can pass this on the command line or put it in a
      # separate API_KEY file which you can keep out of version control.
      # cred_file:
    

   If you're not pushing the JSON files to a richard instance, you can
   ignore the ``api_url``, ``username`` and ``api_key`` keys.

5. Run: ``steve-cmd fetch``

   This fetches the video metadata from that YouTube user and
   generates a series of JSON files---one for each video---and puts
   them in the ``json/`` directory the command creates if necessary.

   The format for each file matches the format expected by the richard
   API.

6. Run: ``steve-cmd sync``

   This creates the ``yaml/`` directory and creates YAML metadata
   files for all JSON files. It also creates/update ``status.yaml`` to
   hold a time-stamp of the last sync action.

7. See the status of your video metadata.

   Run: ``steve-cmd status``

   Lists filenames for all videos that have a non-empty whiteboard
   field. Because you've just downloaded the metadata, all of the
   videos have a whiteboard field stating they haven't been edited,
   yet. 
   *This currently works on the JSON files, ``sync`` beforehand if necessary.*

   Run: ``steve-cmd ls``

   Lists titles and some other data for each video in the set.
   *This currently works on the JSON files, ``sync`` beforehand if necessary.*

8. Now you go through and edit the json or yaml metadata. There are a few ways
   to do this. **Don't** just pick one way---mix and match them to
   reduce the work required.

   Use the `whiteboard` field to keep track of which videos still have
   problems and/or things that need to be done with them and/or just
   haven't been edited, yet.

   1. **Edit with your favorite editor.**

      You can use the ``status`` command to make this easier.

      For example, if you use vim::

          steve-cmd status --aslist | xargs vim

      and edit them by hand one-by-one.

   2. **Write a script to batch-process the files.**

      You can also write a script which uses functions in
      ``steve.util`` to automate fixing the metadata.

      For example, here's a script that takes the summary data,
      converts it from reStructuredText to HTML and puts it in the
      description field::

          from docutils.core import publish_parts

          from steve.util import (get_project_config, load_json_files,
              save_json_files)


          cfg = get_project_config()
          data = load_json_files(cfg)


          def parse(text):
              settings = {
                  'initial_header_level': 2,
                  'transform_doctitle': 1
                  }
              parts = publish_parts(
                  text, writer_name='html', settings_overrides=settings)
              return parts['body']


          for fn, contents in data:
              print fn

              summary = contents['summary'].strip()
              summary_parsed = parse(summary)
              if 'ERROR' in summary_parsed or 'WARNING' in summary_parsed:
                  print 'problem with %s' % fn
                  raise ValueError()

              if not contents['description']:
                  contents['description'] = parse(summary)


          save_json_files(cfg, data)


      Conference data varies pretty widely, so writing scripts to
      batch-process it to handle issues like this is super
      helpful. Automate anything you can.

      See the API documentation in :ref:`steve-utils`.

   3. **Use the web editor.**

      steve comes with a bare-bones web-based editor for the json files.
      To launch it from the project directory, do::

          steve-cmd webedit

      then point your browser at the url in the output.

      This is helpful when you have a few things to fix and don't feel
      like writing json.

   4. **Edit the combined YAML files**

      the command::

          steve-cmd yaml
 
      will create a temporary YAML file with all of the combined YAML
      file information. It then starts your editor ($EDITOR). After
      quiting the editor those files which were edited are used to
      overwrite the individual YAML files (based on filename and hash
      information included in initial comments).
    
   5. **Combine and split YAML files**

      You can use other tools than your default editor on the temporary
      combined YAML file by specifying::

          EDITOR=/path/to/command steve-cmd yaml

      You can also combine the YAML files into a file you specify::

          steve-cmd yaml --name some_name.yaml --combine

      run your command on that and then split them into the individual
      files::

          steve-cmd yaml --name some_name.yaml --split

   If there are other tools you want to use---go for it. Anything
   to get the job done.

9. Run: ``steve-cmd verify``

   This goes through all the json files and verifies correctness.

   Is the data of the correct type and shape?

   Are required fields present?

   Are values that should be in HTML in HTML?

   *This currently works on the JSON files, ``sync`` beforehand if necessary.*

10. Now it's time to submit your changes!

   If you do not have an API key that gives you write access to the server,
   then tar the ``json/`` directory up and send it to someone who does.

   If you do have an API key that gives you write access to the
   server, then you can do::

       steve-cmd push

   That will create the videos on the server and update the JSON
   files with the new ids.
   Be sure to run ``steve-cmd sync`` before pushing if you edit the
   metadata in the YAML files.

That's it!

.. Note::

   Use version control for your steve project and commit changes to
   it. Make sure you back it up, too! Don't lose everything you've
   done because you wrote a bad batch-processing script!
