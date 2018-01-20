import contextlib

@contextlib.contextmanager
def lines():
    print('-'*10, 'START', '-'*10)
    yield
    print('-'*11, 'END', '-'*11)

with lines():
    print('inside with block')


print('outside')
