---
title: Книга "Python для сетевых инженеров" переведена на Python 3.6
date: 2017-09-01
comments: true
category:
 - pyneng
tags:
 - pyneng-book
 - python3
---

Спустя 240 часов и плюс 250 страниц - это свершилось :)

В книге есть два типа изменений: из-за перехода на Python 3 и не связанные с переходом.
Фактически, большинство изменений не связаны с переходом и просто являются улучшениями книги.

Тем не менее, все примеры, весь код, все задания и все темы обновлены до Python 3.6.
Эти изменения перечислены в отдельном разделе, чтобы было легче перейти со Python 2.7 на Python 3.

> Теперь версия для Python 3.6 используется как основная. И на неё можно перейти с [главной страницы книги на GitBook](https://www.gitbook.com/book/natenka/pyneng/details).

## Что изменилось

### Обновленные разделы

* Полностью переписан раздел [Регулярные выражения](https://natenka.gitbooks.io/pyneng/content/book/09_regex/) - раздел стал больше, подробнее расписан синтаксис регулярных выражений и добавлены примеры. Кроме того, дополнена часть по самому модулю re и подробней описаны его функции
* Раздел по [базам данных](https://natenka.gitbooks.io/pyneng/content/book/11_db/) частично переписан - немного улучшился код примеров, а также более четко разделен на части сам раздел
* Раздел по [Ansible](https://natenka.gitbooks.io/pyneng/content/book/15_ansible/) обновлен до Ansible 2.4
* [Подраздел JSON](https://natenka.gitbooks.io/pyneng/content/book/10_serialization/2_json.html) обновлен - добавлена информация про конвертацию типов данных Python в JSON и наоборот

### Добавлены подразделы

* [Итераторы и comprehensions](https://natenka.gitbooks.io/pyneng/content/book/16_additional_info/iterator_generator/)
* [Основы Git и GitHub](https://natenka.gitbooks.io/pyneng/content/book/01_intro/git-github/)
* [Распаковка переменных](https://natenka.gitbooks.io/pyneng/content/book/16_additional_info/variable_unpacking.html)
* [concurrent.futures](https://natenka.gitbooks.io/pyneng/content/book/12_ssh_telnet/concurrent_futures/)
* [Unicode](https://natenka.gitbooks.io/pyneng/content/book/16_additional_info/unicode/)
* [Объединение литералов строк](https://natenka.gitbooks.io/pyneng/content/book/03_data_structures/4c_string_literal_concatenation.html)


### Добавлена информация про функции

* [print](https://natenka.gitbooks.io/pyneng/content/book/07_functions/useful_functions/print.html)
* [range](https://natenka.gitbooks.io/pyneng/content/book/07_functions/useful_functions/range.html)


### Добавлена информация про модули

* [tabulate](https://natenka.gitbooks.io/pyneng/content/book/08_modules/useful_modules/tabulate.html)
* [pprint](https://natenka.gitbooks.io/pyneng/content/book/08_modules/useful_modules/pprint.html)


Подразделы "Полезные функции" и "Полезные модули" перенесены из раздела "Дополнительная информация" в разделы [Функции](https://natenka.gitbooks.io/pyneng/content/book/07_functions/useful_functions/) и [Модули](https://natenka.gitbooks.io/pyneng/content/book/08_modules/useful_modules/), соответственно.

### Задания

* добавлено 5 заданий в 12 раздел
* добавлено 1 задание в 8 раздел
* удалено задание 10.2

Теперь в книге 116 заданий.

### Изменения из-за перехода на Python 3.6

Изменений достаточно мало.
Все они описаны в [книге](https://natenka.gitbooks.io/pyneng/content/book/16_additional_info/py2_vs_py3.html) с ссылками на соответствующие разделы.

### Новое в книге

* Добавлена информация про [отличия книги py2 и py3](https://natenka.gitbooks.io/pyneng/content/book/16_additional_info/py2_vs_py3.html)
* Во все разделы добавлен подраздел "Дополнительные материалы" с ссылками для дополнительного изучения темы
* Примеры и упражнения вынесены в отдельный [репозиторий](https://github.com/natenka/pyneng-examples-exercises)
* Для всех тем есть [презентации](https://github.com/natenka/pyneng-slides)
* Для некоторых тем есть [тесты](https://github.com/natenka/pyneng-examples-exercises/blob/master/tests.md)
* Подготовлены [виртуалки для Python 3.6](https://natenka.gitbooks.io/pyneng/content/book/01_intro/) - кроме того, перечислены пару вариантов облачных сервисов
* Добавлен раздел [Продолжение обучения](https://natenka.gitbooks.io/pyneng/content/resources/) - в этом разделе перечислены ресурсы по которым можно продолжать обучение.


## О книге

Суть книги не изменилась - это книга по основам Python.
Её главная задача объяснить основы питон на понятных задачах и примерах.
Вам даже не нужно читать всю книгу, чтобы начать использовать Python.

Задача книги не в том, чтобы после прочтения вы начали парсить вручную вывод команд или всё делать самописными скриптами.
Если у вас есть возможность использовать какой-то управляющий софт - лучше использовать его.
Если у оборудования есть нормальный API - используйте его.

Задача книги помочь в освоении основ Python.
Примеры показаны на сетевых задачах, чтобы помочь разобраться, лучше усвоить информацию и на понятных практических примерах разобраться с Python.



## Книга для Python 2.7

Предыдущая версия книги по-прежнему [доступна](https://natenka.gitbooks.io/pyneng/content/v/python2.7/).
Со временем, в эту версию будут перенесены те изменения из книги для Python 3.6, которые не касаются изменений в Python 3.


