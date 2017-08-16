#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:15:48 2017

@author: edwardpuccio
"""
# This algo buys and sell gold and the sp500 during price moves in the 
# sp500 greater tham 2 standard devaitions, 3 standard deviations and 4
# standard deviations

import numpy

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):

    nMarkets = CLOSE.shape[1]
    pos=numpy.zeros(nMarkets)
    count1STD = 0
    count2STD = 0
    count3STD = 0
    count4STD = 0
    sp500Std = 0.01562 
    
    """
    if CLOSE[(-1,1)] >=  ((sp500Std) + 1.0) * (CLOSE[(-2,1)]):
        settings['count1STD'] += 1
        if CLOSE[(-1,1)] >= (((sp500Std * 2) + 1.0)) * (CLOSE[(-2,1)]):
            settings['count2STD'] += 1
            if CLOSE[(-1,1)] >= (((sp500Std * 3) + 1.0)) * (CLOSE[(-2,1)]):
                settings['count3STD'] += 1
                if CLOSE[(-1,1)] >= (((sp500Std * 4) + 1.0)) * (CLOSE[(-2,1)]):
                    settings['count4STD'] += 1
    
               
    print ("Count", settings['count1STD'])
    print ("Count", settings['count2STD'])
    print ("Count", settings['count3STD'])
    print ("Count", settings['count4STD'])
    """
    
    #If price is greater the yesterday close
    if CLOSE[(-1,1)] >= (((sp500Std) * 4) + 1.0) * (CLOSE[(-2,1)]):
        pos [0] = 4
        pos [1] = .2
        pos [2] = -.4
    
    elif CLOSE[(-1,1)] >= (((sp500Std) * 3) + 1.0) * (CLOSE[(-2,1)]) and CLOSE[(-1,1)] < (((sp500Std) * 4) + 1.0) * (CLOSE[(-2,1)]):
        pos [0] = 4
        pos [1] = .2
        pos [2] = -.4
    
    if CLOSE[(-1,1)] >= (((sp500Std) * 2) + 1.0) * (CLOSE[(-2,1)]) and CLOSE[(-1,1)] < (((sp500Std) * 3) + 1.0) * (CLOSE[(-2,1)]):
        pos [0] = 4
        pos [1] = .2
        pos [2] = -.4
    #If price is less then yesterday close
    elif CLOSE[(-1,1)] <= ((CLOSE[(-2,1)]) / ((sp500Std) * 2) + 1.0) and CLOSE[(-1,1)] > (CLOSE[(-2,1)]) / (((sp500Std) * 3) + 1.0):
        pos [0] = 4
        pos [1] = -.2
        pos [2] = .4
    
    elif CLOSE[(-1,1)] <= ((CLOSE[(-2,1)]) / ((sp500Std) * 3) + 1.0)  and CLOSE[(-1,1)] > ((CLOSE[(-2,1)]) / ((sp500Std) * 4) + 1.0):  
        pos [0] = 4
        pos [1] = -.2
        pos [2] = .4
    
    elif CLOSE[(-1,1)] <= ((CLOSE[(-2,1)]) / ((sp500Std) * 4) + 1.0):
        pos [0] = 4
        pos [1] = -.2
        pos [2] = .4
    else:
        pos [0] = 1
        pos [1] = 0
        pos [2] = 0
           
    return pos, settings
    

def mySettings():


    settings= {}
    settings['markets']  = ['CASH','F_ES', 'F_GC']
    #settings['beginInSample'] = '20060506'
    #settings['endInSample'] = '20170522'
    settings['lookback']= 2520
    settings['budget']= 1000000
    settings['slippage']= 0.05
    settings['count1STD'] = 0
    settings['count2STD'] = 0
    settings['count3STD'] = 0
    settings['count4STD'] = 0


    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)