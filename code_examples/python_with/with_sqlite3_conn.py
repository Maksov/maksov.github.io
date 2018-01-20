import sqlite3

with sqlite3.connect('dhcp_snooping.db') as conn:
    print(conn)
    for row in conn.execute('select * from dhcp'):
        print(row)

try:
    conn.execute('select * from dhcp')
except sqlite3.ProgrammingError as e:
    print(e)
else:
    print('Connection is open')

