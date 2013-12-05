from db import db_connection
import logging

log = logging.getLogger(__name__)

def get_users(request):
    conn = db_connection(request)
    cursor = conn.cursor()
    result = _get_users(cursor)
    conn.close()
    return result

def _get_users(cursor):
    cursor.execute("SELECT * FROM users;")
    return cursor.fetchall()

def get_user(request, name, animal=None):
    conn = db_connection(request)
    cursor = conn.cursor()
    result = _get_user(cursor, name, animal)
    conn.close()
    return result

def _get_user(cursor, name, animal=None):
    if animal is None:
        cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    else:
        cursor.execute("SELECT * FROM users WHERE name = ? AND spirit_animal = ?", (name, animal))
    return cursor.fetchone()
    
def create_user(request, params):
    conn = db_connection(request)
    cursor = conn.cursor()
    if not _validate_user(params, cursor):
        return False
    cursor.execute('INSERT INTO users VALUES (?,?,?)', (params['name'], params['spirit_animal'], 0))
    conn.commit()
    result = _get_user(cursor, params['name'])
    conn.close()
    return result

def _validate_user(params, cursor):
    try:
        log.debug("in validate_user")
        assert(isinstance(params['name'], basestring))
        log.debug("Name ok")
        assert(isinstance(params['spirit_animal'], basestring))
        log.debug("animal ok")
        assert(not _user_name_exists(params['name'], cursor))
        log.debug("Name unique")
        return True
    except AssertionError:
        return False
    except KeyError:
        return False

def increment_user_score(request, username, amount_to_add=1):
    conn = db_connection(request)
    cursor = conn.cursor()
    result = _increment_user_score(username, amount_to_add, cursor)
    conn.commit()
    conn.close()
    return result

def _increment_user_score(username, amount_to_add, cursor):
    user = _get_user(cursor, username)
    if not user:
        return False
    cursor.execute("UPDATE users SET points = ? WHERE name = ?", 
            (user[2] + amount_to_add, username))
    return cursor.fetchone() == 1

def _user_name_exists(username, cursor):
    log.debug("UNE")
    cursor.execute("SELECT count(*) FROM users WHERE name = ?", (username,))
    result = cursor.fetchone()
    log.debug(result)
    return (result[0] != 0)

def _authenticate_user(name, spirit_animal, cursor):
    cursor.execute("SELECT count(*) FROM users WHERE name = ? AND spirit_animal = ?", 
            (name, spirit_animal))
    return cursor.fetchone()[0] != 0

def spell_duration(points):
    if points < 5: 
        return 5
    elif points < 10:
        return 10
    elif points < 20:
        return 15
    elif points < 50:
        return 20
    elif points < 75:
        return 25
    else:
        return 30
