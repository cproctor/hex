Writing More Spells
===================

When you want to start writing your own spells, you'll probably want to write a 
program in python. 

Spell structure
---------------

A spell is a dictionary with two possible keys: setup and loop. If setup is 
defined, it will be run once at the beginning of the spell. If loop is defined,
it will run over and over until your time limit is reached. You may define both
setup and loop, but at least one must be defined for a spell to be valid.
Setup and loop should each be a list of frames::

    spell = {
        'setup': [], # A list of frames...
        'loop': [] # Another list of frames...
    }

Frames
++++++

Any animation consists of frames--still pictures--which change rapidly. The Hex
tries to show 24 frames per second, but sometimes lags a bit slower. 

Each frame is a list containing color layers. Each color layer is a list of 
two lists--the first defines a color and the second lists which bulbs 
should be set to that color. By using several color layers in a frame, you can
create a frame which sets each bulb to the color you want. 

Many times you don't need to change a bulb's color from one frame to the next. 
If you don't change a bulb's color in a frame, it stays the same color. Here's an 
example frame which sets bulb 0 to be red, bulb 1 to be green, and bulb 2 to be blue::

    frame = [
        [ [15, 0, 0, 255], [0] ],
        [ [0, 15, 0, 255], [1] ],
        [ [0, 0, 15, 255], [2] ]
    ]

Colors
++++++

Every time you define a color layer, you need to specify a color. A color is a list
of four integers. The first three specify how much red, green, and blue you want, 
from 0 to 15. The fourth number specifies how bright you want the light to be, from 0
to 255. Here are a few colors::

    red     = [15, 0, 0, 255]
    green   = [0, 15, 0, 255]
    blue    = [0, 0, 15, 255]
    yellow  = [15, 15, 0, 255]
    magenta = [15, 0, 15, 255]
    cyan    = [0, 15, 15, 255]
    white   = [15, 15, 15, 255]

Lights
++++++

The second part of each color layer is a list of lights. Each light in the hex has a 
number::

           / \ / \ / \ / \ 
          | 3 | 2 | 1 | 0 |
         / \ / \ / \ / \ / \ 
        | 4 | 20| 19| 18| 17|
       / \ / \ / \ / \ / \ / \ 
      | 5 | 21| 31| 30| 29| 16|
     / \ / \ / \ / \ / \ / \ / \ 
    | 6 | 22| 32| 36| 35| 28| 15|
     \ / \ / \ / \ / \ / \ / \ /
      | 7 | 23| 33| 34| 27| 14|
       \ / \ / \ / \ / \ / \ /
        | 8 | 24| 25| 26| 13|
         \ / \ / \ / \ / \ / 
          | 9 | 10| 11| 12|
           \ / \ / \ / \ / 

However, you'll quickly get tired of writing out lists by hand. The 
:doc:`spellbook` module has some handy functions like :code:`all_lights` and 
:code:`lights_in_ring` which will return a list of lights for you. And you 
can always use the built-in :code:`range` function to get a list. Check out 
the `documentation on range <http://docs.python.org/2/library/functions.html#range>`_
--it's really powerful. :code:`range(0, 18, 3)` returns a list from 0 to 18, 
counting by 3.

Putting it all together
+++++++++++++++++++++++

Here's an example program that casts a rather annoying spell: The whole Hex will 
flash cyan, yellow, and magenta in turn::

    from hex_connection import HexConnection
    from spellbook import all_lights

    connection = HexConnection()

    cyanFrame    = [[[0, 15, 15, 255], all_lights() ]]
    yellowFrame  = [[[15, 15, 0, 255], all_lights() ]]
    magentaFrame = [[[15, 0, 15, 255], all_lights() ]]

    spell = {
        'setup': None,
        'loop': [cyanFrame, yellowFrame, magentaFrame]
    }

    # Let's assume we already have a user called gertrude, 
    # whose spirit animal is goose.
    connection.create_spell('gertrude', 'goose', spell)





