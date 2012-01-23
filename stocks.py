"""

This script downloads the stock data for a variety of shares
from finance.yahoo.com and performs a set of calculations:

- Linear Transformation
- Beta
- Yield

As this script grows, it might become necessary to split it
into more purposeful files. For now, a single script will do.

It requires the following libraries:

- urllib (standard)
- datetime (standard)
- bivariate (my own script, included)
- matplotlib (http://www.scipy.org/PyLab)

For now, just run the script and see the output.

"""

import urllib
from datetime import date
import bivariate as bv
import matplotlib.pyplot as plt

baseline = "^GSPC"

def readSymbolList(filename):
    symbols = []
    for line in open(filename):
        line = line.strip()
        symbols.append(line)
    return symbols

def download(url, outfile):
    webFile = urllib.urlopen(url)
    localFile = open(outfile, 'w')
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()

def get1YearPriceHistory(symbol):
    today = date.today()
    url = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%02d&b=%02d&c=%04d&d=%02d&e=%02d&f=%04d&g=d&ignore=.csv" % \
           (symbol, today.month - 1, today.day, today.year - 1, today.month - 1, today.day, today.year)
    outfile = symbol + ".csv"
    download(url, outfile)

def downloadSymbols():
    symbols = readSymbolList("watchlist.txt")

    for s in symbols:
        get1YearPriceHistory(s)

def fetchAdjustedClose(symbol):
    i = 0
    closes = []
    for line in file(symbol+".csv"):
        line = line.strip()
        if i > 0:
            closes.append( float(line.split(",")[6]) )
        i += 1
    return closes[::-1]

def determineYield(closes):
    yields = []
    i = 1
    while i < len(closes):
        yields.append( (closes[i]/float(closes[i-1])) - 1.0 )
        i += 1
    return yields

def beta(symbol):
    symbolAdjustedClose = fetchAdjustedClose(symbol)
    baselineAdjustedClose = fetchAdjustedClose(baseline)

    symbolYields = determineYield(symbolAdjustedClose)
    baselineYields = determineYield(baselineAdjustedClose)

    (m, b) = bv.linreg(baselineYields, symbolYields)
    return m

def linearTransformation(closes):
    high = max(closes)
    low = min(closes)
    denominator = float(high - low)
    return [ (x - low) / denominator for x in closes ]

def plotLinearTransform(symbol):
    closes = fetchAdjustedClose(symbol)
    plt.plot(closes)
    plt.show()

def plotYieldComparison(symbol):
    symbolAdjustedClose = fetchAdjustedClose(symbol)
    baselineAdjustedClose = fetchAdjustedClose(baseline)

    symbolYields = determineYield(symbolAdjustedClose)
    baselineYields = determineYield(baselineAdjustedClose)
    plt.plot(baselineYields, symbolYields, 'g+')
    plt.show()

def mean(X):
    return sum(X) / float(len(X))

def ssd(X):
    mu = mean(X)
    return (sum([(x - mu)*(x - mu) for x in X]) / float(len(X)))**0.5

def plotSummary():
    symbols = readSymbolList('watchlist.txt')

    positiveBetas = []
    positiveLastPrice = []

    negativeBetas = []
    negativeLastPrice = []

    betas = []
    lastPrice = []

    for symbol in symbols:
        closes = fetchAdjustedClose(symbol)
        lt = linearTransformation(closes)
        betas.append( beta(symbol) )
        lastPrice.append( lt[-1] )

        if lt[-1] > lt[0]:
            positiveBetas.append( beta(symbol) )
            positiveLastPrice.append( lt[-1] )
        else:
            negativeBetas.append( beta(symbol) )
            negativeLastPrice.append( lt[-1] ) 

    (m, b) = bv.linreg(lastPrice, betas)
    fit = bv.estimatedFit(lastPrice, m, b)
    R = bv.corr(betas, fit)

    print "m  :", m
    print "b  :", b
    print "R^2:", R*R

    plt.plot(positiveLastPrice, positiveBetas, 'b+')
    plt.plot(negativeLastPrice, negativeBetas, 'r+')
    plt.xlabel("<-- 52 Week Low ... 52 Week High -->")
    plt.ylabel("Beta")

    for i in range(len(symbols)):
       plt.text(lastPrice[i], betas[i], symbols[i])

    plt.show()

def summary():

    print "Symbol", "Beta", "Linear Transformed Last Price"
    for symbol in readSymbolList('watchlist.txt'):
        closes = fetchAdjustedClose(symbol)
        lt = linearTransformation(closes)
        print symbol, beta(symbol), lt[-1]

if __name__ == '__main__':
    downloadSymbols()
    plotSummary()
