#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 17:36:04 2017

@author: edwardpuccio
"""

#This algo buys a stock everytime it goes down 10 days in a row or more. However, 
#if the stock goes past 10 days, 
#the algo increases its exposure to the specific stock until the stock finishes 
# at a greater price then the previous day
import numpy

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):

    nMarkets=CLOSE.shape[1]
    pos=numpy.zeros(nMarkets)    
    
    
    for i in range(nMarkets - 1):
        if settings['marketType'][i] == 1:
            if CLOSE[-2,i] > CLOSE[-1,i]:
                settings['increase_pos'][i] += 1
                pos[i] = (numpy.power(2,settings['increase_pos'][i]))/ 100 #increase exposure by 1 + (.02)^n; n > 0
            elif CLOSE[-1,i] > CLOSE[-2,i]:
                settings['increase_pos'][i] = 0
                pos[i] = 0.0
                settings['marketType'][i] = 0  
        elif (CLOSE[-10,i] > CLOSE[-9,i] > CLOSE[-8,i] > CLOSE[-7,i] > CLOSE[-6,i] > CLOSE[-5,i] > \
                CLOSE[-4,i] > CLOSE[-3,i] > CLOSE[-2,i] > CLOSE[-1,i]) and settings['marketType'][i] == 0:
                    if  settings['count'][i] == 0 :
                       settings['count'][i] += 6
                       pos[i] = .01
                       settings['marketType'][i] = 1
        if settings['count'][i] > 0:
            settings['count'][i] -= 1
 
    return pos, settings


def mySettings():

    settings= {}

    # S&P 100 stocks 
    settings['markets']= ['CASH','PEP',
    'AMGN','AMZN','APA','APC','AXP','BA','BAC','BAX','BK','BMY','BRKB','C',
    'CAT','CL','CMCSA','COF','COP','COST','CSCO','CVS','CVX','DD','DIS','DOW',
    'DVN','EBAY','EMC','EMR','EXC','F','FB','FCX','FDX','FOXA','GD','GE',
    'GILD','GM','GOOGL','GS','HAL','HD','HON','HPQ','IBM','INTC','JNJ','JPM',
    'KO','LLY','LMT','LOW','MA','MCD','MDLZ','MDT','MET','MMM','MO','MON',
    'MRK','MS','MSFT','NKE','NOV','NSC','ORCL','OXY','PEP','PFE','PG','PM',
    'QCOM','RTN','SBUX','SLB','SO','SPG','T','TGT','TWX','TXN','UNH','UNP',
    'UPS','USB','UTX','V','VZ','WAG','WFC','WMT','XOM']
    


    #settings['markets']  = ['CASH', 'F_FC']
    #settings['beginInSample'] = '20060506'
    #settings['endInSample'] = '20170506'
    settings['lookback']= 504
    settings['budget']= 10**6
    settings['slippage']= 0.05
    settings['marketType'] = numpy.zeros(101)
    settings['count10DaysDown'] = 0
    settings['count11DaysDown'] = 0
    settings['count12DaysDown'] = 0
    settings['count13DaysDown'] = 0
    settings['count14DaysDown'] = 0
    settings['PnL10'] = 0
    settings['PnL11'] = 0
    settings['PnL12'] = 0
    settings['PnL13'] = 0                  
    settings['PnL14'] = 0
    settings['count10'] = 0
    settings['count11'] = 0  
    settings['count12'] = 0
    settings['count13'] = 0
    settings['count14'] = 0
    settings['relative_pos'] =numpy.zeros(101)
    settings['count'] = numpy.zeros(101)
    settings['increase_pos'] = numpy.zeros(101)
    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)
