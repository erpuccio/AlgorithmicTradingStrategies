"""
Created on Fri Aug  4 12:28:41 2017

@author: edwardpuccio
"""
# If the price of a security is greater than the 500 day moving average and makes
# a fifty two week high, the program enters a logn positon in the security/market
# If if the security meets the previous criteria, but suffers a 15% peak to trough
# loss I sell the security.
# The two secruities/markets I use here are the sp500 mini and the 10 year treasury note

import numpy


def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):

    nMarkets = CLOSE.shape[1]
    pos = numpy.zeros(nMarkets)

    periodLonger = 500
    periodShorter = 252
    TWO_MONTHS = 42
    

    for markets in range(nMarkets):
        fiftytwoweek = CLOSE[-periodShorter, markets]
        movingaverage = numpy.sum(CLOSE[-periodLonger: , markets]) / periodLonger
        # If markets are  not in bear market
        if settings['periodOfDecline'][markets] != 1:                       
           if CLOSE[-1, markets] > movingaverage:
               if CLOSE[-1, markets] > fiftytwoweek:
                   settings['relativePos'][markets] = 1
                   if CLOSE[-1, markets] > settings['high'][markets]:
                      settings['high'][markets] = CLOSE[-1, markets]
           if settings['high'][markets] > 0:
               # If market is off the high off its high by 15% exit position
               if (((CLOSE[-1,markets] - settings['high'][markets]) / settings['high'][markets]) 
               <= - .15):
                   settings['relativePos'][markets] = 0
                   settings['high'][markets] = 0
                   settings['periodOfDecline'][markets] = 1
        elif (CLOSE[-1, markets] > CLOSE[-TWO_MONTHS, markets]) and CLOSE[-1, markets] > settings['high'][markets] :
             settings['periodOfDecline'][markets] = 0
             settings['high'][markets] = 0
        elif CLOSE[-1, markets] < movingaverage:
             settings['periodOfDecline'][markets] = 0
             settings['high'][markets] = 0
                     
    # Give less weight to more volatile asset(Ten year note)
    for markets in range(nMarkets):
        if markets == 0:
            pos[0] = 1
        elif markets != 2 and  settings['relativePos'][markets] > 0:
            pos[markets] = .3
        elif markets == 2 and settings['relativePos'][markets] > 0:
            pos[markets] = .9
            
      
    return pos, settings


def mySettings():
    settings = {}
    settings['markets']  = ['CASH','F_ES','F_TY']
    settings['beginInSample'] = '20000110'
    #settings['endInSample'] = '20000506'
    settings['lookback'] = 500
    settings['budget'] = 10**6
    settings['slippage'] = 0.05
    settings['relativePos'] = numpy.zeros(3)
    settings['high'] = numpy.zeros(3)
    settings['low'] = numpy.zeros(3)
    settings['periodOfDecline'] = numpy.zeros(3)
    settings['periodOfIncrease'] = numpy.zeros(3)

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)
