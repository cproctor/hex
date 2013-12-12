Hex Connection
==============

The :code:`hex_connection` contains functions you'll use to talk with the Hex
Server. All communication back and forth is via JSON. Here's an example of how
you could create a new user and then cast a spell. This spell would turn the 
whole Hex yellow::

    from hex_connection import HexConnection
    import spellbook

    connection = HexConnection()
    response = connection.create_user("gertrude", "goose")
    if response.json()['result'] == 'OK':
        print("Created gertrude.")
    else:
        print("There was an error creating gertrude...")

    yellow = spell_color([15, 15, 0])
    response = connection.create_spell('gertrude', 'goose', yellow)
    if response.json()['result'] == 'OK':
        print(response.json()['spell'])
    else:
        print("Something went wrong.")


.. automodule:: hex_connection
   :members:

