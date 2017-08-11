# This algo enters into a long postion in a  specific market if the 30 day moving average
# was greater
# than the 30 to 60 day moving average which was greater than
# the 60 to 90 day moving average. This algo enters into a short position into
# a specific market if the 90 day to 60 day moving average 
# was greater than the 60 to 30 day moving average which was greater then the 30 day moving
# average

import numpy

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
  
    
    nMarkets=CLOSE.shape[1]
    pos=numpy.zeros(nMarkets) 
    THIRTY_DAYS = 30
    average_0to30_days = numpy.sum(CLOSE[-30: , 4]) / THIRTY_DAYS 
    average_30to60_days = numpy.sum(CLOSE[-60: -29, 4]) / THIRTY_DAYS
    average_60to90_days = numpy.sum(CLOSE[-90: -59, 4]) /THIRTY_DAYS
    
    if (settings['count_days'] % 30 == 0):
        #uptrend
        if (average_0to30_days > average_30to60_days > average_60to90_days):
            for i in range(nMarkets - 1):
                if (settings['relative_pos'][i] != 4 or settings['relative_pos'][i] != 6 or
                      settings['relative_pos'][i] != 11 or settings['relative_pos'][i] != 15):
                    settings['relative_pos'][i] = .0416
                elif settings['relative_pos'][i] == 4 or settings['relative_pos'][i] == 11:
                    settings['relative_pos'][i] = .25
        #downtrend
        elif (average_0to30_days < average_30to60_days < average_60to90_days): 
            for i in range(nMarkets - 1):
                if (settings['relative_pos'][i] != 4 or settings['relative_pos'][i] != 6 or
                      settings['relative_pos'][i] != 11 or settings['relative_pos'][i] != 15):
                    settings['relative_pos'][i] = -.0275
                elif settings['relative_pos'][i] == 4 or settings['relative_pos'][i] == 11:
                    settings['relative_pos'][i] = -.165
                else:
                    settings['relative_pos'][i] = .165
    #set relative_pos equal to pos
    for i in range(nMarkets - 1): 
        pos[i] = settings['relative_pos'][i]
                    
    
    return pos, settings


def mySettings():
    settings= {}

    settings['markets']  = ['CASH','F_C', 'F_CL', 'F_CT', 'F_ES', 'F_FC', 'F_GC', 'F_HG','F_LB',
            'F_LC', 'F_NG', 'F_NQ', 'F_PA', 'F_PL', 'F_S', 'F_SI', 'F_W']
    # settings['beginInSample'] = '20120506'
    # settings['endInSample'] = '20150506'
    settings['lookback']= 90
    settings['budget']= 10**6
    settings['slippage']= 0.05
    settings['marketType'] = 0
    settings['countDays'] = 0
    settings['relative_pos'] = numpy.zeros(17)
    settings['count_days'] = 0

    

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)
