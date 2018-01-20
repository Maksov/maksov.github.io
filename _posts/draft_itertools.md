## Модуль itertools

В Python есть отдельный модуль itertools в котором находятся итераторы и средства работы с ними.

Например, в этом модуле есть бесконечные итераторы:
* count() - этот итератор возвращает номера, начиная с указанного и используя указанный шаг
* cycle() - повторяет циклически элементы
* repeat() - повторяет элемент


### count

Пример count():
```python
In [21]: import itertools

In [22]: count_nums = itertools.count(0,2)

In [23]: count_nums
Out[23]: count(0, 2)

In [24]: for _ in range(10):
    ...:     print(next(count_nums))
    ...:
0
2
4
6
8
10
12
14
16
18

```

Например, count может пригодиться в zip, чтобы сгенерировать номера элементов:
```python
In [25]: nums = list(range(100, 201, 10))

In [26]: nums
Out[26]: [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]

In [27]: list(zip(itertools.count(), nums))
Out[27]:
[(0, 100),
 (1, 110),
 (2, 120),
 (3, 130),
 (4, 140),
 (5, 150),
 (6, 160),
 (7, 170),
 (8, 180),
 (9, 190),
 (10, 200)]
```

### cycle

Пример использования cycle():
```python
In [28]: cycle_letters = itertools.cycle('ABCD')

In [29]: for _ in range(10):
    ...:     print(next(cycle_letters))
    ...:
A
B
C
D
A
B
C
D
A
B

```

### islice

Функция islice создает итератор, который возвращает элементы итерируемого объекта.
Она поддерживает такой же синтаксис, как и функция range:
```python
In [30]: from itertools import islice

In [31]: islice(range(100,200,5), 5)
Out[31]: <itertools.islice at 0xb4f6c57c>

In [32]: list(islice(range(100,200,5), 5))
Out[32]: [100, 105, 110, 115, 120]

In [33]: list(islice(range(100,200,5), 5, 10))
Out[33]: [125, 130, 135, 140, 145]

In [34]: list(islice(range(100,200,5), 5, 10, 2))
Out[34]: [125, 135, 145]

```

> islice не поддерживает отрицательные индексы


С помощью функций, которые находятся в модуле itertools, можно создавать полезные функции для работы с итерируемыми объектами или итератораторами.

Пример из документации модуля:
```python
In [35]: from itertools import islice

In [36]: def take(n, iterable):
    ...:     "Return first n items of the iterable as a list"
    ...:     return list(islice(iterable, n))
    ...:
```

Функция take возвращает указанное количество элементов из итерируемого объекта:
```python
In [37]: a = [1,2,3,4,5,6,7,8]

In [38]: b = range(100,200,5)

In [39]: take(5, a)
Out[39]: [1, 2, 3, 4, 5]

In [40]: take(5, b)
Out[40]: [100, 105, 110, 115, 120]

```

