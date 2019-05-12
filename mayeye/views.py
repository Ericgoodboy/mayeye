from mayeye.Response import Response
from mayeye.Request import Request


def api(req:Request)->Response:
    res =Response()
    res.body="{hello}"
    return res