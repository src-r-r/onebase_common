=======================
Configuration YAML file
=======================

In order for the server to be configured correctly, a configuration file
must be set up.

Location
========

The default location for this file is ``$HOME/.public/onebase/config.yaml``.

Structure
=========

The 1st level of the yaml file will contain the following configuration keys:

===========     ========================================================
key             description
===========     ========================================================
mode            How we want to run the server.
server          Configuration options for the server.
database        Configuration options for the mongodb backend.
collection      Collection name used for mongodb.
email           Email configuration.
===========     ========================================================

mode
----

Any value can be used for this key, as long as it's used throughout the
``server``, ``database``, and ``collection`` configuration. Example values
include ``development``, ``test``, ``production``.

server
------

Hostname and port on which flask will run. This is intended to be the
public-facing URL, so that links don't redirect to ``http://localhost:5000``.
Specify a configuration based on the ``mode``.

Keys:

:host:
    hostname (e.g. "example.com")
:port:
    **(optional)** Port number for the server
:base_urL:
    **(optional)** Overrides whatever is used for ``host`` and ``port``

Example::

    server:
        development:
            host: localhost
            port: 5000
        production:
            host: example.com
            base_url: http://my.example.com
