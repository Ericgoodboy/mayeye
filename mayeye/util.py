from datetime import datetime
from mayeye import config


def getTimeString(date=0,hour=0,minute=0,second=0):
    time=second+minute*60+hour*60*60+date*60*60*24
    GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
    date = datetime.fromtimestamp(datetime.utcnow().timestamp()+time)
    return date.strftime(GMT_FORMAT)

def log(obj):
    if config.debug:
       print(obj)