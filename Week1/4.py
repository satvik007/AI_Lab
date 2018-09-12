filename = "fileName.txt"

ans = 0
flag = False

with open(filename) as f:
  while True:
    c = f.read(1)
    if not c:
      break
    
    if(c == ' ' or c == '\t' or c == '\n'):
        flag = False
    else:
        if flag:
            continue
        else:
            ans += 1
            flag = True

print(int(ans))

