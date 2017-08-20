#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 21:58:57 2017

@author: edwardpuccio
"""

#  This program  buys the us two year treasury note during times when the misean 
#  index (Tobins Q ratio) is under 1.6 and buys the sp500 mini when
# the misean index is under .9.
#  This trade was right out of Mark Spitzengaels book "The Dao of Capital."
import numpy
import csv

def fileOpen():
    count = 0
    dtoq_Ratio_list = [0] * 109
    with open('dateVSq_ratio.csv', 'r') as file:
        read = csv.reader(file)
        for row in read:
            dtoq_Ratio_list[count] = row
            count += 1
    file.close()
    
    return dtoq_Ratio_list

def list_length(a_list):
    length = 0
    length = len(a_list)
    return length

    
    
def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
    nMarkets = CLOSE.shape[1]
    pos = numpy.zeros(nMarkets)
    
    # traverse the list if date of list equals todays date get ms index
    # if ms index is less then the special number by if it is greater then sell,
    # and buy bonds
    # most likley, dates will not match, hence if date is between these two dates then buy
    # Date and Q ratio, [0] [1] respecitvley, both strings
    # print(settings['date_Q_ratio_list'][0][0])
    # geometric mean according to https://www.advisorperspectives.com/dshort/
    # updates/2017/07/05/the-q-ratio-and-market-valuation-june-update
    # geometric average = .63
    
    a = settings['countlow']
    b = settings['counthigh']
    if b != settings['list_length']:
       if ((DATE[-1] >= int(settings['date_Q_ratio_list'][a][0]))
          and (DATE[-1] <= int(settings['date_Q_ratio_list'][b][0]))):
           if (float(settings['date_Q_ratio_list'][a][1]) / settings['geometric_average']) <= .9:
               settings['relative_pos'][1] = 1
               settings['relative_pos'][2] = 0    
           elif (float(settings['date_Q_ratio_list'][a][1]) / settings['geometric_average']) >= 1.6:
               settings['relative_pos'][1] = 0
               settings['relative_pos'][2] = 1
           settings['countlow'] += 1
           settings['counthigh'] += 1
    
    pos[1] = settings['relative_pos'][1]
    pos[2] = settings['relative_pos'][2]

    return pos, settings


def mySettings():
    settings = {}

    # S&P 100 stocks
    # settings['markets']=['CASH','AAPL','ABBV','ABT','ACN','AEP','AIG','ALL',
    # 'AMGN','AMZN','APA','APC','AXP','BA','BAC','BAX','BK','BMY','BRKB','C',
    # 'CAT','CL','CMCSA','COF','COP','COST','CSCO','CVS','CVX','DD','DIS','DOW',
    # 'DVN','EBAY','EMC','EMR','EXC','F','FB','FCX','FDX','FOXA','GD','GE',
    # 'GILD','GM','GOOGL','GS','HAL','HD','HON','HPQ','IBM','INTC','JNJ','JPM',
    # 'KO','LLY','LMT','LOW','MA','MCD','MDLZ','MDT','MET','MMM','MO','MON',
    # 'MRK','MS','MSFT','NKE','NOV','NSC','ORCL','OXY','PEP','PFE','PG','PM',
    # 'QCOM','RTN','SBUX','SLB','SO','SPG','T','TGT','TWX','TXN','UNH','UNP',
    # 'UPS','USB','UTX','V','VZ','WAG','WFC','WMT','XOM']

    # Futures Contracts

    settings['markets'] = ['CASH', 'F_ES','F_TU']
    #settings['beginInSample'] = '20060110'
    #settings['endInSample'] = '20170506'
    settings['lookback'] = 20
    settings['budget'] = 10**6
    settings['slippage'] = 0.05
    settings['date_Q_ratio_list'] = fileOpen()
    settings['countlow'] = 0
    settings['counthigh'] = 1
    settings['relative_pos'] = numpy.zeros(3)
    settings['list_length'] = list_length(settings['date_Q_ratio_list'])
    settings['geometric_average'] = .63

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)
