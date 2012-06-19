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

GitHub allows repositories to be configured with `service hooks`, which allow
GitHub to communicate with a web server (and thus web services) when
certain actions take place within that repository.  These can be
configured via GitHub's web interface through the ``Admin`` page for
repostories, in the ``Service Hooks`` section, which provides most options, 
or else via GitHub's API, which provides some additional hidden settings.  

For an introduction to this topic, consult the `Post-Receive Hooks`_ 
documentation.

Effectively, GitHub will send a POST request to a given web-based endpoint with
relevant information about commits and metadata about the repository when a
certain trigger happens. The `GitHub Hooks API`_ has complete details about
what event triggers are available, details about what services are available,
and more.

Examples
^^^^^^^^

As a worked example, you can configure a repository you have to send details
about commits and changes as they happen to a Jenkins CI instance in order for
continuous testing to take place. You would enter the following in your
``github-collective`` configuration like so::

    [hook:my-jenkins-hook]
    name = web
    config =
        {"url": "https://jenkins.plone.org/github-webhook/",
        "insecure_ssl": "1"
        }
    active = true

    [repo:collective.github.com]
    ...
    hooks = 
        my-jenkins-hook

The result here is that, once run, the ``collective.github.com`` repository
will have a ``web`` hook created against it that instructs GitHub to send the 
relevant POST payload to the given ``url`` in question. This hook creation
is effectively synomymous with adding a hook via the web-based interface,
with the one minor exception in that we provide an extra value 
for ``insecure_ssl`` to ensure that GitHub will communicate with our non-CA
signed certificate.

Our ``[repo:]`` section has a ``hooks`` option in which you can specify
the identifiers of one or more hooks within your configuration. This option
is not required, however, should you have no service hooks.

See the next section for specifics and how to configure
these types of sections within your ``github-collective`` configuration.

Hook section configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^

Each ``[hook:]`` section within your configuration can utilise the following
values. Options provided here will be coerced from standard ini-style options
into suitable values for posting JSON to GitHub's API. For specifications,
refer to https://api.github.com/hooks

    `name` (required)
      String identifier for a service hook. Refer to specification for
      available service identifiers or to the Service Hooks administration page
      for your repository. One of the most commonly used options is ``web`` for
      generic web hooks (seen as `WebHook URLs` in the Service Hooks
      administration page). 

    `config` (required)
      Valid JSON consisting of key/value pairs relating to configuration of
      this service.  Refer to specifications for applicable config for each
      service type. 
      
      *Note*: if a change is made to your local configuration,
      ``github-collective`` will attempt to update hook settings on GitHub. If
      you have Boolean values present in this option, then in order to prevent
      ``github-collective`` from attempting to update GitHub on every run,
      these values should exist as strings - either ``"1"`` or``"0"`` - as this
      is how GitHub stores configuration (and we compare against this to check
      whether we need to sync changes).

    `events` (optional)
      List of events the hook should apply to. Different services can respond
      to different events. If not provided, the hook will default to
      ``push``. Keep in mind that certain services only listen for certain
      types of events.  Refer to API specification for information.


    `active` (optional)
      Boolean value of whether the hook is enabled or not.

How to install
==============

This package can be installed in a traditional sense or otherwise deployed
using Buildout.

Installation
------------

:Tested with: `Python2.6`_
:Dependencies: `argparse`_, `requests`_

::

    % pip install github-collective
    (or)
    % easy_install github-collective

Deploy with Buildout
--------------------

An example configuration for deployment with buildout could look like this::

    [buildout]
    parts = github-collective

    [settings]
    config = github.cfg
    organization = my-organization
    admin-user = my-admin-user
    password = SECRET
    cache = my-organization.cache

    [github-collective]
    recipe = zc.recipe.egg
    initialization = sys.argv.extend('--verbose -C ${settings:cache} -c ${settings:config} -o ${settings:organization} -u ${settings:admin-user} -P ${settings:password}'.split(' '))
    eggs =
        github-collective

Deploying in this manner will result in ``bin/github-collective`` being
generated with the relevant options already provided.  This means that
something calling this script need not provide provide arguments, making its
usage easier to manage.

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
.. _`Post-Receive Hooks`: https://help.github.com/articles/post-receive-hooks
.. _`Python2.6`: http://www.python.org/download/releases/2.6/
.. _`argparse`: http://pypi.python.org/pypi/argparse
.. _`requests`: http://python-requests.org
.. _`Rok Garbas`: http://www.garbas.si
.. _`David Beitey`: http://davidjb.com

