#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 16:25:47 2017

@author: edwardpuccio
"""

# This program does pair trades. It makes a ratio from two securities and
# goes short the overvalued security and goes long the undervalued security;
# in essence, hoping to profit from converging securities. 

import numpy
import matplotlib.pyplot as plt

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
    
    #Used for counting data points
    #settings['cout'] += 1
    
    nMarkets = CLOSE.shape[1]
    pos = numpy.zeros(nMarkets)
    
    # Ratios
    eurotodollar = CLOSE[-1,1] / CLOSE[-1,2]
    mealtoSoybeans = CLOSE[-1,4] / CLOSE[-1,3]
    heatingtoCrude = CLOSE[-1,5] / CLOSE[-1,6]
    goldtosilver = CLOSE[-1,7] / CLOSE[-1,8]
    corntowheat = CLOSE[-1,9] / CLOSE[-1, 10] 
    
    # Used for getting Data
    """
    settings['ratios'][settings['index']][0] = CLOSE[-1, 1] / CLOSE[-1, 2] 
    settings['ratios'][settings['index']][1] = CLOSE[-1,3] / CLOSE[-1,2]
    settings['index'] += 1
          
    #6393
    if (settings['index'] == 6406):
       
        for i in range(settings['ratios'].shape[0]):
            settings['days'][i] = i
        # get in terms of percentage so we know stds of all assets and so
        # we can adjust portfolio correctly
        print(numpy.std((CLOSE[-499: ,1] - CLOSE[-500:-1 ,1]) /
                        CLOSE[-500:-1 ,1]))
        print(numpy.std((CLOSE[-499: ,2] - CLOSE[-500:-1 ,2]) /
                        CLOSE[-500:-1 ,2]))
        print(numpy.std((CLOSE[-499: ,3] - CLOSE[-500:-1 ,3]) /
                        CLOSE[-500:-1 ,3]))
        meanRatio0 = numpy.mean(settings['ratios'][:, 0])
        meanRatio1 = numpy.mean(settings['ratios'][:, 1])
        stdRatio0 = numpy.std(settings['ratios'][:, 0])
        stdRatio1 = numpy.std(settings['ratios'][:, 1])
        print( meanRatio0)
        print( meanRatio1)
        print( stdRatio0 )
        print( stdRatio1)
        
        plt.plot(settings['days'],settings['ratios'][:,0])
        plt.show()
        plt.plot(settings['days'],settings['ratios'][:,1])
        plt.show()
        
    oiltoSoybeans = CLOSE[-1, 1] / CLOSE[-1, 2] 
    mealtoSoybeans = CLOSE[-1,3] / CLOSE[-1,2]
    
    print(settings['cout'])
    """
    
    #F_C vs F_W
    if  corntowheat  >= .95:
        settings['relativePos'][9] = -5
        settings['relativePos'][10] = 5
    elif  corntowheat  < .8 and   corntowheat  > .7:
        settings['relativePos'][9] = 0
        settings['relativePos'][10] = 0
    elif  corntowheat  <= .55:
        settings['relativePos'][9] = 5
        settings['relativePos'][10] = -5
    
    # euro to dollar
    if eurotodollar  >= 2.5:
       settings['relativePos'][1] = -5
       settings['relativePos'][2] = 5
    elif eurotodollar  < 1.9 and eurotodollar  > 1.4:
        settings['relativePos'][1] = 0
        settings['relativePos'][2] = 0
    elif eurotodollar  <= .9:
        settings['relativePos'][1] = 5
        settings['relativePos'][2] = -5
    
    #gold to silver
    if goldtosilver >= 1.6:
       settings['relativePos'][7] = -5
       settings['relativePos'][8] = 3
    elif goldtosilver < 1.25 and goldtosilver > 1.15:
        settings['relativePos'][7] = 0
        settings['relativePos'][8] = 0
    elif goldtosilver <= .8:
        settings['relativePos'][7] = 5
        settings['relativePos'][8] = -3
    
    # meal to soybeans
    if mealtoSoybeans >= .75:
        settings['relativePos'][4] = -5
        settings['relativePos'][3] = 5
    elif mealtoSoybeans < .62 and  mealtoSoybeans > .6:
        settings['relativePos'][4] = 0
        settings['relativePos'][3] = 0
    elif mealtoSoybeans <= .51:
        settings['relativePos'][4] = 5
        settings['relativePos'][3] = -5
    
    #heating oil to crudeOil
    if heatingtoCrude >= 1.4:
       settings['relativePos'][5] = -5
    elif heatingtoCrude < 1.25 and heatingtoCrude > 1.15:
        settings['relativePos'][5] = 0
    elif heatingtoCrude <= 1.0:
        settings['relativePos'][5] = 5
                
    for i in range(nMarkets):
        pos[i] = settings['relativePos'][i]
    pos[0] = 1
       
    return pos, settings


def mySettings():

    settings = {}    
    settings['markets'] = ['CASH','F_EC','F_DX', 'F_S', 'F_SM', 'F_HO', 'F_CL',
    'F_GC', 'F_SI' , 'F_C' , 'F_W'] 
    #settings['beginInSample'] = '19920110'
    #settings['endInSample'] = '20140506'
    settings['lookback'] = 500
    settings['budget'] = 10**6
    settings['slippage'] = 0.05
    settings['index'] = 0
    settings['relativePos'] = numpy.zeros(11)
    """
    settings['ratios'] = numpy.zeros((6406, 10))
    settings['days'] = numpy.zeros(6406)
    settings['mean'] = numpy.zeros(6406)
    settings['cout'] = 0
    """
    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)
