import re
def make(filePath):
    fileString  = ""
    restr = "asmdcasmdckapwsodkcsavdmafmvpoawspdocpsldvpasdp"
    with open(filePath,"r") as f:
        for i in f.readlines():
            fileString+=i
    ma = re.compile('\d+ of 200 DOCUMENTS')
    arr = ma.findall(fileString)
    for i in arr:
        fileString=fileString.replace(i,restr)
    ss = fileString.split(restr)
    ext = re.compile('exclusive')
    for i in range(1,201):
        excl="false"
        if len(ext.findall(ss[i]))>0:
            excl = "true"
        ss[i] = ss[i].replace("</SPAN>","",1).replace("</P>","",1).replace("</DIV>","",1)
        t = "<h1>"+str(i)+" of 200 DOCUMENTS</h1><br>"+("<h1>exclusive:%5s</h1>"%excl)+"<a href = './" +str(i+1)+".html'><h3>next Page</h3></a>"+ss[i]
        with open("../files/"+str(i)+".html","w") as f:
            f.write(t)


if __name__ == '__main__':
    filePath = "F:\\2019\mayeye\\temp\\1.HTML"
    make(filePath)