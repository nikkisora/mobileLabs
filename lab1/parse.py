import csv, time, math
import tariffing

def calcBilling(csvFP, number, SMSRate, firstFree, timeRate):
    totalCIn, totalCOut, totalS, outDur, inDur, smsN = 0, 0, 0, 0, 0, 0
    log = []
    with open(csvFP) as csv_f:
        data = csv.DictReader(csv_f)
        for row in data:
            timestamp, origin, destination, callDuration, SMSNumber = row.values()
            timeOfCall = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

            if origin == number:
                billC, billS = tariffing.tariffing(float(callDuration), 0, int(SMSNumber), timeOfCall, SMSRate, firstFree, timeRate)
                totalCOut += billC
                totalS += billS
                outDur+=float(callDuration)
                smsN += int(SMSNumber)
                log.append([time.strftime('%Y-%m-%d %H:%M:%S', timeOfCall), 'out', billC, billS])

            if destination == number:
                billC, billS = tariffing.tariffing(0, float(callDuration), 0, timeOfCall, SMSRate, firstFree, timeRate)
                totalCIn += billC
                totalS += billS
                inDur+=float(callDuration)
                log.append([time.strftime('%Y-%m-%d %H:%M:%S', timeOfCall), 'in', billC, billS, float(callDuration)])

        return log, totalCOut, totalCIn, totalS, outDur, inDur, smsN