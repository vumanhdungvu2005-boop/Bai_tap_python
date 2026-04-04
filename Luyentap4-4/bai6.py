_list = ['abc', 'xyz', 'aba', '1221', 'ii', 'ii2', '5yhy5']

n = 4
count = 0

for s in _list:
    if len(s) >= n and s[0] == s[-1]:
        count += 1

print("Kết quả:", count)