import datetime
import weasyprint
import locale
import math
import sys
from bs4 import BeautifulSoup
from num2text import num2text

sys.path.insert(1, '../lab1')
from parse import calcBilling

sys.path.insert(1, '../lab2')
from netTariffingInOutGraph import tarrifParse

locale.setlocale(locale.LC_ALL, 'ru')

number = '968247916'
SMSRate = 1
firstFree = [0, 5, 5]
timeRate = [[[0000,2360], [4,1]]]

log, totalCOut, totalCIn, totalSms, outDur, inDur, smsN = calcBilling('../lab1/data.csv', number, SMSRate, firstFree, timeRate)

IPTarget = '192.168.250.1'
netRate = [500,    # block size;
        0.5,    # rate per block; 
        1024,   # unit of block (Kb - 1024, Mb - 1024*1024); 
        -1,     # repeat n - repeat n times, -1 - repeat inf; 
        0]      # first free

totalData, costData, plotXYin, plotXYout = tarrifParse('../lab2/clean_data.csv', IPTarget, netRate)


calls = [[outDur, timeRate[0][1][0], totalCOut], [inDur, timeRate[0][1][1], totalCIn]] #[outDur, cost, totalCost], [inDur, cost, totalCost]
sms = [smsN, SMSRate, totalSms] #[amount, cost, totalCost]
net = [totalData, 'КБ', str(netRate[1])+' за блок', costData] #[amount, unit, cost, totalCost]

itemTable = [['001', 'Исходящие вызовы', calls[0][0], 'Минут', calls[0][1], calls[0][2]],
             ['002','Входящие вызовы', calls[1][0], 'Минут', calls[1][1], calls[1][2]],
             ['012','Смс', sms[0], 'Шт.', sms[1], sms[2]],
             ['023','Интернет', net[0], net[1], net[2], net[3]]]

companyInfo = ['Лучший Банк',
               '045354601',
               '30101810600000374602',
               '589308271150',
               '775001001',
               'ООО"Дорогая телефония", ИНН 7723011004, КПП 772013089, 602063, Санкт-Петербург г ВЯЗЕМСКИЙ переулок, дом №15, тел.: 8-800-555-35-35']
recepientInfo = ['72306410590000127420',
                 'ИП МНОГО ДЕНЕГ',
                 'ИП МНОГО ДЕНЕГ, ИНН 7724613021, КПП 775923165, 602786, Санкт-Петербург г 2-Я линия Васильевского острова, дом №41, тел.: 8-812-323-56-03']

chief = 'Молодец О.А.'
accountant = 'Боженов Г.В.'

with open('blank.html', encoding='utf-8') as text:
    html = BeautifulSoup(text.read(), 'html.parser')
    # html.find(id="date").string = "asdas"
    # print(html.find(id="date").string)
    html.find(id="bankName").string = companyInfo[0]
    html.find(id="bankBik").string = companyInfo[1]
    html.find(id="account").string = companyInfo[2]
    html.find(id="inn").string = companyInfo[3]
    html.find(id="kpp").string = companyInfo[4]
    html.find(id="recepientAccount").string = recepientInfo[0]
    html.find(id="recepientName").string = recepientInfo[1]
    html.find(id="invoiceID").string = '1'
    html.find(id="date").string = datetime.date.strftime(datetime.date.today(), '%d %B %Y')
    html.find(id="fullName").string = companyInfo[5]
    html.find(id="recepientFullName").string = recepientInfo[2]

    totalCost = 0

    for i in range(len(itemTable)):
        totalCost+=itemTable[i][5]
        row = html.new_tag("tr")

        cellTag = html.new_tag("td")
        cellTag['style']='text-align:center;'
        cellTag.append(str(i+1))
        row.append(cellTag)

        cellTag = html.new_tag("td")
        cellTag['style']='text-align:left;'
        cellTag.append(str(itemTable[i][0]))
        row.append(cellTag)

        cellTag = html.new_tag("td")
        cellTag['style']='text-align:left;'
        cellTag.append(str(itemTable[i][1]))
        row.append(cellTag)

        cellTag = html.new_tag("td")
        cellTag['style']='text-align:right;'
        cellTag.append(str(itemTable[i][2]))
        row.append(cellTag)

        cellTag = html.new_tag("td")
        cellTag['style']='text-align:left;'
        cellTag.append(str(itemTable[i][3]))
        row.append(cellTag)

        cellTag = html.new_tag("td")
        cellTag['style']='text-align:right;'
        cellTag.append(str(itemTable[i][4]))
        row.append(cellTag)

        cellTag = html.new_tag("td")
        cellTag['style']='text-align:right;'
        cellTag.append(str(itemTable[i][5]))
        row.append(cellTag)

        html.find(id="itemContainer").append(row)

    html.find(id="totalCost").string = str(round(totalCost, 2))
    html.find(id="nds").string = str(round(totalCost-(totalCost/1.2), 2))
    html.find(id="totalItemNumber").string = str(len(itemTable))
    html.find(id="totalCost2").string = str(round(totalCost, 2))
    html.find(id="totalCostInWords").string = num2text(int(math.floor(totalCost)))+' руб. '+"{0:0=2d}".format(int((totalCost-math.floor(totalCost))*100))

    html.find(id="Chief").string = chief
    html.find(id="Accountant").string = accountant

    open('Filled.pdf', 'wb').write(weasyprint.HTML(string=html.prettify()).write_pdf())
