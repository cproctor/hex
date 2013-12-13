hex: a classroom spell-casting medium
===

I wanted to build an array of lights that I could put up on the wall in the 
gallery at school, without telling anybody where it came from. The only clue 
about its origins or purpose will be a small sign containing a web address: 
http://hex.local Students who go to this URL will find a page served by the
device which explains how to cast spells on the lights. My students now have
all the technical skills they need to for this--they know how to write basic 
python programs, how to install python packages, and how to think about an 
animation as a sequence of numbers. This should be a fun challenge which 
reinforces their ability to learn new coding skills independently and to 
have an impact on the world through them. 
Plus, we all like the idea of Hogwarts--of having something magical about your
school that you can discover.

Hex was also an opportunity to exercise a "full stack" of technology, from 
physically building the box with a tablesaw to writing documentation for the 
client program in sphinx. Here's a bottom-to-top tour of the project:

The thing itself
----------------
Building the hex allowed me the distinctive pleasure of calculating the geometry
of triangles. There are thirty seven lights on the hex, forming a hexagon whose 
diameter is seven lights. After prototyping a few different arrangements, I 
decided to space the bulbs three inches apart on center, giving me a twenty-four
inch diameter hexagon. I had a chance to visit Tap Plastics to buy some diffusing 
acrylic plastic--living out my fantasy of having majored in mechanical engineering!

Wires, solder, and embedded circuits
------------------------------------
I'm partway through a more ambitious lights project, so solering wasn't new to me. I'm 
using GE's G35 holiday lights, which they seem to have discontinued. These lights became
popular with hackers in the 2012 holiday season because each bulb can be controlled 
independently. The communication protocol was reverse-engineered so you could write your
own light patterns. 

Each bulb has an integrated circuit; when a bulb is powered up, it starts with no address.
When a bulb receives a message and it has no address, it takes that messages's address 
as its own. Otherwise, bulbs only respond to messages addressed to them and relay other
messages along the wire. This allows an elegant addressing mechanism: when you start up, 
send out messages addressed to 0, 1, 2, 3, etc. The first bulb consumes the first message and
then relays the rest; the second bulb consumes the second message and then relays the rest,
and so on. 

Arduino
-------
I've played with Arduinos for years, so I knew it would be a good fit for this project. 
I used sowbug's G35 library (github) to drive the lights, and then wrote a program that 
receives data over the serial port, parses light programs, and then tells the G35 driver 
to update the lights. 

One challenge that was new to me was dealing with the Arduino's 64-bit buffer. It's not
convenient to fit one frame of information--37 lights, each with 4-byte R, G, and B, and 
8-byte intensity--into 64 bits, so it became necessary to create a simple protocol by 
which the arduino tells its client when it has finished reading the buffer and is ready 
for more. Communication errors are not uncommon, so I had to choose a way for the Arduino
to validate the messages it receives and request retransmission of any that are invalid.

Raspberry Pi
------------
This project was a great opportunity to buy myself a Raspberry Pi, a $40 linux
computer on a chip the size of a pack of cards. This was my first experience 
doing basic configuration of a linux sysyem, and I found myself needing to 
do some shell scripting (a dark art which I had been hoping I would never need again).
Using a couple of scripts I found online, I configured the pi to automatically 
join one of the networks whose credentials I provided, and, failing this, to broadcast
its own network so that I could ssh into it. The first time I tried to set this up, I 
mis-configured the script so that the machine wouldn't boot at all. I had to wipe its 
memory and start over. 

Hex Driver
----------
I wrote a python program which listens on a message queue for light programs, validates
them, and then sends them chunk by chunk to the arduino. 

Hex Server
----------
I wrote an API that client programs can interact with to create users, cast spells, 
and praise other peoples' spells. The hex server implements the API, hosts
documentation for the client modules, and has an interactive javascript-based 
renderer to show spells. 

Hex Client
----------
I wrote a few modules for use by clients--hex_client, which is a text-based 
interactive game that lets users cast spells, spellbook, which contains the 
spells used in hex_client and also helper functions students can use, and 
hex_connection, which my program and students' programs can use to actually
communicate with the hex.

I had installed plenty of modules from pypi, but I had never gone through the
process of packaging and uploading one before. 
