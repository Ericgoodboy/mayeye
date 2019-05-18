from mayeye import Request,Response,config
import time
class MiddleWare():
    def __init__(self):
        self.next=None
        pass
    def link(self,next:__init__):

        print(type(next))
        self.next=next
        pass
    def run(self,req:Request,res:Response):
        res =self.handel(req,res)
        if res == -1:
            if self.next != None:
                self.next.run()
    def handel(self,req:Request,res:Response)->int:

        return -1
class Session(object):
    def __init__(self):
        self.lastVisitTime = time.time()#以秒为单位的时间
        self.deleyTime = config.sessionTime
        self.session = {}
    def getter(self,k):
        if k in self.session:
            return self.session[k]
        else:
            return None
    def setter(self,k,v):
        self.session.update(k,v)
    def visit(self):
        self.lastVisitTime = time.time()


class SessionMiddleWare(MiddleWare):
    def __init__(self):
        MiddleWare.__init__(self)
        self.sessionPool={}
    def handel(self,req:Request,res:Response)->int:
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

    def _genSessionId(self):
        import time,random
        stime = str(int(time.time()))
        srandom = str(random.randint(0,100000))
        s = stime+srandom
        return hash(s)

