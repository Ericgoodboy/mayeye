import pymysql
from mayeye import config
class Field():

    def __init__(self):
        self._value = ""
        self._saveValue=""
        self.formatdict={}
        self.unset = False
        pass
    def setValue(self,value):
        self._value = value
        self._saveValue = "'"+value+"'"
    def getValue(self):
        return self._value
    def getSaveValue(self):
        return self._saveValue
    def getFieldInfo(self,**kwargs)->str:
        pass
    def setName(self,name:str):
        self.name = name
        self.formatdict.update({"name":name})
class TextField(Field):
    def __init__(self,**kwargs):
        Field.__init__(self)
        self.formatdict = {
            "length": kwargs["maxLength"],
            "not_null": " not null" if "not_null" in kwargs and kwargs["not_null"] else '',
            "unique": " unique" if "unique" in kwargs and kwargs["unique"] else "",
            "pk": "primary key" if "pk" in kwargs and kwargs["pk"] else ""
        }
    def getSaveValue(self):
        return "'"+self.getValue()+"'"
    def getFieldInfo(self)->str:
        temp = "{name} varchar({length}){not_null}{unique} {pk}"
        return temp.format(**self.formatdict).strip()
class IntegerField(Field):
    def __init__(self,**kwargs):
        Field.__init__(self)
        self.formatdict = {
            "length": kwargs["maxLength"],
            "not_null": " not null" if "not_null" in kwargs and kwargs["not_null"] else '',
            "unique": " unique" if "unique" in kwargs and kwargs["unique"] else "",
            "pk": "primary key" if "pk" in kwargs and kwargs["pk"] else ""
        }
    def getFieldInfo(self)->str:
        temp = "{name} varchar({length}){not_null}{unique} {pk}"
        return temp.format(**self.formatdict).strip()
class Model():
    def __init__(self):
        host = config.database["host"]
        db = config.database["db"]
        username = config.database["username"]
        pwd = config.database["pwd"]
        self.conn = pymysql.connect(host, username, pwd, db)
        self._nameToField()
    def all(self):
        pass
    def find(self,**kwargs):
        # print(kwargs)
        equal = [k for k in kwargs if not k.startswith("_")]
        unequel = [k for k in kwargs if k.startswith("_")]
    def fieldString(self):
        fields = []
        self.name = "_".join(str(self.__class__).replace("<class '", "").replace("'>", "").split("."))
        for i in self.__dir__():
            if not i.startswith("__"):
                if isinstance(self.__getattribute__(i),Field):
                    field = self.__getattribute__(i)

                    fields.append(field.getFieldInfo())
        return ",\n".join(fields)
    def _nameToField(self):
        fields = {}
        print("setting name------------------------,")
        self.name = "_".join(str(self.__class__).replace("<class '", "").replace("'>", "").split("."))
        for i in self.__dir__():
            if not i.startswith("__"):
                if isinstance(self.__getattribute__(i), Field):
                    field = self.__getattribute__(i)
                    field.setName(i)
                    fields.update({i:field})
        self.fields=fields
    def createString(self):
        temp = "create table if not exists {table_name} (\n{fieldString}\n)"

        formatDict={
            "table_name":self.name,
            "fieldString":self.fieldString()
        }
        return temp.format(**formatDict)
    @classmethod
    def createOne(cls,**kwargs):
        res = cls()
        resdict = dir(res)
        resdict = [i for i in resdict if isinstance(getattr(res,i),Field)]
        for k in kwargs:
            if k in resdict:
                getattr(res,k).setValue(kwargs[k])
        return res
    def save(self):
        saveString = "INSERT INTO {table_name} ({keys}) VALUES ({values});"
        k=[self.fields[f].name for f in self.fields if self.fields[f].unset==False]
        v=[self.fields[f].getSaveValue() for f in self.fields if self.fields[f].unset==False]
        k=",".join(k)
        v=",".join(v)
        fdict = {
            "table_name": self.name,
            "keys":k,
            "values":v
        }
        saveString = saveString.format(**fdict)
        print(saveString)
        print(self.conn.query(saveString))
    def __del__(self):
        self.conn.close()

class Session(Model):
    date = TextField(maxLength=100)
    sessionID = TextField(maxLength=50)
    def __init__(self):
        Model.__init__(self)
        pass
    def __str__(self):
        return "session"

class test(Model):
    date = TextField(maxLength=100)
    uid = TextField(maxLength=50,unique=True)
    def __init__(self):
        Model.__init__(self)

    def __str__(self):
        return "session"

class User(Model):

    uname = TextField(maxLength=40)
    def __init__(self):
        Model.__init__(self)



if __name__ == '__main__':
    a = Session()

    print(Session.createOne())