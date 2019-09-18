from mayeye import Request,Response,config
import time,random
class MiddleWare():
    def __init__(self):
        self.next=None
        pass
    def link(self,next:__init__):

        print(type(next))
        self.next=next
        pass

    def run(self,req:Request,res:Response):
        tip =self.handel(req,res)

        if tip == -1:
            if self.next != None:
                self.next.run()
    # 所有的middlewaredou要重写这个handle方法，使用责任链模式对数据进行处理
    def handel(self,req:Request,res:Response)->int:
        return -1
class Session(object):
    def __init__(self):
        self.lastVisitTime = time.time()#以秒为单位的时间
        self.deleyTime = config.sessionTime
        self.session = {}
    def getter(self,k):
        if time.time()-self.lastVisitTime>self.deleyTime:
            print("session 过期")
            self.session = {}
        self._visit()
        if k in self.session:
            return self.session[k]
        else:
            return None
    def setter(self,k,v):
        self._visit()
        self.session.update(k,v)
    def _visit(self):
        self.lastVisitTime = time.time()

# 具体的中间件只需要考虑中间件对请求做什么，就可以
class SessionMiddleWare(MiddleWare):
    def __init__(self):
        MiddleWare.__init__(self)#对父类初始化
        self.sessionPool={}
    # 为请查看session和创建session
    def handel(self,req:Request,res:Response)->int:
        if hasattr(req,"cookie")==False:
            sessionID = self._genSessionId()
            session = Session()
            self.sessionPool.update({sessionID: session})
            req.session = session
            res.addCookie("sessionID", sessionID)
            return -1
        if "sessionID" in req.cookie:#请求中是否有sessionId
            sessionID = req.cookie["sessionID"]
            if sessionID in self.sessionPool:#服务器池中是否有sessionID
                req.session = self.sessionPool[sessionID]
                req.session.visit()
            else:
                sessionID = self._genSessionId()
                session = Session()
                self.sessionPool.update({sessionID:session})
                req.session = session
                res.addCookie("sessionID", sessionID)
        else:
            sessionID = self._genSessionId()
            session = Session()
            self.sessionPool.update({sessionID:session})
            req.session = session
            res.addCookie("sessionID", sessionID)
        return -1
    #用随机函数生成一个sessioonid
    def _genSessionId(self):
        stime = str(int(time.time()))
        srandom = str(random.randint(0,100000))
        s = stime+srandom
        return hash(s)

