import urllib2

from jsonlib import *

class ServiceProxy(object):
    '''
    Proxy for JSON remote calls
    '''
    separator  = '.'
    
    def __init__(self, url, name = None):
        self.__url   = url
        self.__name  = name

    def __getattr__(self, name):
        return ServiceProxy(self.__url, name)

    def __call__(self, *args, **kwargs):
        func_name = self.__name
        data = {'method': func_name,
                'args':   args,
                'kwargs': kwargs}
        postdata = dumps(data)
        respdata = urllib2.urlopen(self.__url, postdata).read()
        return loads(respdata)
