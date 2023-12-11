import hashlib

input = "yzbqklnj"

for i in range(10000000):
    m = hashlib.md5()
    m.update((input + str(i)).encode("utf-8"))
    if m.hexdigest().startswith("00000"):
        print(i)
        break
    
for i in range(10000000):
    m = hashlib.md5()
    m.update((input + str(i)).encode("utf-8"))
    if m.hexdigest().startswith("000000"):
        print(i)
        break
