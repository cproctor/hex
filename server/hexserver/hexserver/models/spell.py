from db import db_connection
from user import _user_name_exists, _authenticate_user
import json
import time
import logging

log = logging.getLogger(__name__)

def get_spells(request):
    conn = db_connection(request)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spells;")
    result = cursor.fetchall()
    conn.close()
    return result

def get_current_spells(request):
    conn = db_connection(request)
    cursor = conn.cursor()
    currentSpells = _get_current_spells(cursor)
    conn.close()
    return currentSpells

def get_spell_by_time(request, castTime):
    conn = db_connection(request)
    cursor = conn.cursor()
    spell = _get_spell_by_time(cursor, castTime)
    conn.close()
    return spell
    
def _get_spell_by_time(cursor, castTime):
    cursor.execute("SELECT * FROM spells WHERE cast_time = ?", (castTime,))
    return cursor.fetchone()

def _get_current_spells(cursor):
    cursor.execute("SELECT * FROM spells WHERE complete = 0 ORDER BY cast_time")
    current = cursor.fetchone()
    upcoming = cursor.fetchall()
    return {
        "current": current,
        "upcoming":upcoming
    }

def create_spell(request, params):
    conn = db_connection(request)
    cursor = conn.cursor()
    spellTime = int(time.time())
    # We use spellTime as a primary key. So if we should happen to get two spells
    # at the same second, pretend like the second came a second later.
    while _get_spell_by_time(cursor, spellTime):
        spellTime += 1
    try:
        assert(_authenticate_user(params['user_name'], params['spirit_animal'],
                cursor))
        assert(isinstance(params['name'], basestring))
        assert(params['name'] != '')
        assert(params['setup'] or params['loop'])
        for component in ['setup', 'loop']:
            if params[component]:
                for frame in params[component]:
                    try:
                        assert(validate_frame(frame))
                    except:
                        log.debug(frame)
                        raise AssertionError()
    except IOError():
        return False
    setup = json.dumps(params['setup']) if params['setup'] else ''
    loop = json.dumps(params['loop']) if params['loop'] else ''
    cursor.execute('INSERT INTO spells VALUES (?,?,?,?,?,?,?)', (
        params['user_name'],
        params['name'], 
        3,
        spellTime,
        setup,
        loop,
        0
    ))
    conn.commit()
    newSpell = _get_spell_by_time(cursor, spellTime)
    conn.close()
    return newSpell

def mark_spell_complete(request, castTime):
    conn = db_connection(request)
    cursor = conn.cursor()
    result = _mark_spell_complete(cursor, castTime)
    conn.commit()
    conn.close()
    return result

def _mark_spell_complete(cursor, castTime):
    cursor.execute("UPDATE spells SET complete = ? WHERE cast_time = ?", (1, castTime))
    return cursor.fetchone()
    

def validate_frame(frame):
    try:
        assert isinstance(frame, list)
        for layer in frame: 
            assert isinstance(layer, list)
            assert len(layer) == 2
            colors, bulbs = layer
            assert len(colors) == 4
            for color in colors:
                assert isinstance(color, int)
            for bulb in bulbs:
                assert isinstance(bulb, int)
    except:
        return False
    return True
