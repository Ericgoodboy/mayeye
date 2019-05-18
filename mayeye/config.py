#用于配置相关数据
import os
from mayeye.middlewares import SessionMiddleWare
import pymysql
#from mayeye.Models import Session
#staticPath = [os.path.abspath("F:/2018/code/vue")]
staticPath = [os.path.abspath("../static")]

sessionTime = 60*60*3#3小时
debug = True
middleWares = [
    SessionMiddleWare()
]
#models = [Session()]
database = {#暂时只支持pymysql
    "db":"test",
    "username":"root",
    "host":"127.0.0.1",
    "pwd":"19980321hq."
}
