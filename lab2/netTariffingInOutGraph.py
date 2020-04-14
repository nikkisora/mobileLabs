import csv
import datetime
import math
import matplotlib
import matplotlib.pyplot as plt
import collections

def tarrifNet(size, rate):
    totalCost = 0
    actRate = rate[1]
    repeat = rate[3]
    size = max(0, size/rate[2]-rate[4])

    while size-rate[0]>0 and repeat!=0:
        totalCost+=rate[0]*actRate
        actRate+=rate[1]
        size-=rate[0]
        repeat -= 1

    totalCost+=size*actRate
    return round(totalCost, 2)

def tarrifParse(dataFP, targetIp, ratePerSize):
    totalData = 0
    plotXYin = {}
    plotXYout = {}

    with open(dataFP) as csv_f:
        data = csv.DictReader(csv_f)
        for row in data:
            srcIP = row['Src IP Addr']
            dstIP = row['Dst IP Addr']
            if targetIp in srcIP or targetIp in dstIP:
                sizeByte = math.ceil(float(row['In Byte']))
                firstSeen = matplotlib.dates.date2num(datetime.datetime.strptime(row['Date first seen'], '%Y-%m-%d %H:%M:%S'))
                totalData+=sizeByte
                if targetIp in srcIP:
                    if firstSeen in plotXYout:
                        plotXYout[firstSeen] += sizeByte/ratePerSize[2]
                    else:
                        plotXYout[firstSeen] = sizeByte/ratePerSize[2]
                if targetIp in dstIP:
                    if firstSeen in plotXYin:
                        plotXYin[firstSeen] += sizeByte/ratePerSize[2]
                    else:
                        plotXYin[firstSeen] = sizeByte/ratePerSize[2]
    return round(totalData/ratePerSize[2], 2), tarrifNet(totalData, ratePerSize), plotXYin, plotXYout


if __name__ == "__main__":
    target = '192.168.250.1'
    rate = [500,    # block size;
            0.5,    # rate per block; 
            1024,   # unit of block (Kb - 1024, Mb - 1024*1024); 
            -1,     # repeat n - repeat n times, -1 - repeat inf; 
            0]      # first free

    totalData, cost, plotXYin, plotXYout = tarrifParse('clean_data.csv', target, rate)

    print('for', totalData, 'kb total cost:', cost, 'rub')

    plotXYout = collections.OrderedDict(sorted(plotXYout.items()))
    plotXYin = collections.OrderedDict(sorted(plotXYin.items()))

    lout = plt.plot_date(plotXYout.keys(), plotXYout.values(), marker=',', color='red')
    lin = plt.plot_date(plotXYin.keys(), plotXYin.values(), marker=',')
    plt.setp(lout, linewidth=1.0, linestyle='-')
    plt.setp(lin, linewidth=1.0, linestyle='-')
    plt.show()