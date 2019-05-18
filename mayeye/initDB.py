from mayeye import config
import pymysql
from mayeye.Models import test
def createDatabase():
    host = config.database["host"]
    db = config.database["db"]
    username = config.database["username"]
    pwd = config.database["pwd"]
    connect = pymysql.connect(host,username,pwd,db)
    i=test()
    print(i.createString())
    res=connect.query(i.createString())
    print("res:",str(res))
    connect.close()
if __name__ == '__main__':
    createDatabase()