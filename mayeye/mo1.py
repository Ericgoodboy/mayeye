def func(string:str):
    temp = list(string)
    flag=0

    stopWord = set("-., !\t\\")
    res = []
    for i in temp:
        if flag ==0:
            if i in stopWord:
                res.append(i)
                flag = 0
            else:
                res.append(i.upper())
                flag=1
            continue
        if flag ==1:
            if i in stopWord:
                res.append(i)
                flag = 0
            else:
                res.append(i.lower())
    return "".join(res)

import sys
line =sys.stdin.readline().strip()
#line = "A"
print(func(line))