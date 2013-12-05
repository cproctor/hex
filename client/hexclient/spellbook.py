# The spellbook contains functions that generate spells, as well as helper
# functions you can use to write your own spells. Hex Client uses the 
# spellbook, but it can be used directly with Hex Connection as well:
# 
# from hex_connection import HexConnection
# hex = HexConnection()
# colorSpell = spell_color([15,15,0,220])
# hex.create_spell('my_name', 'my_spirit_animal', 'spell name', colorSpell)
# 
# The structure of every spell is the same:
#   {
#       'setup': [frames...]
#       'loop': [frames...],
#   }
# 
# Setup runs once and then loop runs forever (the total time available for 
# your program is limited by how many points you have). Each frame is composed
# of color layers, where each color layer specifies a color and then which lights
# should have that color. Here's a color layer that turns the seven center lights
# green:
#
# [ [0, 15, 0, 200], [30, 31, 32, 33, 34, 35, 36] ]

# ===============
# Built-in spells
# ===============

def spell_color(color):
    validate_color(color)
    return {
        'setup': [[[color, all_lights()]]],
        'loop': None
    }

def spell_spirit(backgroundColor, spiritColor):
    for color in [backgroundColor, spiritColor]:
        validate_color(color)
    setup = [[[backgroundColor, all_lights()]]]
    loop = [[
        [backgroundColor,                           [(i) % 18]], 
        [fade(spiritColor, backgroundColor, 0.7),   [(i+1) % 18]], 
        [fade(spiritColor, backgroundColor, 0.3),   [(i+2) % 18]], 
        [spiritColor,                               [(i+3) % 18]]
    ] for i in range(18)]
    return {
        'setup': setup,
        'loop': loop
    }


# =======
# Helpers
# =======
# These functions make it easier to define the spells above.

def all_lights():
    return range(37)

def lights_in_ring(ringNumber):
    if ringNumber not in range(4):
        raise ValueError("You can only get light rings from 0 to 3.")
    ringBoundaries = [37, 36, 30, 18, 0] 
    return range(ringBoundaries[ringNumber + 1], ringBoundaries[ringNumber])

def fade(colorOne, colorTwo, t):
    """Returns a color partway between colorOne and colorTwo. 
    t=0.0 is fully colorOne, and t=1.0 is fully colorTwo"""
    for color in [colorOne, colorTwo]:
        validate_color(color)
    return [colorOne[i] + (colorTwo[i] - colorOne[i]) * t for i in range(4)]


# ==========
# Validators
# ==========
# The functions below check to make sure spells are valid. It's a good idea to
# validate your spells before sending them to the server.
class InvalidSpellError(Exception):
    "An error to represent a situation where we have an invalid spell"
    pass

def validate_spell(spell, strict=True):
    "Checks to make sure a spell is valid"
    try:
        assert(isinstance(spell, dict))
        assert(spell.get('setup') or spell.get('loop'))
        for programPart in [spell.get('setup'), spell.get('loop')]:
            if programPart is not None:
                assert(isinstance(programPart, list))
                for frame in programPart:
                    validate_frame(frame)
    except AssertionError:
        if strict:
            raise InvalidSpellError()
        else:
            return False
    return True

def validate_frame(frame, strict=True):
    try: 
        assert(isinstance(frame, list))
        for colorLayer in frame: 
            assert(isinstance(colorLayer, list))
            assert(len(colorLayer) == 2)
            validate_color(colorLayer[0])
            lights = colorLayer[1]
            assert(isinstance(lights, list))
            for lightNum in lights:
                assert(isinstance(lightNum, int))
    except AssertionError:
        if strict:
            raise InvalidSpellError()
        else:
            return False
    return True

def validate_color(color, strict=True):
    try: 
        assert(isinstance(color, list))
        assert(len(color) == 4)
        for i, colorValue in enumerate(color):
            assert(isinstance(colorValue, int))
            assert(0 <= colorValue)
            assert (colorValue <= [15, 15, 15, 255][i])
    except AssertionError:
        if strict:
            raise InvalidSpellError()
        else:
            return False
        return True
                
                
            
