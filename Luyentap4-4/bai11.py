_list = ['apple', 'cat', 'banana', 'dog']

n = int(input("Nhập n: "))

_new = []

for i in _list:
    if len(i) <= n:
        _new.append(i)

print(_new)