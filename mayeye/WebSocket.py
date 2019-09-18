from socket import *
import _thread
def log(*args):
    print(*args)

ip_port = ("127.0.0.1",1923)
class WebSocket(object):
    def __init__(self):
        self.back_log = 5  # 连接池
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(ip_port)
        self.handleMap = {}
        #self.loadMiddleWare()
        log("开始监听")
    def listen(self):
        self.server.listen(self.back_log)
        while True:
            conn, addr = self.server.accept()
            log("接收到来自：" + str(addr) + "的消息:")
            def f(conn):
                data = conn.recv(10000)
                log(data.decode("utf-8"))
                conn.send("hello world".encode("utf-8"))
            _thread.start_new_thread(f, (conn,))
if __name__ == '__main__':
    ws = WebSocket()
    ws.listen()
