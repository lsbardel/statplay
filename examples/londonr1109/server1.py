'''
Test JSONRPC Server implementing a function for retriving simple moving averages
'''
import sys
from twisted.web2 import server, channel
from twisted.python import log
from jsonrpc import jsonrpc
import roll


class JsonService(jsonrpc):
    
    def jsonrpc_mean(self, request, ticker, window = 20):
        '''
        Call roll.mean function
        '''
        return roll.mean.get(ticker, window = window)


if __name__ == '__main__':
    '''
    Start the server
    '''
    from twisted.internet import reactor
    site = server.Site(JsonService())
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except:
            pass
    reactor.listenTCP(port, channel.HTTPFactory(site))
    log.startLogging(sys.stdout)
    log.msg("LondonR Nov-09 simple JSON RPC server running on localhost:%s" % port)
    reactor.run()
