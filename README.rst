jupyter_app
===========

Run Jupyter lab as a desktop app.

Installation
------------

.. code-block:: none

    $ pip install jupyter_app

Additionally, you need Firefox installed,
or download `NW.js <https://nwjs.io/>`_ to your downloads folder.


Usage
-----

.. code-block:: none

    $ jupyter_app


Select a specific app runtime (see
`docs <http://webruntime.readthedocs.io/en/latest/#webruntime.launch>`_):
    
.. code-block:: none

    $ jupyter_app --webruntime=nw-app


How it works
------------

The ``jupyter_lab`` command starts a normal Jupyterlab server, but instead
of launching a brower tab to connect to it, it launches a browser window
that is made to look like a desktop app (including icon, process name, etc.).
When the window is closed, the server shuts down. This uses the
`webruntime <https://github.com/flexxui/webruntime/>`_ module.
