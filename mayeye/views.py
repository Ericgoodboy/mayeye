from mayeye.Response import Response
from mayeye.Request import Request


def api(req:Request,res:Response):
    res.body="{hello}"
    res.send()
    return -1