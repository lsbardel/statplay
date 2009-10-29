'''
Requires python 2.6 or higher
'''
import json        
from datetime import date, datetime


class JSONEncodeException(Exception):
    '''JSON RPC encode error'''
    pass

class ServiceException(Exception):
    pass

class BadServiceRequest(ServiceException):
    pass

class ServiceMethodNotFound(ServiceException):
    pass

class ServiceRequestNotTranslatable(ServiceException):
    pass


class JSONRPCEncoder(json.JSONEncoder):
    """
    Provide custom serializers for JSON-RPC.
    """
    def default(self, obj):
        if isinstance(obj, date):
            return obj.strftime("%Y%m%d")
        elif isinstance(obj, datetime):
            return obj.strftime("%Y%m%dT%H:%M:%S")
        else:
            raise JSONEncodeException("%r is not JSON serializable" % (obj,))
        

def dumprequest(obj, **kwargs):
    '''
    dumps a request for JSON RPC server
    '''
    if isinstance(obj, Exception):
        err = {'name':       obj.__class__.__name__,
               'message':    obj.message}
        result = None
    else:
        err    = None
        result = obj
    res = {'error':  err,
           'result': result,
           'id':     id,
           'time':   tim}
    try:
        return json.dumps(res, cls=JSONRPCEncoder, **kws)
    except JSONEncodeException, e:
        return dumps(e, id, **kws)
 
        
def dumps(obj, **kws):
    '''
    Modify JSON dumps method
    '''
    if isinstance(obj, Exception):
        err = {'name':       obj.__class__.__name__,
               'message':    str(obj)}
        result = None
    else:
        err    = None
        result = obj
    res = {'error':  err,
           'result': result}
    try:
        return json.dumps(res, cls=JSONRPCEncoder, **kws)
    except JSONEncodeException, e:
        return dumps(e)


def loads(string, **kwargs):
    '''
    Modify JSON loads method
    '''
    resp = json.loads(string, **kwargs)
    err  = resp.get('error',None)
    if err != None:
        ename  = err.get('name',None)
        if ename:
            errore = globals()[str(ename)]
        else:
            error = Exception
        raise errore(err.get('message',None))
    else:
        return resp.get('result',None)
    

class SimpleParser(object):
    
    def __init__(self):
        self.buffer = ''

    def feed(self, data):
        self.buffer += data