import netmiko

def send_show_command(device_params):
    print('Open connection to: '.rjust(40, '#'),
          device_params['ip'])
    conn = netmiko.ConnectHandler(**device_params)
    conn.enable()
    result = None
    while True:
        try:
            command = yield result
            result = conn.send_command(command)
        except GeneratorExit:
            conn.disconnect()
            print('Connection closed'.rjust(40, '#'))
            break


r1 = {'device_type': 'cisco_ios',
      'ip': '192.168.100.1',
      'username': 'cisco',
      'password': 'cisco',
      'secret': 'cisco' }

commands = ['sh ip int br', 'sh ip arp']

ssh = send_show_command(r1)
next(ssh)

for c in commands:
    result = ssh.send(c)
    print(result)

ssh.close()

