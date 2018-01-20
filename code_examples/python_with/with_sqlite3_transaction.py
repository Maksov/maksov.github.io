# -*- coding: utf-8 -*-
import sqlite3

data = [('00:19:FF:3D:D6:58', '10.1.10.33', '10', 'FastEthernet0/3'),
        ('00:09:BB:3D:D6:58', '10.1.10.2', '10', 'FastEthernet0/1'),
        ('00:14:33:FE:5B:69', '10.1.15.2', '15', 'FastEthernet0/12'),
        ('00:15:BF:7E:9B:60', '10.1.15.4', '15', 'FastEthernet0/6')]


connection = sqlite3.connect('dhcp_snooping.db')

try:
    with connection:
        query = 'INSERT into dhcp values (?, ?, ?, ?)'
        connection.executemany(query, data)
except sqlite3.IntegrityError as e:
    print('Error occured: ', e)
else:
    print('Запись данных прошла успешно')


for row in connection.execute('select * from dhcp'):
    print(row)

connection.close()
