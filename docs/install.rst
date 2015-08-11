============
INSTALLATION
============

This would guide you with setting up and running the app locally.

Pre-Requisites
--------------

I assume you have virtual environment installed and activated.

Local Set-up
------------

To set up the app locally, carry out the following steps:

- Install the requirements for the app from requirements.txt file in the root by:
::

  $ pip install -r requirements.txt

- Start the ``mongo`` server on your machine by running command:
::

  $ mongod

- In another terminal, go to ``/src``  and start the Flask Server by running command:
::

  $ python manage.py

.. note:: For each terminal, ensure you activate your virtual environment.

- In another terminal, Launch the web app by navigating to ``src/client/app`` and launch on a simple server such as ``SimpleHTTPServer`` by:
::

  $ python -m SimpleHTTPServer
  
You can now access the app via `localhost:8000`_ (If running SimpleHTTPServer in default configuration).
  
.. _localhost:8000: http://localhost:8000
