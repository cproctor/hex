.. Hex documentation master file, created by
   sphinx-quickstart on Tue Dec 10 11:27:28 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Hex's documentation!
===============================

The hex is a hexagonal array of programmable lights that lives on the wall of 
the gallery. The hex is powered by several computers that serve websites (like
this one), receive commands from computers, and tell the lights what to do. 
If you can figure out who created the hex, he or she will show you how it works.
Watch out, though--this person will probably deny being the creator at first.

There are several different ways cast spells on the hex. To get started with
any of them, you'll need to install the hex_client library::

  sudo easy_install hex_client


The simplest way to cast spells is to just run :code:`hex_client`. You can read more 
about :code:`hex_client` by clicking the link below. To start :code:`hex_client`, 
just type :code:`hex_client` in Terminal.

After a while, you'll probably want to start writing your own spells. To 
do this, just write a python program which creates a spell and then uploads
it to the hex. :code:`hex_client.hex_connection` contains some functions you'll need
for talking to the hex. :code:`hex_client.spellbook` contains all the standard spells
(which can serve as models for your spells), and also some helpful functions
that you might want to use while writing your spells. Click the links below 
for more information.

.. toctree::
   :maxdepth: 2

   hex_client
   writing_more_spells
   spellbook
   hex_connection

