import netmiko
from pprint import pprint

#subgenerator
def send_show_command(device_params):
    command = yield
    print('Opening connection to IP: {}'.format(device_params['ip']))
    conn = netmiko.ConnectHandler(**device_params)
    conn.enable()
    command_result = {}
    while True:
        if command is None:
            conn.disconnect()
            print('Connection closed')
            break
        print(command)
        output = conn.send_command(command)
        command_result[command] = output
        command = yield
    return command_result


#delegating generator
def collect_output(results, device_params):
    while True:
        print('*'*40)
        results[device_params['ip']] = yield from send_show_command(device_params)


#caller
def main(devices, commands):
    results = {}
    for device in devices:
        collect = collect_output(results, device)
        next(collect)
        for command in commands:
            collect.send(command)
        collect.send(None)
    return results


r1 = {'device_type': 'cisco_ios',
      'ip': '192.168.100.1',
      'username': 'cisco',
      'password': 'cisco',
      'secret': 'cisco' }
r2 = {'device_type': 'cisco_ios',
      'ip': '192.168.100.2',
      'username': 'cisco',
      'password': 'cisco',
      'secret': 'cisco' }


all_devices = [r1, r2]
commands = ['sh ip arp', 'sh ip int br']

result = main(all_devices, commands)

for device, command in result.items():
    print(' IP: {} '.format(device).center(50,'#'))
    for c, output in command.items():
        print(' Command: {} '.format(c).center(50,'#'))
        print(output)


