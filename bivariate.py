import math
import matplotlib.pyplot as plt

# Simple Linear Regression using the least squares approach.
def linreg(X, Y):
    assert len(X)==len(Y)
    n = len(X)
    EX = sum(X)
    EY = sum(Y)
    EX2 = sum([x*x for x in X])
    EXY = sum([ X[i] * Y[i] for i in range(n)])
    m = (n*EXY - EX*EY) / (n*EX2 - EX*EX)
    b = (EY - m*EX) / float(n)
    return (m, b)

def estimatedFit(X, m, b):
    return [x*m+b for x in X]

def corr(X, Y):
    mux = sum(X) / float(len(X))
    muy = sum(Y) / float(len(Y))
    SUMXX = sum([(x - mux)*(x - mux) for x in X])
    SUMYY = sum([(y - mux)*(y - mux) for y in Y])
    SUMXY = sum([(Y[i] - mux)*(X[i] - mux) for i in range(len(X))])
    return SUMXY / math.sqrt( SUMXX * SUMYY )

def studyVariables(X, Y):
    (m, b) = linreg(X, Y)
    fit = estimatedFit(X, m, b)
    Rsqrd = corr(Y, fit)**2
    print "m:", m
    print "b:", b
    print "r-squared:", Rsqrd
    print
    return (m, b)

def bivariate(X, Y):

    print

    data = zip(X, Y)
    data.sort()
    X, Y = zip(*data)

    plt.plot(X, Y, 'k+')

    print "Linear Regression."
    (m, b) = studyVariables(X, Y)

    print
    print "Inverse Regression."
    try:
        Xp = [1.0/float(x) for x in X]
        (m, b) = studyVariables(Xp, Y)
        fit = [m/float(x) + b for x in X]
        plt.plot(X, fit, 'm-')
    except OverflowError:
        print "We're sorry. Overflow error. Numbers are either too large or too small."
        print

    print "Square Root Regression."
    try:
        Xp = [math.sqrt(x) for x in X]
        (m, b) = studyVariables(Xp, Y)
        fit = [m*math.sqrt(x) + b for x in X]
        plt.plot(X, fit, 'b-')
    except OverflowError:
        print "We're sorry. Overflow error. Numbers are either too large or too small."
        print

    print "Logrithmic Regression."
    try:
        Xp = [math.log(x) for x in X]
        (m, b) = studyVariables(Xp, Y)
        fit = [m*math.log(x) + b for x in X]
        plt.plot(X, fit, 'c-')
    except OverflowError:
        print "We're sorry. Overflow error. Numbers are either too large or too small."
        print

    print "Power law."
    try:
        Xp = [math.log(x) for x in X]
        Yp = [math.log(y) for y in Y]
        (m, b) = studyVariables(Xp, Yp)
        fit = [math.exp(m*math.log(x) + b) for x in X]
        plt.plot(X, fit, 'r-')
    except OverflowError:
        print "We're sorry. Overflow error. Numbers are either too large or too small."

    plt.show()
