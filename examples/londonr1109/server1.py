'''
Test JSONRPC Server implementing a function for retriving annualized rolling volatility
'''
import sys
from twisted.web2 import server, channel
from jsonrpc import jsonrpc
import roll


class JsonService(jsonrpc):
    
    def jsonrpc_mean(self, request, ticker, window = 20):
        return roll.mean.get(ticker,window = window)


if __name__ == '__main__':
    from twisted.internet import reactor
    site = server.Site(JsonService())
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except:
            pass
    reactor.listenTCP(port, channel.HTTPFactory(site))
    print("LondonR Nov-09 simple JSON RPC server running on localhost:%s" % port)
    reactor.run()
