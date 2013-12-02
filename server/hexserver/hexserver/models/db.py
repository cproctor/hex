import sqlite3

def db_connection(request):
    return sqlite3.connect(request.registry.settings['sqlite3.dbname'])

def db_exists(request, cursor=None):
    if not cursor:
        conn = db_connection(request)
        cursor = conn.cursor()
    conn.close()
    
def create_db(request):
    conn = db_connection(request)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS spells")
    cursor.execute(""" 
        CREATE TABLE users (
            name text,
            spirit_animal text,
            points integer
        )
    """)
    cursor.execute("""
        CREATE TABLE spells (
            user_name text,
            name text,
            priority int,
            cast_time int,
            setup string,
            loop string,
            complete int
        )
    """)
    conn.commit()
    conn.close()
    return True
