import time

def tariffing(outCallsTime,         ##
              inCallsTime,          ##
              SMSNumber,            ##
              callTime,             ##
              SMSRate,              ## rub per sms
              firstFree,            ## first minute or sms        [out, in, sms]
              timeRate):            ## charge for different time  [ [[t1, t2], [outRate, inRate]], ...]
    if timeRate:
        timeInt = int(str(callTime.tm_hour)+str(callTime.tm_min))
        inTCR = 0
        outTCR = 0
        for timePeriod in timeRate:
            if timeInt >= timePeriod[0][0] and timeInt < timePeriod[0][1]:
                outTCR = timePeriod[1][0]
                inTCR = timePeriod[1][1]
                break

        if inCallsTime:
            bill = (inCallsTime - firstFree[1])*inTCR
            return round(bill, 2), 0

        if outCallsTime:
            billC = (outCallsTime - firstFree[0]) * outTCR
            billS = (SMSNumber - firstFree[2]) * SMSRate
            return round(billC, 2), round(billS, 2)

    raise RuntimeError("bad arguments")