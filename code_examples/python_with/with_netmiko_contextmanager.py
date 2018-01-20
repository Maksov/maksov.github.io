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


