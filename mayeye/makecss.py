import random
with open("F:/2019/mayeye/static/css/star.css", "w")as f:
    temp = []
    for i in range(30):

        index = i+1
        top = random.randint(5,90)
        left = random.randint(20,60)
        arr = [index,top,left]
        temp.append(arr)
    temp.sort(key=lambda x:x[2])

    for i in temp:
        string = ".star:nth-child({0})<top:{1}%;left:{2}%;animation-delay:{3}s;>\n"
        left = i[2] - 20;
        dely = (left/40)*6
        i.append(dely)
        string = string.format(*i)
        string = string.replace("<","{").replace(">","}")
        print(string)
        f.writelines(string)