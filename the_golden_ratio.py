# This program buys the sp500 mini when the gold/silver ratio is greater than 
# or equal to 1.5
# This program buys the ten year treasury note when the gold/silver ratio is less
# than or equal to 1.0
# Hence at no time can you ever be long the us ten year and the sp500 mini at
# the same time.
# More weight is given to us ten yera becuase of its lower volaitlity.
# The gold to silver ratio is recalculated every 21 days or around every month
# in trading terms.
import numpy
import matplotlib.pyplot as plt


def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
    ''' This system uses trend following techniques to allocate capital into the desired equities'''

    
    nMarkets = CLOSE.shape[1]
    pos = numpy.zeros(nMarkets)
    settings['relativePos'][0] = 10
    settings['countDays'] += 1
    
    if settings['countDays'] % 21 == 0:
        settings['gldtoslv'] = (CLOSE[-1, 2] / CLOSE[-1, 3])
        settings['gldslvarray'][settings['count']] = settings['gldtoslv']
        settings['count'] += 1
    
    
    if settings['gldtoslv'] >= 1.55 and settings['countDays'] % 20 == 0 :
        settings['relativePos'][1] = 10
        settings['relativePos'][4] = 0
    elif settings['gldtoslv']<= 1.0 and settings['countDays'] % 20 == 0:
        settings['relativePos'][1] = 0
        settings['relativePos'][4] = 90

        
    
    pos[0] = settings['relativePos'][0]
    pos[1] = settings['relativePos'][1]
    pos[4] = settings['relativePos'][4]
    
    # initally plotted gold vs silver ratio to get an approximate idea
    """
    if (settings['count'] == 327):
        for i in range(settings['array'].shape[0]):
            settings['array'][i] = i
        print(settings['gldslvarray'])
        plt.plot(settings['array'],settings['gldslvarray'])
        plt.show()
    """
    return pos, settings


def mySettings():
    ''' Define your trading system settings here '''

    settings = {}
    
    # Futures Contracts
    settings['markets'] = ['CASH', 'F_ES', 'F_GC', 'F_SI', 'F_TY']
    #`19900104 - 20170710
    
    settings['beginInSample'] = '20000104'
    #settings['endInSample'] = '20170710'
    settings['lookback'] = 21
    settings['budget'] = 10**6
    settings['slippage'] = 0.05
    settings['countDays'] = 0
    settings['gldtoslv']= 0.0
    settings['relativePos'] = numpy.zeros(5)
    settings['gldslvarray'] = numpy.zeros(328)
    settings['array'] = numpy.zeros(328)
    settings['count'] = 0
    settings['entrance'] = 0

    
   
    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)
