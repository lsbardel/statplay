'''
Minimalistic JSON RPC Server implementation using twisted.web2
'''
from twisted.web2 import resource, stream
from twisted.web2 import responsecode, http, http_headers
from twisted.internet import defer, protocol
from twisted.python import log, reflect
from jsonlib import *


def rpcfunction(f, method, *args, **kwargs):
    '''
    Decorator for jsonrpc functions
    '''
    def wrapper(request):
        log.msg('Accessing remote function %s' % method)
        try:
            res = f(request, *args, **kwargs)
        except Exception, e:
            raise BadServiceRequest(str(e))
        return res
    
    return wrapper



class jsonrpc(resource.Resource):
    '''
    Minimalistic class for handling JSON server objects
    '''
    addSlash  = True
    prefix    = 'jsonrpc'
    
    def __init__(self):
        resource.Resource.__init__(self)
        
    def http_POST(self, request):
        '''
        Handle post request
        '''
        parser = SimpleParser()
        deferred = stream.readStream(request.stream, parser.feed)
        deferred.addCallback(lambda x: self._cbDispatch(request, parser))
        deferred.addErrback(self._ebRender)
        deferred.addCallback(self._cbRender, request)
        return deferred
    
    def _cbDispatch(self, request, parser):
        function = self.make_function(parser.buffer)
        return defer.maybeDeferred(function, request)

    def _cbRender(self, result, request):
        s = dumps(result)
        return http.Response(responsecode.OK,
                             {'content-type': http_headers.MimeType('text', 'json')},
                              s)

    def _ebRender(self, failure):
        obj = failure.value
        return obj
    
    def listFunctions(self):
        """
        Return a list of the names of all jsonrpc methods.
        """
        return reflect.prefixedMethodNames(self.__class__, self.prefix)
        
    def make_function(self, data):
        method, args, kwargs = self.get_method_and_args(data)
        kwstr = {}
        for k,v in kwargs.items():
            kwstr[str(k)] = v
        function = self.get_function(method)
        return rpcfunction(function, method, *args, **kwstr)
    
    def handleRequest(self, json):
        '''
        handle a new request
        '''
        err    = None
        result = None
        id     = self.idmaker()
        tim    = datetime.now()
        
        try:
            req = self.translateRequest(json)
        except ServiceRequestNotTranslatable, e:
            err = e

        if err==None:
            try:
                methName = req['method']
                args     = req['params']
            except:
                err = BadServiceRequest(json)
                
        if err == None:
            try:
                meth = self.findServiceEndpoint(methName)
            except Exception, e:
                err = e

        if err == None:
            try:
                result = self.invokeServiceEndpoint(meth, args)
            except Exception, e:
                err = e

        resultdata = self.translateResult(result, err, id_)

        return resultdata

    def get_method_and_args(self, data):
        req    = loads(data)
        method = req['method']
        args   = req['args']
        kwargs = req['kwargs']
        return method, args, kwargs
    
    def get_function(self, functionPath):
        """
        Given a string, return a function, or raise ValueError.
        """
        f = getattr(self, "%s_%s" % (self.prefix,functionPath), None)
        if not f:
            msg = "function %s not found" % functionPath
        elif not callable(f):
            msg = "function %s not callable" % functionPath
        else:
            return f
        raise ValueError(msg)
    
    def translateRequest(self, data):
        try:
            req = loads(data)
        except:
            raise ServiceRequestNotTranslatable(data)
        return req

    def invokeServiceEndpoint(self, meth, args):
        return meth(*args)