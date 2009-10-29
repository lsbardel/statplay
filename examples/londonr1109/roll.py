
import numpy as ny
import rpy2.rinterface as ri
from rpy2.robjects import r
#ri.initr()

_rlibs = ['PerformanceAnalytics',
          'quantmod']

# Loads the R libraries
for lib in _rlibs:
    r('library(%s)' % lib)
    
    
class RollBase(object):
    rApplyFunc = r['rollapply']
    rfunc = None
    
    def get(self, ticker, window = 20, align = 'right'):
        res = self.data(ticker, window, align)
        return self.tojson(res)
        
    def getSymbols(self, ticker):
        return r('getSymbols("%s")' % ticker)
    
    def data(self, ticker, window, align):
        gs = self.getSymbols(ticker)
        data = r("Cl(%s['2008::'])" % ticker)
        res = self.rApplyFunc(data,window,self.rfunc,align = align)
        return res

    def tojson(self, res):
        dates  = r['index'](res)
        values = r['coredata'](res)
        jts = []
        for k,v in zip(dates,values):
            jts.append((k,v))
        return jts
            
class RollMean(RollBase):
    rfunc = r['mean']

mean = RollMean()


