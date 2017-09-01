import requests
from bs4 import BeautifulSoup
from option.models import *


def update_deposite():
     res=requests.get('http://www.dce.com.cn/publicweb/notificationtips/queryDayTradParaByVariety.html?variety=m')
     soup=BeautifulSoup(res.text,'html.parser')
     trs= soup.find_all('tr')



for i in range(2,len(trs)):
     tds=trs[i].find_all('td')
     name=tds[0].text.strip() #期权或者期货的名称
     price=tds[2].text.strip()#对应的保证金
     price = float(price.replace(',', ''))
     print(name,price)
#m1708，m1709系列期权的保证金信息大商所没有