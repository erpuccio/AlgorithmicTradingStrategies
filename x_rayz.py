# This program imports the federal reserve economic data consumer price index
# values from 1990 and uses those values to get the real values or infaltion adjusted
# values of the sepcific commodities/markets. 
# Then when a commdoity hits a specific low infaltion based price, the algo
# enters into a long psoiton and exits when the commodity/market hits a relativley 
# high price.
import numpy
import csv

#elemnt zero is the oldest elment, in this case, inflation from 2/1/1990
def cpi_array():
    cpi_array = numpy.zeros((328))
    count = 0
    with open("CPI_Spyder.csv", 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            cpi = float(row[1])
            cpi_array[count] = cpi
            count += 1 
    csvfile.close()
    return cpi_array

#market dicitonary [buy price, sell price, current pos, iniital entry pos, fall by price, add to pos price
#if it falls by 'fall by price', # of times added to the pos]
def market_dictionary():
    market_dictionary = {}
    market_dictionary[0] = [10000.0,12500.0,0,.5,.08,.1, 0]
    market_dictionary[1] = [8000.0,12000.0,0,.5,.12,.1, 0]
    market_dictionary[2] = [20000.0,25000.0,0,.5,.1,.1, 0]
    market_dictionary[3] = [15000.0,20000.0,0,.5,.06,.1, 0]
    market_dictionary[4] = [26000.0,36000.0,0,.5,.07,.1, 0]
    market_dictionary[5] = [25000.0,30000.0,0,.5,.08,.1, 0]
    market_dictionary[6] = [20000.0,21000.0,0,.5,.05,.1, 0]
    market_dictionary[7] = [14000.0,17000.0,0,.5,.07,.1, 0]
    market_dictionary[8] = [15000.0,20000.0,0,.5,.07,.1, 0]
    market_dictionary[9] = [5000.0,6000.0,0,.5,.1,.1, 0]
    market_dictionary[10] = [13000.0,19500.0,0,.5,.075,.1, 0]
    
    return market_dictionary



def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
    ''' This system uses trend following techniques to allocate capital into the desired equities'''

    #initalzie the basics
    nMarkets = CLOSE.shape[1]
    pos = numpy.zeros(nMarkets)
    i = 0
    settings['countDays'] += 1
            
    #setting the cpi multiplyer to get compare prices reltivlely
    settings['CPI_muliplyer'] = (settings['BASE_CPI'] /  settings['cpi_array'][ settings['count']])
    # constantly get a new cpi every month by adding to count       
    if settings['countDays'] % 21 == 0:
        settings['count'] += 1
    #entering the pos
    for i in range(nMarkets - 1):
        if (CLOSE[-1, i] * settings['CPI_muliplyer']) <= settings['market_dictionary'][i][0]:
            settings['market_dictionary'][i][2] = settings['market_dictionary'][i][3]
    # pyramding to a falling posiiton - stage 1
        if (CLOSE[-1,i] * settings['CPI_muliplyer']) <= (settings['market_dictionary'][i][0] / 
             (1+(settings['market_dictionary'][i][4] * 5)) and settings['market_dictionary'][i][6] == 4):
            settings['market_dictionary'][i][6] += 1
            settings['market_dictionary'][i][3] += settings['market_dictionary'][i][5]
        elif (CLOSE[-1,i] * settings['CPI_muliplyer']) <= (settings['market_dictionary'][i][0] / 
             (1+(settings['market_dictionary'][i][4] * 4)) and settings['market_dictionary'][i][6] == 3):
            settings['market_dictionary'][i][6] += 1
            settings['market_dictionary'][i][3] += settings['market_dictionary'][i][5]
        elif (CLOSE[-1,i] * settings['CPI_muliplyer']) <= (settings['market_dictionary'][i][0] / 
             (1+(settings['market_dictionary'][i][4] * 3)) and settings['market_dictionary'][i][6] == 2):
            settings['market_dictionary'][i][6] += 1
            settings['market_dictionary'][i][3] += settings['market_dictionary'][i][5]
        elif (CLOSE[-1,i] * settings['CPI_muliplyer']) <= (settings['market_dictionary'][i][0] / 
             (1+(settings['market_dictionary'][i][5] * 2)) and settings['market_dictionary'][i][6] == 1):
            settings['market_dictionary'][i][6] += 1
            settings['market_dictionary'][i][3] += settings['market_dictionary'][i][5]
        elif (CLOSE[-1,i] * settings['CPI_muliplyer']) <= (settings['market_dictionary'][i][0] / (1+settings['market_dictionary'][i][4])
        and settings['market_dictionary'][i][6] == 0):
            settings['market_dictionary'][i][6] += 1
            settings['market_dictionary'][i][3] += settings['market_dictionary'][i][5] 
        
    #closing the position 
        if (CLOSE[-1, i] * settings['CPI_muliplyer']) >= settings['market_dictionary'][i][1]:
            settings['market_dictionary'][i][2] = 0
            settings['market_dictionary'][i][6] = 0
    #set posistion to be returned equal to market dictionary value 2
    for i in range(nMarkets - 1):
        pos[i] = settings['market_dictionary'][i][2] 
    pos[11] = 11
    return pos, settings


def mySettings():
    ''' Define your trading system settings here '''

    settings = {}
    
    # Futures Contracts
    settings['markets'] = ['F_C', 'F_CC', 'F_CL', 'F_CT', 'F_FC','F_KC',
            'F_LC', 'F_LN', 'F_NG', 'F_O', 'F_PA', 'CASH']
    #`19900104 - 20170710
    settings['beginInSample'] = '19900104'
    #settings['endInSample'] = '20170710'
    settings['lookback'] = 21
    settings['budget'] = 10**6
    settings['slippage'] = 0.05
    settings['countDays'] = 0
    settings['count'] = 0
    settings['cpi_array'] = cpi_array()
    settings['market_dictionary'] = market_dictionary()
    settings['BASE_CPI'] = settings['cpi_array'][0]
    settings['CPI_muliplyer'] = 0
   
    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)