import sqlite3


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('connected')
    except Exception as e:
        print(e)

    return conn


def create_table():
    db_file = 'ipchecker.sqlite3'

    table = '''
    CREATE TABLE IF NOT EXISTS apichecker_table (
        id integer PRIMARY KEY,
        api text NOT NULL,
        ip  text,
        result text
    );
    '''
    try:

        conn = create_connection(db_file)
        c = conn.cursor()
        c.execute(table)
    except Exception as e:
        print(e)

if __name__=="__main__":
    create_table()