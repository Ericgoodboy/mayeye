from mayeye.Response import Response
from mayeye.Request import Request
import _thread
from socket import *
import time
from mayeye.urls import urls
from mayeye.util import log
class HttpServer(object):
    def __init__(self,ip_port=("127.0.0.1", 8080)):
        self.back_log = 5  # 连接池
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(ip_port)
        self.handleMap ={}
        log("开始监听")
    def listen(self):
        self.server.listen(self.back_log)
        while True:
            conn, addr = self.server.accept()
            log("接收到来自："+str(addr)+ "的消息:")
            def f(conn):
                start_time = time.time()
                data = conn.recv(10000)
                request = Request(data)
                if request.code == -1:
                    log("failed"+data.decode("utf-8"))
                    conn.close()
                    return
                response = self.handleRequest(request)
                conn.send(response.encodeStr())
                conn.close()
                log("{0} {1} {2} {3}".format(request.method,request.path,request.args["host"],time.time()-start_time))
            _thread.start_new_thread(f, (conn,))
    def handleRequest(self,req: Request)->Response:

        res =Response.createStaticReaponse("."+req.path)
        if res == -1:
            res = self.doHandelList(req)
        if res == -1:
            res = Response.create404Response()
        return res
    def _getFormatTime(self):
        import time
        s = time.asctime()
        a = s.split(" ")
        d = (a[0],a[3],a[1],a[5],a[4])
        return " ".join(d)
    def doHandelList(self,req: Request):
        res =-1
        path=req.path.lstrip("/")
        log("--------------------- "+path)
        if path in urls:
            res = urls[path](req)
        return res
if __name__ == '__main__':
    server = HttpServer()
    server.listen()