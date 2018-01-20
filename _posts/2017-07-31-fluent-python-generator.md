---
title: "Fluent Python: generator"
date: 2017-07-31
tags:
 - links
 - notes
 - fluent-python
 - pyneng
category:
 - python
---

Небольшая заметка о генераторах (generator) с примером использования.

Сейчас я читаю книгу [Fluent Python](http://shop.oreilly.com/product/0636920032519.do) и, чтобы повторить пройденную тему, решила придумать пару примеров.


## generator (генератор)

Генераторы - это специальный класс функций, который позволяет легко создавать свои итераторы.
В отличии от обычных функций, генератор не просто возвращает значение и завершает работу, а возвращает итератор, который отдает элементы по одному.

> Более корректное определение: функция-генератор - это функция, в которой присутствует ключевое слово yield. При вызове, эта функция возвращает объект генератор. Так как и сама функция и объект, который она возвращает, называется генератор, возникает путанница, о чем идет речь.
> В документации Python очень часто объект генератор называется итератором. Поэтому тут я тоже буду называть возвращенный объект итератором, а функцию - генератором.

Обычная функция завершает работу если:
* встретилось выражение return
* закончился код функции (это срабатывает как выражение ```return None```)
* возникло исключение

После выполнения функции, управление возвращается и программа выполняется дальше.
Все аргументы, которые передавались в функцию, локальные переменные, все это теряется.
Остается только результат, который вернула функция.

Функция может возвращать список элементов, несколько объектов или возвращать разные результаты, в зависимости от аргументов, но она всегда возвращает какой-то один результат.

Генератор же генерирует значения.
При этом, значения возвращаются по запросу и после возврата одного значения, выполнение функции-генератора приостанавливается до запроса следующего значения.
Между запросами генератор сохраняет свое состояние.


С точки зрения синтаксиса, генератор выглядит как обычная функция.
Но, вместо return, используется оператор ```yield```.

Каждый раз, когда внутри функции встречается yield, генератор приостанавливается и возвращает значение.
При следующем запросе, генератор начинает работать с того же места, где он завершил работу в прошлый раз.

Так как yield не завершает работу генератора, он может использоваться несколько раз.

### Базовый пример

Рассмотрим простой пример генератора:
```python
In [1]: def generate_nums(number):
   ...:     print('Start of generation')
   ...:     yield number
   ...:     print('Next number')
   ...:     yield number+1
   ...:     print('The end')
   ...:
```

Если вызвать генератор и присвоить результат в переменную, его код еще не будет выполняться:
```python
In [3]: result = generate_nums(100)
```

Теперь в переменной result находится итератор:
```python
In [4]: result
Out[4]: <generator object generate_nums at 0xb5788e9c>
```

Раз result это итератор, можно вызвать функцию next, чтобы получить значение:
```python
In [5]: next(result)
Start of generation
Out[5]: 100
```

После первого вызова next, генератор выполнил все строки до первого yield.
В данном случае, отобразилась строка 'Start of generation'.
Затем yield вернул значение - число 100.

Второй вызов next:
```python
In [6]: next(result)
Next number
Out[6]: 101
```

Выполнение продолжилось с предыдущего места - выведена строка 'Next number' и вернулось значение 101.

Следующий next:
```python
In [7]: next(result)
The end
------------------------------------------------------------
StopIteration              Traceback (most recent call last)
<ipython-input-7-1b214ba10814> in <module>()
----> 1 next(result)

StopIteration:
```

Так как в result находится итератор, когда элементы заканчиваются, он генерирует исключение StopIteration.
Но, до этого, вывелась строка 'The end'.

Раз функция-генератор возвращает итератор, его можно использовать в цикле:
```python
In [8]: for num in generate_nums(100):
   ...:     print('Number:', num)
   ...:
Start of generation
Number: 100
Next number
Number: 101
The end
```

### Обычная функция и аналогичный генератор

С помощью генераторов зачастую можно написать ту же функцию с меньшим количеством промежуточных переменных.

Например, функцию такого вида:
```python
In [14]: def work_with_items(items):
    ...:     result = []
    ...:     for item in items:
    ...:         result.append('Changed {}'.format(item))
    ...:     return result
    ...:

In [15]: for i in work_with_items(range(10)):
    ...:     print(i)
    ...:
Changed 0
Changed 1
Changed 2
Changed 3
Changed 4
Changed 5
Changed 6
Changed 7
Changed 8
Changed 9
```

Можно заменить таким генератором:
```python
In [16]: def yield_items(items):
    ...:     for item in items:
    ...:         yield 'Changed {}'.format(item)
    ...:

In [17]: for i in yield_items(range(10)):
    ...:     print(i)
    ...:
Changed 0
Changed 1
Changed 2
Changed 3
Changed 4
Changed 5
Changed 6
Changed 7
Changed 8
Changed 9
```

При этом, генератор yield_items возвращает элементы по одному, а функция work_with_items - собирает их в список, а потом возвращает.
Если количество элементов небольшое, это не существенно.
Но, при обработке больших объемов данных, лучше работать с элементами по одному.

При этом, в любой момент, если действительно нужно получить все элементы, например, в виде списка, это можно сделать применив функцию list:
```python
In [20]: result =  yield_items(range(10))

In [21]: result
Out[21]: <generator object yield_items at 0xb579053c>

In [22]: list(result)
Out[22]:
['Changed 0',
 'Changed 1',
 'Changed 2',
 'Changed 3',
 'Changed 4',
 'Changed 5',
 'Changed 6',
 'Changed 7',
 'Changed 8',
 'Changed 9']
```

### Использование генератора, при работе с файлами

Например, при обработке большого log-файла, лучше обрабатывать его построчно, не выгружая все содержимое в память.

Допустим, нам нужно часто фильтровать определенные строки из файла.
Например, надо получить только строки, которые соответствуют регулярному выражению.
Конечно, можно каждый раз это делать в процессе обработки строк.
Но можно вынести подобную функциональность и в отдельную функцию.

Но только, в случае обычной функции, придется опять возвращать список или подобный объект.
А, если файл очень большой, то, скорее всего, придется отказаться от этой затеи.

Однако, если использовать генератор, файл будет обрабатываться построчно.
Это может быть, например, такой генератор:
```python
In [3]: import re

In [5]: def filter_lines(filename, regex):
   ...:     with open(filename) as f:
   ...:         for line in f:
   ...:             if re.search(regex, line):
   ...:                 yield line.rstrip()
   ...:
```

Генератор проходится по указанному файлу и отдает те строки, которые совпали с регулярным выражением.

Пример использования:
```python
In [7]: for line in filter_lines('config_r1.txt', '^interface'):
   ...:     print(line)
   ...:
interface Loopback0
interface Tunnel0
interface Ethernet0/0
interface Ethernet0/1
interface Ethernet0/2
interface Ethernet0/3
interface Ethernet0/3.100
interface Ethernet1/0
```

### Пример использования генератора для обработки вывода sh cdp neighbors detail

Генераторы могут использоваться не только в том случае, когда надо возвращать элементы по одному.

Например, генератор get_cdp_neighbor читает файл с выводом sh cdp neighbor detail и выдает вывод частями, по одному соседу:
```python
def get_cdp_neighbor(sh_cdp_neighbor_detail):
    with open(sh_cdp_neighbor_detail) as f:
        line = ''
        while True:
            while not 'Device ID' in line:
                line = f.readline()
            neighbor = ''
            neighbor += line
            for line in f:
                if line.startswith('-----'):
                    break
                neighbor += line
            yield neighbor
            line = f.readline()
            if not line:
                return
```

Полный скрипт выглядит таким образом (файл parse_cdp_file.py):
```python
import re
from pprint import pprint

def get_cdp_neighbor(sh_cdp_neighbor_detail):
    with open(sh_cdp_neighbor_detail) as f:
        line = ''
        while True:
            while not 'Device ID' in line:
                line = f.readline()
            neighbor = ''
            neighbor += line
            for line in f:
                if line.startswith('-----'):
                    break
                neighbor += line
            yield neighbor
            line = f.readline()
            if not line:
                return


def parse_cdp(output):
    regex = ('Device ID: (?P<device>\S+)'
             '|IP address: (?P<ip>\S+)'
             '|Platform: (?P<platform>\S+ \S+),'
             '|Cisco IOS Software, (?P<ios>.+), RELEASE')

    result = {}

    match_iter = re.finditer(regex, output)
    for match in match_iter:
        if match.lastgroup == 'device':
            device = match.group(match.lastgroup)
            result[device] = {}
        elif device:
            result[device][match.lastgroup] = match.group(match.lastgroup)

    return result


filename = 'sh_cdp_neighbors_detail.txt'
result = get_cdp_neighbor(filename)

all_cdp = {}
for cdp in result:
    all_cdp.update(parse_cdp(cdp))

pprint(all_cdp)
```

Так как генератор get_cdp_neighbor выдает каждый раз вывод про одного соседа, можно проходиться по результату в цикле и передавать каждый вывод функции parse_cdp.

И конечно же, полученный результат тоже можно не собирать в один большой словарь, а передавать куда-то дальше на обработку или запись.

Результат выполнения:
```
$ python parse_cdp_file.py
{'R1': {'ios': '3800 Software (C3825-ADVENTERPRISEK9-M), Version 12.4(24)T1',
        'ip': '10.1.1.1',
        'platform': 'Cisco 3825'},
 'R2': {'ios': '2900 Software (C3825-ADVENTERPRISEK9-M), Version 15.2(2)T1',
        'ip': '10.2.2.2',
        'platform': 'Cisco 2911'},
 'R3': {'ios': '2900 Software (C3825-ADVENTERPRISEK9-M), Version 15.2(2)T1',
        'ip': '10.3.3.3',
        'platform': 'Cisco 2911'},
 'SW2': {'ios': 'C2960 Software (C2960-LANBASEK9-M), Version 12.2(55)SE9',
         'ip': '10.1.1.2',
         'platform': 'cisco WS-C2960-8TC-L'}}
```


## dropwhile и takewhile из модуля itertools

В Python есть отдельный модуль itertools в котором находятся итераторы и средства работы с ними.

Используя функции dropwhile и takewhile из модуля itertools, можно значительно сократить код в функции get_cdp_neighbor.

#### dropwhile

Функция dropwhile ожидает как аргументы функцию, которая возвращает True или False, в зависимости от условия, и итерируемый объект.
Функция dropwhile отбрасывает элементы итерируемого объекта до тех пор, пока функция переданная как аргумент возвращает True.
Как только dropwhile встречает False, он возвращает итератор с оставшимися объектами.

Пример:
```python
In [1]: from itertools import dropwhile

In [2]: list(dropwhile(lambda x: x < 5, [0,2,3,5,10,2,3]))
Out[2]: [5, 10, 2, 3]
```

В данном случае, как только функция dropwhile дошла до числа, которое больше или равно пяти, она вернула все оставшиеся числа.
При этом, даже если далее есть числа, которые меньше 5, функция уже не проверяет их.

#### takewhile

Функция takewhile є абсолютная противоположность функции dropwhile: она возвращает итератор с теми элементами, которые соответствуют условию, до первого ложного условия:
```python
In [3]: from itertools import takewhile

In [4]: list(takewhile(lambda x: x < 5, [0,2,3,5,10,2,3]))
Out[4]: [0, 2, 3]
```


### Пример использования takewhile и dropwhile

Генератор get_cdp_neighbor, который использовался ранее, возвращает вывод sh cdp neighbors detail по одному соседу.

Логика функции была такая:
* сначала надо отбросить все, пока не встретится строка с Device ID
* затем надо взять все строки, пока не встретится строка с '-----'
* потом начать все с начала

В прошлом варианте эта функциональность реализована циклами.
Но первое условие - это именно то, что делает функция dropwhile, а второе - то, что делает функция takewhile.

В итоге, генератор выглядит так:
```python
def get_cdp_neighbor(sh_cdp_neighbor_detail):
    with open(sh_cdp_neighbor_detail) as f:
        while True:
            begin = dropwhile(lambda x: not 'Device ID' in x, f)
            lines = takewhile(lambda y: not '-----' in y, begin)
            neighbor = ''.join(lines)
            if not neighbor:
                return
            yield neighbor
```

Остальные части скрипта никак не поменялись (файл parse_cdp_file_ver2.py):
```python
import re
from pprint import pprint
from itertools import dropwhile, takewhile

def get_cdp_neighbor(sh_cdp_neighbor_detail):
    with open(sh_cdp_neighbor_detail) as f:
        while True:
            f = dropwhile(lambda x: not 'Device ID' in x, f)
            lines = takewhile(lambda y: not '-----' in y, f)
            neighbor = ''.join(lines)
            if not neighbor:
                return
            yield neighbor


def parse_cdp(output):
    regex = ('Device ID: (?P<device>\S+)'
             '|IP address: (?P<ip>\S+)'
             '|Platform: (?P<platform>\S+ \S+),'
             '|Cisco IOS Software, (?P<ios>.+), RELEASE')

    result = {}

    match_iter = re.finditer(regex, output)
    for match in match_iter:
        if match.lastgroup == 'device':
            device = match.group(match.lastgroup)
            result[device] = {}
        elif device:
            result[device][match.lastgroup] = match.group(match.lastgroup)

    return result


filename = 'sh_cdp_neighbors_detail.txt'
result = get_cdp_neighbor(filename)

all_cdp = {}
for cdp in result:
    all_cdp.update(parse_cdp(cdp))

pprint(all_cdp)
```


Результат аналогичный:
```
$ python parse_cdp_file_ver2.py
{'R1': {'ios': '3800 Software (C3825-ADVENTERPRISEK9-M), Version 12.4(24)T1',
        'ip': '10.1.1.1',
        'platform': 'Cisco 3825'},
 'R2': {'ios': '2900 Software (C3825-ADVENTERPRISEK9-M), Version 15.2(2)T1',
        'ip': '10.2.2.2',
        'platform': 'Cisco 2911'},
 'R3': {'ios': '2900 Software (C3825-ADVENTERPRISEK9-M), Version 15.2(2)T1',
        'ip': '10.3.3.3',
        'platform': 'Cisco 2911'},
 'SW2': {'ios': 'C2960 Software (C2960-LANBASEK9-M), Version 12.2(55)SE9',
         'ip': '10.1.1.2',
         'platform': 'cisco WS-C2960-8TC-L'}}
```


## generator expression (генераторное выражение)

Генераторное выражение использует такой же синтаксис, как list comprehentions, но возвращает итератор, а не список.

Генераторное выражение выглядит точно так же, как list comprehentions, но используются круглые скобки:
```python
In [1]: genexpr = (x**2 for x in range(10000))

In [2]: genexpr
Out[2]: <generator object <genexpr> at 0xb571ec8c>

In [3]: next(genexpr)
Out[3]: 0

In [4]: next(genexpr)
Out[4]: 1

In [5]: next(genexpr)
Out[5]: 4
```

Обратите внимание, что это не tuple comprehentions, а генераторное выражение.

Оно полезно в том случае, когда надо работать с большим итерируемым объектом или бесконечным итератором.

## Дополнительные материалы

Документация:

* [Iterator types](https://docs.python.org/3/library/stdtypes.html#iterator-types)
* [Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html)
* [itertools](https://docs.python.org/3/library/itertools.html#module-itertools)
* [PyMOTW itertools](https://pymotw.com/3/itertools/)


Статьи:

* [Iterables vs. Iterators vs. Generators](http://nvie.com/posts/iterators-vs-generators/)
* [Improve Your Python: 'yield' and Generators Explained](https://jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/) - generator and generator expressions
* [Generator Tricks for Systems Programmers. David Beazley](http://www.dabeaz.com/generators/)

Ответ на stackoverflow:

* [Difference between Python's Generators and Iterators](https://stackoverflow.com/questions/2776829/difference-between-pythons-generators-and-iterators)
* [Understanding Generators in Python](https://stackoverflow.com/questions/1756096/understanding-generators-in-python)
* [What can you use Python generator functions for?](https://stackoverflow.com/questions/102535/what-can-you-use-python-generator-functions-for)


В книге Fluent Python этой теме посвящен 14 раздел:

* [Fluent Python. Chapter 14 Iterables, Iterators, and Generators](http://shop.oreilly.com/product/0636920032519.do)
* [Примеры из книги](https://github.com/fluentpython/example-code/tree/master/14-it-generator)

