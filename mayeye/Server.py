from mayeye.Response import Response
from mayeye.Request import Request
import _thread
from socket import *
import time
from mayeye.urls import urls
from mayeye.util import log
from mayeye import config
class HttpServer(object):
    def __init__(self,ip_port=("0.0.0.0", 80)):
        self.back_log = 5  # 连接池
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(ip_port)
        self.handleMap ={}
        self.loadMiddleWare()
        log("开始监听")
    def loadMiddleWare(self):
        if len(config.middleWares)<=0:
            return
        self.headMiddleWare= config.middleWares[0]
        nowMiddleWare = self.headMiddleWare
        for middle in config.middleWares[1:]:
            nowMiddleWare.link(middle)
            nowMiddleWare = middle

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
                response = Response(conn)
                self.handleRequest(request,response)#将response传给handler进行
                log("{0} {1} {2} {3}".format(request.method,request.path,request.args["host"],time.time()-start_time))
            _thread.start_new_thread(f, (conn,))
    def handleRequest(self,req: Request,res:Response):
        self.doMiddleWare(req,res)
        if res.sended:
            return
        self.doHandelList(req,res)
        if res.sended:
            return
        self.doHandleStatic(req,res)
        if res.sended:
            return
        res.make404Response()
    def doMiddleWare(self,req: Request,res:Response):
        self.headMiddleWare.run(req,res)
    def doHandleStatic(self,req: Request,res:Response):#静态获取
        path = req.path

        if path.endswith("/"):
            path += "/index.html"
        res.makeStaticResponse("./"+path)

    def doHandelList(self,req: Request,res:Response):
        path=req.path.lstrip("/")
        log("--------------------- "+path)
        if path in urls:
            urls[path](req,res)

if __name__ == '__main__':
    server = HttpServer()
    server.listen()