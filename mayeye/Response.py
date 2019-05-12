import time
from mayeye import config
import os
import mime
from mayeye import util
from socket import socket
class Response():
    def __init__(self,conn:socket = None):
        self.conn = conn
        self.contentType = 'text/html'
        self.httpVersion = "HTTP/1.1"
        self.statusCode = 200
        self.date =self._getFormatTime()
        self.body = "<h1>helloWord</h1>"
        self.file = b''
        self.headers={
            "Accept-Encoding":"gzip, deflate, br"
        }
        self.cookie = {
            "add":100
        }
    def _getFormatTime(self):
        s = time.asctime()
        # a = s.split(" ")
        # d = (a[0],a[3],a[1],a[5],a[4])
        return s
    def encodeStr(self,encoding='utf-8')->bytearray:
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        headers=""
        for i in self.headers:
            headers+="\r\n"+i+" "+":"+self.headers[i]
        cookie=""
        for k in self.cookie:
            temp="\r\nSet-Cookie: {k}={v}; expires={time}; path=/; domain=127.0.0.1;"
            v=self.cookie[k]
            time = util.getTimeString(date=1)
            cookie+=temp.format(k=k,v=v,time=time)
        tempStr = "{version} {statusCode} OK\r\nDate: {date}\r\nContent-Type: {contentType}; charset=UTF-8{headers}{cookie}\r\n\r\n{body}"
        resStr = tempStr.format(version=self.httpVersion,statusCode=self.statusCode,date=self.date,body = self.body,headers = headers,cookie=cookie,contentType=self.contentType)
        return resStr.encode(encoding)+self.file

    def addCookie(self,k,v):
        self.cookie.update({k:v})
    @classmethod
    def create404Response(cls):
        res = Response()
        res.body = '<h1>404 not found</h1>'
        res.statusCode = 404
        return res
    @classmethod
    def createFileResponse(cls,path,contentType):
        data=b''
        if os.path.isfile(path):
            with open(path,'rb') as f:
                while True:
                    d = f.read(1024)
                    if d:
                        data+=d
                    else:
                        break
            res = Response()
            res.body = ''
            res.file = data
            res.contentType = contentType
        else:
            res = Response.create404Response()
        return res

    @classmethod
    def createStaticReaponse(cls,suburl):
        paths = [os.path.join(i,suburl)for i in config.staticPath]
        for path in paths:
            if os.path.isfile(path):
                contentType = mime.Types.of(path)[0].content_type
                return Response.createFileResponse(path,contentType)
        return -1
