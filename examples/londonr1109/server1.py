'''
Test JSONRPC Server implementing a function for retriving annualized rolling volatility
'''
PORT = 8080
HOST = 'localhost'

from twisted.web2 import server, channel
from twisted.internet import reactor
from jsonrpc import jsonrpc
import roll


class JsonService(jsonrpc):
    
    def __init__(self):
        jsonrpc.__init__(self)
    
    def jsonrpc_mean(self, request, ticker, window = 20):
        return roll.mean.get(ticker,window = window)


site = server.Site(JsonService())
reactor.listenTCP(PORT, channel.HTTPFactory(site))
print("Simple JSON RPC server running on %s:%s" % (HOST,PORT))
reactor.run()
    

