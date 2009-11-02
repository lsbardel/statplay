'''
Plotting client for server1
Usage:
    python plot.py <SYMBOL>
'''
import sys
import datetime

from pylab import figure, show
from matplotlib.dates import MONDAY, SATURDAY
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter

# every monday
mondays   = WeekdayLocator(MONDAY)

# every 3rd month
months    = MonthLocator(range(1,13), bymonthday=1, interval=3)
monthsFmt = DateFormatter("%b '%y")

d1970 = datetime.date(1970,1,1)

def r2ordinal(dt):
    '''
    convert Julian Date to python datetime.date
    '''
    dt  = d1970 + datetime.timedelta(days = int(dt))
    return dt.toordinal()

def plot(data):
    dates = []
    values = []
    for d in data:
        dt = r2ordinal(d[0])
        dates.append(dt)
        values.append(d[1])

    fig = figure()
    ax = fig.add_subplot(111)
    ax.plot_date(dates, values, '-')
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
    ax.xaxis.set_minor_locator(mondays)
    ax.autoscale_view()
    ax.grid(True)
    fig.autofmt_xdate()
    show()
    

if __name__ == '__main__':
    from jsonrpc import ServiceProxy
    s = ServiceProxy('http://localhost:8080/')
    N = len(sys.argv)
    window = 20
    if N > 1:
        symbol = str(sys.argv[1]).upper()
        if N > 2:
            window = int(sys.argv[2])
    else:
        symbol = 'GOOG'
    r = s.mean(symbol, window = window)
    plot(r)
