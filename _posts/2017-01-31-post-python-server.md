---
title:  "TCP-Server and Client на Python"
search: false
categories:
  - Jekyll
---

Данная статья в рамках обучения по курсу Python. Описывает процесс создания простейшего tcp сервера, 
слушающего соединения на порту и отправляющего в ответ на соединение response ответ, и клиента, 
отправляющего presence сообщение.

В дальнейшем это будет чат-сервер. Для обмена будет использоваться JIM IM Protocol.

Клиент посылает серверу presence сообщение следующего формата:
```
presence = \
        {
            "action": "presence",
            "time": int(time.time()),
            "type": "status",
            "user": {"account_name": str(self.nickname),
                     "status": str(self.status)
                     }
        }
```
Сервер отправляет клиенту ответ (на данном этапе сервер никак не проверяет сообщение от пользователя)
```
response_200 = \
            {
                "response": 200,
                "time": int(time.time()),
                "alert": "OK"
            }
```

Немного о сокетах. Сокет – это объект, напоминающий файл, позволяющий программе принимать входящие
соединения, устанавливать исходящие соединения, а также отправлять и принимать данные. Прежде
чем два компьютера смогут обмениваться информацией, на каждом из них должен быть создан объект
сокета.
Компьютер, принимающий соединение, (сервер) должен присвоить своему объекту сокета
определенный номер порта. На стороне сервера, работающего по протоколу TCP, объект сокета, используемый 
для приема запросов на соединение, – это не тот же самый сокет, что в дальнейшем используется для обмена
данными с клиентом. В частности, системный вызов accept() возвращает новый объект сокета, который
фактически будет использоваться для обслуживания соединения. Это позволяет серверу
одновременно обслуживать соединения с большим количеством клиентов.
При определении сокета задаем какой сетевой протокол будет использоваться.
server_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
В оснвновном используется AF_INET - Протокол IPv4 (TCP, UDP) и AF_INET6 Протокол IPv6 (TCP, UDP).
Типы сокетов
SOCK_STREAM - Поток байтов с поддрежкой логического соединения, обеспечивающего надженость передачи данных (TCP)
SOCK_DGRAM - Дейтаграммы (UDP)
SOCK_RAW Простой сокета
SOCK_RDM Дейтаграммы с надежной доставкой
SOCK_SEQPACKET - Обеспечивает последовательную передачу записей с поддержкой логических соединений



Класс TCP Server
```
import socket
import json
import time

class CServer:
    def __init__(self, config):
        self.config = config
        try:
            self._server_sock = /
            socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)  # TCP
            self._server_sock.bind(config)
            self._server_sock.listen(5)
        except OSError as err:
            pass

    def response(self):
        '''
        Сообщение-ответ

        '''
        response_200 = \
            {
                "response": 200,
                "time": int(time.time()),
                "alert": "OK"
            }
        return response_200

    def recieve_data(self, sock):
        '''
        Получение данных от ответа. Парсинг данных.
        '''
        try:
            data = sock.recv(1024)
            data_decode = json.loads(data.decode())
            return data_decode
        except OSError as err:
            pass

    def send_data(self, sock, msg):
        '''
        Отправка данных клиенту
          '''
        msg = json.dumps(msg).encode()
        try:
            sock.send(msg)
        except OSError as err:
            pass

    def main(self):
        '''
        Ожидание подключения. Прием данных от сервера. Отправка ответа клиенту.
        '''
        while 1:
            try:
                sock, addr = self._server_sock.accept()
                print(sock)
                print(addr)
                data = self.recieve_data(sock)
                print("К серверу присоединился клиент {}".format(data['user']['account_name']))
                print(data)
                resp = self.response()
                self.send_data(sock, resp)
            except OSError as err:
                pass
```

Класс TCP клиента
```
import socket
import json
import time

class CClient:
    '''
    Класс для клиента
    '''
    def __init__(self, nickname, status, config):
        try:
            self._sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)

        except socket.error as err:
            print("Ошибка создания сокета: {}".format(err))
        self.nickname = nickname
        self.status = status
        self.config = config
        self.main()

    def connect_srv(self):
        '''
        Функция для соединения с сервером. Отправялет presence-сообщение серверу. 
        Получает ответ и выводит его.
        '''
        try:
            self._sock.connect(self.config)
            presence = self.presence_msg()
            self.send_msg(presence)
            data = self.recieve_data()
            print(data)
        except OSError as err:
            print('Ошибка соединения с сервером')

    def send_msg(self, msg):
        '''
        Функция отправляет данные серверу
        '''
        msg = json.dumps(msg).encode()
        try:
            self._sock.send(msg)
        except OSError as err:
            pass

    def recieve_data(self):
        '''
        Функция для приема данных от сервера
        '''
        try:
            data = self._sock.recv(1024)
            data_decode = json.loads(data.decode())
            return data_decode
        except OSError as err:
            pass

    def presence_msg(self):
        '''
        Функция формирует presence-сообщение серверу для уведомления о своем присутствии
        '''

        presence = \
            {
                "action": "presence",
                "time": int(time.time()),
                "type": "status",
                "user": {"account_name": str(self.nickname),
                         "status": str(self.status)
                         }
            }
        return presence

    def main(self):
        self.connect_srv()
```

Теперь листинг приложений

Сервер
```
import sys
import re
import TCP.tcp_server as serv

#server_sock.settimeout(5)

if __name__ == "__main__":

    ipv4_address = /
    re.compile('^(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
    patern_port = re.compile('[80-65536]')
    argv = sys.argv[1:]

    if len(argv) == 0:
        config = ("0.0.0.0", 7777)
    else:
        if ipv4_address.match(argv[1]):
            if len(argv) == 1:
                    config = (sys.argv[1], 7777 )
            if len(argv) == 2:
                if patern_port.match(argv[2]):
                    config = (argv[1].strip(), argv[2].strip())

    server = serv.CServer(config)
```
Клиент
```
if __name__ == "__main__":

    ipv4_address = /
    re.compile('^(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
    patern_port = re.compile('[80-65536]')
    argv = sys.argv[1:]
    config =  ()
    if len(argv) == 0:
        print("Не введены параметры подключения")
    else:
        if ipv4_address.match(argv[0]):
            if len(argv) == 1:
                    config = (sys.argv[1], 7777 )
            if len(argv) == 2:
                if patern_port.match(argv[2]):
                    config = (argv[1].strip(), argv[2].strip())

            nick = input("Введите имя пользователя: ")
            status = input("Введите ваш статус: ")
            print(config)
            client = cl.CClient(nick, status, config)
```
