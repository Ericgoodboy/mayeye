from mayeye.Response import Response
from mayeye.Request import Request
from PIL import ImageGrab
from mayeye import config
import os
def api(req:Request,res:Response):
    res.body="{hello}"
    res.send()
    return -1

def deskTop(req:Request,res:Response):
    img = ImageGrab.grab()
    path =os.path.abspath(os.path.join(config.staticPath[1],"temp.jpg"))
    print("cuting")
    with open(path,"wb") as f:
        img.save(f,format="jpeg")
    res.makeStaticResponse("temp.jpg")