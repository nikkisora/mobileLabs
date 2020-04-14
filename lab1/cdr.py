import csv
import time
from parse import calcBilling

def printLog(log, totalCOut, totalCIn, totalS):
    print('\n')
    for line in log:
        if line[1] == 'in':
            print('incoming call at', line[0], ', charge call:', line[2])
        else:
            print('outgoing call at', line[0], ', charge call:', line[2], ', charge sms: ', line[3])
    print('total calls cost: ', totalCOut+totalCIn, '\ntotal sms cost: ', totalS, '\ntotal biling: ', totalS+totalCOut+totalCIn)

if __name__ == "__main__":
    number = '968247916'
    SMSRate = 1
    firstFree = [0, 5, 5]
    timeRate = [[[0000,2360], [4,1]]]

    log, totalCOut, totalCIn, totalS, outDur, inDur, smsN = calcBilling('data.csv', number, SMSRate, firstFree, timeRate)

    printLog(log, totalCOut, totalCIn, totalS)