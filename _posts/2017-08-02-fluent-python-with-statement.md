---
title: "Fluent Python: with statement"
date: 2017-08-02
tags:
 - links
 - notes
 - fluent-python
 - pyneng
category:
 - python
---

Небольшая заметка о конструкции with и о том как создавать свои менеджеры контекста.

Продолжаю читать [Fluent Python](http://shop.oreilly.com/product/0636920032519.do) и дошла до раздела про менеджеры контекстов.

## Конструкция with

Конструкция with используется для оборачивания блока кода менеджером контекста.

Менеджер контекста - это объект, который определяет контекст выполнения операций в конструкции with.
Задача менеджера контекста выполнить определенные операции в начале блока with, и в конце.

Чаще всего, менеджер контекста вызывается с помощью блока with, но может использоваться и вызывая его методы напрямую.

Один из самых распространенных примеров использования конструкции with - работа с файлами.

> Весь код находится в [репозитории](https://github.com/natenka/natenka.github.io/tree/master/code_examples/python_with)

Пример открытия файла:
```python
In [1]: with open('r1.txt') as f:
   ...:     for line in f:
   ...:         print(line, end='')
   ...:
```

Именно эта конструкция обычно используется, чтобы открыть файл, что-то сделать с содержимым и затем закрывать файл.

В данном случае, после завершения конструкции with, файл автоматически закроется:
```python
In [1]: with open('r1.txt') as f:
   ...:     for line in f:
   ...:         print(line, end='')
   ...:
...

In [2]: f.closed
Out[2]: True
```

Обратите внимание, что переменная f доступна за пределами конструкции f, так как with не создает отдельного пространства имен, как функция.

Внутри конструкции with происходит следующее:
```python
In [19]: f = open('r1.txt').__enter__()

In [20]: for line in f:
    ...:     print(line, end='')
    ...:
...

In [21]: f.__exit__()

In [23]: f.closed
Out[23]: True
```

Метод ```__enter__``` вызывается в самой конструкции with.
Если в with есть выражение ```as```, результат выполнения метода, присваивается в переменную, которая указана после  ```as```.

Потом выполняются какие-то действия, которые находятся в блоке with.

И в конце вызывается метод ```__exit__```.
В данном случае, этот метод закрывает файл.

В примере с файлом, метод ```__exit__``` гарантирует закрытие файла, независимо от того, было ли исключение в блоке with.


### Генератор и @contextlib.contextmanager

В Python существует целый модуль для работы с менеджерами контекста - contextlib.

Например, в этом модуле находится декоратор @contextlib.contextmanager, который позволяет создавать менеджер контекста из генератора.


Простой пример:
```python
import contextlib

@contextlib.contextmanager
def lines():
    print('-'*10, 'START', '-'*10)
    yield
    print('-'*11, 'END', '-'*11)
```

Генератор должен выдавать только одно значение.
При этом то, что находится до yield, будет выполняться в начале блока with.
А то, что находится после yield - в конце.

Использование функции lines() выглядит таким образом:
```python
with lines():
    print('inside with block')

print('outside')
```

Результат выполнения:
```python
$ python with_simple.py
---------- START ----------
inside with block
----------- END -----------
outside
```

## SQLite и with

### Выполнение транзакции в блоке with

При работе с SQLite, Python позволяет использовать объект Connection, как менеджер контекста.

Пример использования соединения с базой, как менеджера контекста (файл with_sqlite3_transaction.py):
```python
# -*- coding: utf-8 -*-
import sqlite3

data = [('00:19:FF:3D:D6:58', '10.1.10.33', '10', 'FastEthernet0/3'),
       #('00:09:BB:3D:D6:58', '10.1.15.55', '15', 'FastEthernet0/17'),
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
```

В блоке with в БД добавляются данные. При этом:
* при возникновении исключения, транзакция автоматически откатывается
* если исключения не было, автоматически выполняется commit

До выполнения скрипта в таблице dhcp такие записи:
```
$ sqlite3 dhcp_snooping.db
-- Loading resources from /home/vagrant/.sqliterc

SQLite version 3.8.7.1 2014-10-29 13:59:56
Enter ".help" for usage hints.
sqlite> select * from dhcp;
mac                ip          vlan        interface
-----------------  ----------  ----------  ---------------
00:09:BB:3D:D6:58  10.1.10.2   10          FastEthernet0/1
00:04:A3:3E:5B:69  10.1.5.2    5           FastEthernet0/1
00:05:B3:7E:9B:60  10.1.5.4    5           FastEthernet0/9
00:09:BC:3F:A6:50  10.1.10.6   10          FastEthernet0/3
sqlite>
```

Результат выполнения:
```
$ python with_sqlite3_transaction.py
Запись данных прошла успешно
('00:09:BB:3D:D6:58', '10.1.10.2', '10', 'FastEthernet0/1')
('00:04:A3:3E:5B:69', '10.1.5.2', '5', 'FastEthernet0/10')
('00:05:B3:7E:9B:60', '10.1.5.4', '5', 'FastEthernet0/9')
('00:09:BC:3F:A6:50', '10.1.10.6', '10', 'FastEthernet0/3')
('00:19:FF:3D:D6:58', '10.1.10.33', '10', 'FastEthernet0/3')
('00:14:33:FE:5B:69', '10.1.15.2', '15', 'FastEthernet0/12')
('00:15:BF:7E:9B:60', '10.1.15.4', '15', 'FastEthernet0/6')
```

Если теперь раскомментировать строку в списке кортежей data, будет возникать исключение, так как MAC-адрес в этой строке совпадает с уже существующим в таблице, а поле mac является primary key и поэтому должно быть уникальным:
```python
$ sqlite3 dhcp_snooping.db
-- Loading resources from /home/vagrant/.sqliterc

SQLite version 3.8.7.1 2014-10-29 13:59:56
Enter ".help" for usage hints.
sqlite> .schema dhcp
CREATE TABLE dhcp (
    mac          text not NULL primary key,
    ip           text,
    vlan         text,
    interface    text
);
```

Чтобы еще раз попробовать добавить данные, надо раскомментировать строку в списке data и вернуть БД в исходное состояние:
```
$ cp dhcp_snooping_backup.db dhcp_snooping.db

$ python with_sqlite3_transaction.py
Error occured:  UNIQUE constraint failed: dhcp.mac
('00:09:BB:3D:D6:58', '10.1.10.2', '10', 'FastEthernet0/1')
('00:04:A3:3E:5B:69', '10.1.5.2', '5', 'FastEthernet0/10')
('00:05:B3:7E:9B:60', '10.1.5.4', '5', 'FastEthernet0/9')
('00:09:BC:3F:A6:50', '10.1.10.6', '10', 'FastEthernet0/3')
```

При добавлении данных возникло исключение UNIQUE constraint failed и транзакция откатилась.
Поэтому в таблице остались те же записи, которые были до попытки добавить новую информацию.

Содержимое таблицы dhcp до и после добавления информации - одинаково. Это значит, что не записалась ни одна строка из списка data.

Так получилось из-за того, что используется метод executemany и в пределах одной транзакции мы пытаемся записать все 4 строки. Если возникает ошибка с одной из них - откатываются все изменения.

Иногда, это именно то поведение, которое нужно. Если же надо чтобы игнорировались только строки с ошибками, надо использовать метод execute и записывать каждую строку отдельно.

### Соединение с БД в блоке with

В sqlite3 with используется только для работы с транзакциями.

И хотя соединение тоже можно открывать в блоке with (файл with_sqlite_conn.py):
```python
import sqlite3

with sqlite3.connect('dhcp_snooping.db') as conn:
    for row in conn.execute('select * from dhcp'):
        print(row)
```

На самом деле, после этого блока соединение не закрыто:
```python
In [1]: import sqlite3

In [2]: with sqlite3.connect('dhcp_snooping.db') as conn:
   ...:     for row in conn.execute('select * from dhcp'):
   ...:         print(row)
   ...:
('00:09:BB:3D:D6:58', '10.1.10.2', '10', 'FastEthernet0/1')
('00:04:A3:3E:5B:69', '10.1.5.2', '5', 'FastEthernet0/10')
('00:05:B3:7E:9B:60', '10.1.5.4', '5', 'FastEthernet0/9')
('00:09:BC:3F:A6:50', '10.1.10.6', '10', 'FastEthernet0/3')

In [3]: conn.execute('select * from dhcp')
Out[3]: <sqlite3.Cursor at 0xb5705660>
```

Поэтому лучше не открывать соединение таким образом, так как создается впечатление, что оно будет автоматически закрыто.

Но, можно создать свой менеджер контекста, который будет закрывать соединение:
```python
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
```

Теперь запрос в блоке try не выполнится, так как соединение уже закрыто:
```
$ python with_sqlite3_conn_contextmanager.py
('00:09:BB:3D:D6:58', '10.1.10.2', '10', 'FastEthernet0/1')
('00:04:A3:3E:5B:69', '10.1.5.2', '5', 'FastEthernet0/10')
('00:05:B3:7E:9B:60', '10.1.5.4', '5', 'FastEthernet0/9')
('00:09:BC:3F:A6:50', '10.1.10.6', '10', 'FastEthernet0/3')
Cannot operate on a closed database.
```

### contextlib.closing

В модуле contextlib есть менеджер контекста closing, который вызывает метод close, в конце блока with.

Соответственно, в предыдущем примере можно не создавать менеджер контекста, а использовать closing (файл with_sqlite3_conn_closing.py):
```python
import contextlib
import sqlite3


with contextlib.closing(sqlite3.connect('dhcp_snooping.db')) as conn:
    for row in conn.execute('select * from dhcp'):
        print(row)

try:
    conn.execute('select * from dhcp')
except sqlite3.ProgrammingError as e:
    print(e)
```

Результат выглядит аналогично:
```
$ python with_sqlite3_conn_closing.py
('00:09:BB:3D:D6:58', '10.1.10.2', '10', 'FastEthernet0/1')
('00:04:A3:3E:5B:69', '10.1.5.2', '5', 'FastEthernet0/10')
('00:05:B3:7E:9B:60', '10.1.5.4', '5', 'FastEthernet0/9')
('00:09:BC:3F:A6:50', '10.1.10.6', '10', 'FastEthernet0/3')
Cannot operate on a closed database.
```


### Соединение SSH в блоке with

И напоследок еще одна идея для использования менеджера контекста - подключение по SSH с помощью netmiko (файл with_netmiko_contextmanager.py):
```python
import contextlib
import netmiko

@contextlib.contextmanager
def ssh_connection(device_params):
    connection = netmiko.ConnectHandler(**device_params)
    yield connection
    connection.disconnect()

DEVICE_PARAMS = {'device_type': 'cisco_ios',
                 'ip': '192.168.100.1',
                 'username': 'cisco',
                 'password': 'cisco',
                 'secret': 'cisco' }

with ssh_connection(DEVICE_PARAMS) as ssh:
    ssh.enable()
    result = ssh.send_command("sh ip int br")
    print(result)


try:
    ssh.send_command("sh ip int br")
except OSError as e:
    print(e)
```

Выполнение выглядит так:
```
$ python with_netmiko_contextmanager.py
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
Ethernet0/2                19.1.1.1        YES NVRAM  up                    up
Ethernet0/3                192.168.230.1   YES NVRAM  up                    up
Socket is closed
```

Последнее сообщение появляется из-за того что в блоке try метод send_command выполняется на закрытом соединении.


### Дополнительные материалы

Все примеры выше использовались чтобы показать простейшие примеры использования и заинтересовать этой темой.
Ссылки для погружения в тему ниже.

Документация:

* [The with statement](https://docs.python.org/3/reference/compound_stmts.html#with)
* [contextlib — Utilities for with-statement contexts](https://docs.python.org/3/library/contextlib.html)
* [PyMOTW: contextlib — Context Manager Utilities](https://pymotw.com/3/contextlib/)
* [PEP 343 -- The "with" Statement](https://www.python.org/dev/peps/pep-0343/)

Статьи:

* [The Python "with" Statement by Example](http://preshing.com/20110920/the-python-with-statement-by-example/)

Ответ на stackoverflow:

* [What is the python “with” statement designed for?](https://stackoverflow.com/questions/3012488/what-is-the-python-with-statement-designed-for)

В книге Fluent Python этой теме посвящен 15 раздел:

* [Fluent Python. Chapter 15 Context Managers and else Blocks](http://shop.oreilly.com/product/0636920032519.do)
* [Примеры из книги](https://github.com/fluentpython/example-code/tree/master/15-context-mngr)

