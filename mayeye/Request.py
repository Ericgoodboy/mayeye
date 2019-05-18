from mayeye.util import log
class Request(object):
    def __init__(self,data):
        try:
            requestString = data.decode("utf-8")
            arr = requestString.split("\r\n")
            self.requestString=requestString
            print("requestString",requestString)
            reqLine = arr[0].split(" ")
            print("reqLine",reqLine)
            if len(reqLine) <= 1:
                self.code = -1
                return
            self.method = reqLine[0]
            self.path = reqLine[1]
            self.httpVersion = reqLine[2]
            self.body = requestString.split("\r\n\r\n")[1]
            self.args = {}
            self.session = None
            for i in arr[1:-2]:
                att = i.split(":")
                k=att[0].strip().lstrip().lower()
                v=att[1].strip().lstrip()
                if k in self.args:
                    self.args[k].append(v)
                else:
                    self.args[k]=[v]
            for k in self.args:
                if len(self.args[k])==1:
                    self.args[k] = self.args[k][0]
            self._genCookie()
            self.code =1
        except Exception as e:
            requestString = data.decode("utf-8")
            print("requestStringeee",requestString)
            self.code = -1
    # def __init__(self):
    #     self.method = "GET"
    #     self.path = "/"
    #     self.httpVersion = "Http/1.1"
    #     self.body = ""
    #     self.host=""
    #     self.args = {}
    #     pass

    def _analysis(self):
        pass
    def _genCookie(self):
        if "cookie" in self.args:
            cookieString = self.args["cookie"]
            cookies = cookieString.split(";")
            self.cookie={}
            for cookie in cookies:
                kvs = cookie.split("=")
                k=kvs[0].strip().lstrip()
                v=kvs[1].strip().lstrip()
                self.cookie[k] = v
            log(self.cookie)
        else:
            pass
    def _ansBody(self):
        pass