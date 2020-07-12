a = open("text/text1.txt")
print(type(a))
b = a.read().lower()
a = ''
for i in b:
    if(ord('a') <= ord(i) <= ord('z') or ord('A') <= ord(i) <= ord('Z')):
        pass
    else:
        a += i
print(a)
