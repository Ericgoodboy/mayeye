import math
def func(string:str):
    j=list(string)
    mapc = {}
    for i in j:
        if i in mapc:
            mapc[i]+=1
        else:
            mapc[i]=1
    des = 1
    for i in mapc:
        nn = mapc[i]
        k = 1
        for j in range(1, nn + 1):
            k *= j
        des *= k
    m=string.lower()
    c=list(m)
    s = set("aeio")
    x = 0
    y = 0
    for i in c:

        if i not in s:
            x+=1
        else:
            y+=1

    #print(x,y)
    if x<y-1:
        return 0
    num = math.pow(y+1,x-y+1)

    #print(y+1,x-y+1)
    if x-y+1==0:
        num=1
    nx=1
    ny=1
    for i in range(1,x+1):
        nx*=i
        if i==y:
            ny=nx
    # for i in range(1,y+1):
    #     nx*=i
    print(nx,ny,num)
    if y==0:
        return nx/des
    if y==1:
        return nx*(x+1)
    return nx*ny*num/des
# line = "aefgh"
# print(int(func(line)))
import sys
n = int(sys.stdin.readline().strip())
for i in range(n):
        # 读取每一行
        line = sys.stdin.readline().strip()

        print(int(func(line)))
