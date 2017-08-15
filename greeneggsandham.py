#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 12:40:37 2017

@author: edwardpuccio
"""


# This algo checks if the TED spread is above a certain value and if it is, 
# it buys the sp500. If it is less than a certain value it buys the ten year
# tbill. 

import numpy
import csv

# Read in TED spread from csv
def fileOpen():
    TED_array = numpy.zeros(400)
    count_months = 1
    index = 0
    
    with open('ted_spread.csv', 'r') as file:
        read = csv.reader(file)
        for row in read:
           date_split = row[0].split('/')
           month = int(date_split[0])
           TED = row[1]
           # If month chanegs get first TED spread and use a default TED spread
           if month == count_months:
               if TED != '.':
                   TED_array[index]= float(TED)
                   index += 1
                   count_months += 1
                   if count_months == 13:
                       count_months = 1
    file.close()
    return TED_array
   
def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
    
    nMarkets = CLOSE.shape[1]
    pos = numpy.zeros(nMarkets)
    
    # Check if the month has passed and if does get new TED spread
    date = str(DATE[-1])
    month = date[4] + date[5]
    month = int(month)
    settings['previousMonth'] =  settings['currentMonth']
    settings['currentMonth'] = month
    
    # if month changes then change TED
    if settings['previousMonth'] != settings['currentMonth']:
        settings['index'] += 1 
    currentTED = settings['TED_spread'][settings['index']]
    #
    FIVEHUNDRED = 500
    movingaverage = numpy.sum(CLOSE[-FIVEHUNDRED: , 1]) / FIVEHUNDRED
    # if the monthly ted spread is grater than 1.3 buy 10 year bond
    if  currentTED >= 1.3:
        settings['relativePos'][1] = 0
        settings['relativePos'][2] = 9
    # if monthly ted spread is less than or equal to .3 and 500 day moving 
    # average  is less than close, buy sp500
    elif currentTED <= .3 and CLOSE[-1,1] > movingaverage:
        settings['relativePos'][1] = 2
        settings['relativePos'][2] = 0
    
        
    
    pos[0] = 1
    pos[1] = settings['relativePos'][1]
    pos[2] = settings['relativePos'][2]


    return pos, settings


def mySettings():
    settings = {}
    settings['markets']  = ['CASH','F_ES', 'F_TY']
    #19911219 when it starts
    #settings['beginInSample'] = '20060110'
    #settings['endInSample'] = '20170506'
    settings['lookback'] = 500
    settings['budget'] = 10**6
    settings['slippage'] = 0.05
    settings['TED_spread'] = fileOpen()
    settings['currentMonth'] = 0
    settings['previousMonth'] = 0
    settings['relativePos'] = numpy.zeros(3)
    settings['index'] = 0
    settings['indciator'] = 0
   

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)