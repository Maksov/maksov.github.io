import netmiko
from pprint import pprint

#subgenerator
def send_show_command(device_params):
    #print('*'*40)
    print('Opening connection to IP: {}'.format(device_params['ip']))
    conn = netmiko.ConnectHandler(**device_params)
    conn.enable()
    command_result = {}
    while True:
        command = yield
        if command is None:
            conn.disconnect()
            print('Connection closed')
            break
        print(command)
        output = conn.send_command(command)
        command_result[command] = output
        #print(output)
    #print('Subgenerator:', command_result)
    return command_result

def send_show_command2(device_params):
    print('Opening connection to IP: {}'.format(device_params['ip']))
    conn = netmiko.ConnectHandler(**device_params)
    conn.enable()
    command_result = {}
    while True:
        try:
            command = yield
            output = conn.send_command(command)
            command_result[command] = output
        except GeneratorExit:
            conn.disconnect()
            print('Connection closed')
            print(command_result)
            return command_result

def send_show_command3(device_params):
    #print('*'*40)
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
        #print(output)
    #print('Subgenerator:', command_result)
    return command_result


#delegating generator
def collect_output(results, device_params):
    while True:
        print('*'*40)
        print('delegating generator')
        #pprint(results)
        #results[device_params['ip']] = yield from send_show_command(device_params)
        #results[device_params['ip']] = yield from send_show_command2(device_params)
        results[device_params['ip']] = yield from send_show_command3(device_params)


#caller
def main(devices, commands):
    results = {}
    for device in devices:
        collect = collect_output(results, device)
        next(collect)
        for command in commands:
            collect.send(command)
        collect.send(None)
        #collect.close()
        #print('Caller:', results)
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
pprint(result)
