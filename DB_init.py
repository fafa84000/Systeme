from sqlite3 import connect
from config import DATABASE_FILE, SQL
from log_manager import log_error

def init():
    try:
        print(DATABASE_FILE)
        print(SQL)
        conn = connect(DATABASE_FILE)
        c = conn.cursor()

        with open(SQL, 'r', encoding='utf-8') as file:
            file_sql = file.read()
        
        stmts = file_sql.split(';')
        for stmt in stmts:
            c.execute(stmt)
            
        conn.commit()
        return conn
    except Exception as e:
        log_error(e)
        return None

def is_connected(conn):
    try:
        conn.execute('SELECT 1')
        return True
    except Exception as e:
        log_error(e)
        return False

def re_init(conn):
    if not is_connected(conn):
        conn.close()
        conn = init()
    return conn