import contextlib
import sqlite3


with contextlib.closing(sqlite3.connect('dhcp_snooping.db')) as conn:
    for row in conn.execute('select * from dhcp'):
        print(row)

try:
    conn.execute('select * from dhcp')
except sqlite3.ProgrammingError as e:
    print(e)


