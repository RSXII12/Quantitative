import numpy as np
import scipy as scy

def simulateStockMC(initialValue, strikePrice, sigma, T, riskFreeInterest, N):

    Z = np.random.normal(0,1,N)
    
    finalValue = initialValue * np.exp(
        (riskFreeInterest - 0.5 * sigma ** 2) * T
        + sigma * Z * np.sqrt(T)
        )
    
    # Numpy applies this element-wise instead of using a for loop, more computationally efficient
    
    payoff = finalValue - strikePrice

    payoff[payoff < 0] = 0

    #payoff<0 is a boolean mask which creates an array which is fine here but in practice numpy has an element-wise
    #operation function

    optionPrice = np.exp(-riskFreeInterest*T) * np.mean(payoff)

    #Monte-Carlo option price
    
    standardError = np.std(payoff)/np.sqrt(N)
    
    return optionPrice,standardError


def simulateStockMCAntithetic(initialValue, strikePrice, sigma, T, riskFreeInterest, N):

    Z = np.random.normal(0,1,N)

    finalValue = initialValue * np.exp(
        (riskFreeInterest - 0.5 * sigma ** 2) * T
        + sigma * Z * np.sqrt(T)
        )

    finalValuePair = initialValue * np.exp(
        (riskFreeInterest - 0.5 * sigma ** 2) * T
        + sigma * -Z * np.sqrt(T)
        )
    # Numpy applies this element-wise instead of using a for loop, more computationally efficient

    finalValue = finalValue - strikePrice
    finalValuePair = finalValuePair - strikePrice
    
    finalValue[finalValue <= 0] = 0
    finalValuePair[finalValuePair <= 0] = 0
    
    payoff = (finalValue + finalValuePair) /2.0

    optionPrice = np.exp(-riskFreeInterest*T) * np.mean(payoff)

    #Monte-Carlo option price

    standardError = np.std(payoff)/np.sqrt(N)

    return optionPrice,standardError


def blackScholesCall(initialValue, strikePrice, sigma, T, riskFreeInterest):


    d1 = (np.log(initialValue / strikePrice) + (riskFreeInterest + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    callValue = initialValue * scy.stats.norm.cdf(d1) - strikePrice * np.exp(-riskFreeInterest * T) * scy.stats.norm.cdf(d2)

    return callValue
    
