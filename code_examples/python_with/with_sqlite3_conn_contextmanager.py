import contextlib
import sqlite3

@contextlib.contextmanager
def sqlite3_connection(db_name):
    connection = sqlite3.connect(db_name)
    yield connection
    connection.close()


with sqlite3_connection('dhcp_snooping.db') as conn:
    for row in conn.execute('select * from dhcp'):
        print(row)

try:
    conn.execute('select * from dhcp')
except sqlite3.ProgrammingError as e:
    print(e)


