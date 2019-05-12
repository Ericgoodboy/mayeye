from mayeye import Request,Response
class MiddleWare():
    def __init__(self):
        self.next=None
        pass
    def link(self,next:__init__):

        print(type(next))
        self.next=next
        pass
    def run(self,req:Request)->Response:
        res =self.handel()
        if res==-1:
            if self.next==None:
                return -1
            else:
                return self.next.run(req)
        return res
    def handel(self,req:Request)->Response:

        return -1


class SessionMiddleWare(MiddleWare):
    def handel(self, req: Request) -> Response:

        return -1
