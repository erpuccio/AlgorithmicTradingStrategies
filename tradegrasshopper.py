# This program uses the 10 day rate of change(ROC) tehcnical indicator to either go
# long a market or short a market based on if the ROC is greater than 25 (Long market)
# or less than -25 (short market)

import numpy


def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
    nMarkets = CLOSE.shape[1]
    pos = numpy.zeros(nMarkets)
    for markets in range(nMarkets):
        # ROC = ((todays close - 10 days ago close) / (ten days ago close)) * 100
        settings['rateOfChange'][markets] = ((CLOSE[-1, markets] - CLOSE[-10, markets]) / 
                CLOSE[-10, markets]) * 100
        if settings['rateOfChange'][markets] > 25 and settings['relativePos'][markets] == 0 :
            settings['relativePos'][markets] = -.05
            settings['countPos'] += 1
        elif settings['rateOfChange'][markets] < -25 and settings['relativePos'][markets] == 0:
            settings['relativePos'][markets] = .05
            settings['countPos'] += 1
    for markets in range(nMarkets):
        if settings['relativePos'][markets] == -.05 and settings['rateOfChange'][markets] <= 0:
            settings['relativePos'][markets] = 0
            settings['countPos'] -= 1
        elif settings['relativePos'][markets] == .05 and settings['rateOfChange'][markets] >= 0:
            settings['relativePos'][markets] = 0
            settings['countPos'] -= 1
    # allocating positions, weigh portfolio
    independentVar = settings['countPos'] / (1 + (.05 * (settings['countPos'] - 1)))
    longShortFactor = independentVar * .05
    for markets in range(nMarkets):
        if markets == 0:
            pos[0] = independentVar
        elif settings['relativePos'][markets] == .05:
            pos[markets] = longShortFactor
        elif  settings['relativePos'][markets] == -.05:
            pos[markets] = -longShortFactor
    settings['countPos'] = 0
            
        
   
    
    return pos, settings


def mySettings():
    ''' Define your trading system settings here '''

    settings = {}
    
    settings['markets']  = ['CASH','F_AD', 'F_BO', 'F_BP', 'F_C', 'F_CC', 'F_CD',
    'F_CL', 'F_CT', 'F_DX', 'F_EC', 'F_ED', 'F_ES', 'F_FC','F_FV', 'F_GC',
    'F_HG', 'F_HO', 'F_JY', 'F_KC', 'F_LB', 'F_LC', 'F_LN', 'F_MD', 'F_MP',
    'F_NG', 'F_NQ', 'F_NR', 'F_O', 'F_OJ', 'F_PA', 'F_PL', 'F_RB', 'F_RU',
    'F_S','F_SB', 'F_SF', 'F_SI', 'F_SM', 'F_TU', 'F_TY', 'F_US','F_W', 'F_XX',
    'F_YM']
    
    
    
    settings['beginInSample'] = '20000104'
    #settings['endInSample'] = '20170710'
    settings['lookback'] = 10
    settings['budget'] = 10**6
    settings['slippage'] = 0.05
    settings['relativePos'] = numpy.zeros(45)
    settings['rateOfChange'] = numpy.zeros(45)
    settings['countPos'] = 0
   
    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)