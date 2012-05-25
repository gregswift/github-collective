Introduction
============

`GitHub organizations`_ are great way for organizations to manage their Git
repositories. This tool will let you automate the tedious tasks of creating
teams, granting permissions, and creating repositories or modifying their
settings.

The approach that the ``github-collective`` tool takes is that you edit a
central configuration (currently an ini-like file) from where options are
read and synchronized to GitHub respectively.

Initially, the purpose of this script was to manage Plone's collective
organization on GitHub: http://collective.github.com. It is currently in use
in several other locations.


.. contents

Features
========

* Repositories: create and modify repositories within an organization

  * Configure all repository properties as per the `GitHub Repos API`_,
    including privacy (public/private), description, and other metadata. 
  * After the initial repository creation happens, updated values in your
    configuration will replace those on GitHub.

* Service hooks: add and modify service hooks for repositories.

  * GitHub repositories have support for sending information upon
    certain events taking place (for instance, pushes being made to a 
    repository or a fork being taken).
  * After the initial repo creation process takes place, updated values in your
    hook configuration will `replace` those on GitHub. 
  * Hooks not present in your configuration (such as those manually added
    on GitHub or those removed from local configuration) will *not* be
    deleted.

* Teams: automatically create teams and modify members

  * Control permissions for teams (for example: push, pull or admin)

* Automatically syncs all of the above with GitHub when the tool is run.

Configuration 
=============

Service hooks
-------------

Configure service hooks in your configuration as per the `GitHub Hooks API`_ 
like so::

    [hook:my-hook]
    name = web
    config =
        {"url": "http://plone.org",
        "insecure_ssl": "1"
        }
    events = push issues fork
    active = true

    [repo:my.project]
    ...
    hooks = my-hook

Values provided here will be coerced into suitable values for posting
to GitHub's API. For specifications, refer to https://api.github.com/hooks

    `name` (required)
      String identifier for a service hook. Refer to specification for
      available identifiers.

    `config` (required)
      JSON consisting of key/value pairs relating to configuration
      of this service.  Refer to specifications for applicable config for each
      service. *Note*: in order to prevent this script from attempting
      to update GitHub every run, record Boolean values as string "1" or "0"
      in this JSON - this is how values are stored by GitHub.

    `events` (optional)
      List of events the hook should apply to. Different services can 
      respond to different events. Refer to API specification for information.

    `active` (optional)
      Boolean value of whether the hook is enabled or not.

How to install
==============

:Tested with: `Python2.6`_
:Dependencies: `argparse`_, `requests`_

::

    % pip install github-collective
    (or)
    % easy_install github-collective


Usage
=====

When ``github-collective`` is installed it should create executable with same
name in your `bin` directory. 
::

    % bin/github-collective --help
    usage: github-collective [-h] -c CONFIG [-M MAILER] [-C CACHE] -o GITHUB_ORG
                             -u GITHUB_USERNAME -P GITHUB_PASSWORD [-v] [-p]
    
    This tool will let you automate tedious tasks of creating teams granting
    permission and creating repositories.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            path to configuration file (could also be remote
                            location). eg.
                            http://collective.github.com/permissions.cfg (default:
                            None)
      -M MAILER, --mailer MAILER
                            TODO (default: None)
      -C CACHE, --cache CACHE
                            path to file where to cache results from github.
                            (default: None)
      -o GITHUB_ORG, --github-org GITHUB_ORG
                            github organisation. (default: None)
      -u GITHUB_USERNAME, --github-username GITHUB_USERNAME
                            github account username. (default: None)
      -P GITHUB_PASSWORD, --github-password GITHUB_PASSWORD
                            github account password. (default: None)
      -v, --verbose
      -p, --pretend

Configuration
=============

You can consult one of these examples:

* https://raw.github.com/collective/github-collective/master/example.cfg
* http://collective.github.com/permissions.cfg

to get an idea on how to construct your configuration. 

Example of configuration stored locally
---------------------------------------

::

    % bin/github-collective \
        -c example.cfg \ # path to configuration file
        -o vim-addons \  # organization that we are 
        -u garbas \      # account that has management right for organization
        -P PASSWORD      # account password

Example of configuration stored on github
-----------------------------------------

::

    % bin/github-collective \
        -c https://raw.github.com/collective/github-collective/master/example.cfg \
                         # url to configuration file
        -o collective \  # organization that we are 
        -u garbas \      # account that has management right for organization
        -P PASSWORD      # account password

Example of cached configuration
-------------------------------

::

    % bin/github-collective \
        -c https://raw.github.com/collective/github-collective/master/example.cfg \
                         # url to configuration file
        -C .cache        # file where store and read cached results from github
        -o collective \  # organization that we are 
        -u garbas \      # account that has management right for organization
        -P PASSWORD      # account password


Todo
====

 - Send emails to owners about removing repos
 - better logging mechanism (eg. logbook)


Credits
=======

:Author: `Rok Garbas`_ (garbas)
:Contributor: `David Beitey`_ (davidjb)


.. _`GitHub organizations`: https://github.com/blog/674-introducing-organizations
.. _`GitHub Repos API`: http://developer.github.com/v3/repos/#create
.. _`GitHub Hooks API`: http://developer.github.com/v3/repos/hooks/
.. _`Python2.6`: http://www.python.org/download/releases/2.6/
.. _`argparse`: http://pypi.python.org/pypi/argparse
.. _`requests`: http://python-requests.org
.. _`Rok Garbas`: http://www.garbas.si
.. _`David Beitey`: http://davidjb.com

